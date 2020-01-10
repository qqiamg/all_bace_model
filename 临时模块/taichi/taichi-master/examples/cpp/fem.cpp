#include <taichi/lang.h>
#include <taichi/util.h>
#include <taichi/visual/gui.h>
#include <taichi/system/profiler.h>
#include <taichi/visual/texture.h>
#include <deque>

TC_NAMESPACE_BEGIN

#include "fem_coeff.h"

using namespace Tlang;

constexpr int dim = 3, n = 256;
real F = -10;

const auto E = 1_f;     // Young's Modulus
const auto nu = 0.2_f;  // Poisson ratio

const real mu_0 = E / (2 * (1 + nu));
const real lambda_0 = E * nu / ((1 + nu) * (1 - 2 * nu));
auto active = new bool[n][n][n]();
auto R = new real[n][n][n][dim]();
auto D = new real[n][n][n]();
auto X = new real[n][n][n][dim]();

auto fem = [](std::vector<std::string> cli_param) {
  CoreState::set_trigger_gdb_when_crash(true);

  auto param = parse_param(cli_param);

  bool gpu = param.get("gpu", false);
  TC_P(gpu);
  bool vectorization = param.get("vec", true);
  TC_P(vectorization);
  int threads = param.get("threads", 8);
  TC_P(threads);
  bool use_cache = param.get("cache", true);
  TC_P(use_cache);
  bool compute_gt = param.get("compute_gt", false);
  TC_P(compute_gt);
  Program prog(gpu ? Arch::gpu : Arch::x86_64);
  prog.config.simplify_before_lower_access = param.get("simp1", true);
  TC_P(prog.config.simplify_before_lower_access);
  prog.config.lower_access = param.get("lower_access", true);
  TC_P(prog.config.lower_access);
  prog.config.print_ir = param.get("print_ir", false);
  TC_P(prog.config.print_ir);
  prog.config.simplify_after_lower_access = param.get("simp2", true);
  TC_P(prog.config.simplify_after_lower_access);
  prog.config.attempt_vectorized_load_cpu = param.get("vec_load_cpu", true);
  TC_P(prog.config.attempt_vectorized_load_cpu);
  bool use_pointer = param.get("use_pointer", true);
  TC_P(use_pointer);
  bool block_soa = param.get("block_soa", true);
  TC_P(block_soa);
  prog.config.lazy_compilation = false;

  Vector x(DataType::f32, dim), r(DataType::f32, dim), p(DataType::f32, dim),
      Ap(DataType::f32, dim);

  Global(alpha, f32);
  Global(beta, f32);
  Global(sum, f32);

  AmbientGlobal(lambda, f32, 0.0f);
  AmbientGlobal(mu, f32, 0.0f);

  int block_size = 8;

  layout([&]() {
    auto ijk = Indices(0, 1, 2);
    std::function<void(Matrix & mat)> place;
    std::function<void(Expr & expr)> place_scalar;

    SNode *block;
    if (block_soa) {
      if (use_pointer) {
        block = &root.dense(ijk, n / block_size).pointer();
      } else {
        block = &root.dense(ijk, n / block_size).bitmasked();
      }
      place_scalar = [&](Expr &s) { block->dense(ijk, block_size).place(s); };
      place = [&](Matrix &mat) {
        for (auto &e : mat.entries) {
          place_scalar(e);
        }
      };
    } else {
      place = [&](Matrix &mat) {
        root.dense(ijk, n / block_size).dense(ijk, block_size).place(mat);
      };
      place_scalar = [&](Expr &mat) {
        root.dense(ijk, n / block_size).dense(ijk, block_size).place(mat);
      };
    }

    place(x);
    place(p);
    place(Ap);
    place(r);
    place_scalar(lambda);
    place_scalar(mu);
    root.place(alpha, beta, sum);
  });

  Kernel(compute_Ap).def([&] {
    BlockDim(256);
    if (!gpu) {
      Parallelize(threads);
      if (vectorization)
        Vectorize(block_size);
    }
    For(Ap(0), [&](Expr i, Expr j, Expr k) {
      auto cell_coord = Var(Vector({i, j, k}));
      auto Ku_tmp = Var(Vector(dim));
      Ku_tmp = Vector({0.0f, 0.0f, 0.0f});
      for (int cell = 0; cell < pow<dim>(2); cell++) {
        auto cell_offset =
            Var(Vector({-(cell / 4), -(cell / 2 % 2), -(cell % 2)}));
        auto cell_lambda = lambda[cell_coord + cell_offset];
        auto cell_mu = mu[cell_coord + cell_offset];
        for (int node = 0; node < pow<dim>(2); node++) {
          auto node_offset = Var(Vector({node / 4, node / 2 % 2, node % 2}));
          for (int u = 0; u < dim; u++) {
            for (int v = 0; v < dim; v++) {
              Ku_tmp(u) += (cell_lambda * K_la[cell][node][u][v] +
                            cell_mu * K_mu[cell][node][u][v]) *
                           p[cell_coord + cell_offset + node_offset](v);
            }
          }
        }
      }
      // boundary condition
      If(j < 2).Then([&] { Ku_tmp = Vector({0.0f, 0.0f, 0.0f}); });
      Ap[i, j, k] = Ku_tmp;
    });
  });

  prog.config.print_ir = false;

  Kernel(reduce_r).def([&] {
    mark_reduction();
    Parallelize(threads);
    Vectorize(block_size);
    For(r(0), [&](Expr i, Expr j, Expr k) {
      Atomic(sum[Expr(0)]) += r[i, j, k].norm2();
    });
  });

  Kernel(reduce_pAp).def([&] {
    mark_reduction();
    Parallelize(threads);
    Vectorize(block_size);
    For(r(0), [&](Expr i, Expr j, Expr k) {
      auto tmp = Var(0.0f);
      for (int d = 0; d < dim; d++) {
        tmp += p[i, j, k](d) * Ap[i, j, k](d);
      }
      Atomic(sum[Expr(0)]) += tmp;
    });
  });

  Kernel(update_x).def([&] {
    Parallelize(threads);
    Vectorize(block_size);
    For(x(0), [&](Expr i, Expr j, Expr k) {
      x[i, j, k] += alpha[Expr(0)] * p[i, j, k];
    });
  });

  Kernel(update_r).def([&] {
    Parallelize(threads);
    Vectorize(block_size);
    For(p(0), [&](Expr i, Expr j, Expr k) {
      r[i, j, k] -= alpha[Expr(0)] * Ap[i, j, k];
    });
  });

  Kernel(copy_b_to_r).def([&] {
    For(p(0), [&](Expr i, Expr j, Expr k) {
      If(i == n / 2 && j == n / 2 && k == n / 2)
          // If(j == n / 2)
          .Then([&] {
            r[i, j, k] = Vector({0.0f, -1.0f, 0.0f});
          })
          .Else([&] {
            r[i, j, k] = Vector({0.0f, 0.0f, 0.0f});
          });
    });
  });

  Kernel(update_p).def([&] {
    Parallelize(threads);
    Vectorize(block_size);
    For(p(0), [&](Expr i, Expr j, Expr k) {
      p[i, j, k] = r[i, j, k] + beta[Expr(0)] * p[i, j, k];
    });
  });

  Kernel(enforce_bc).def([&] {
    For(x(0), [&](Expr i, Expr j, Expr k) {
      If(j == 0).Then([&] { x[i, j, k] = Vector({0.0f, 0.0f, 0.0f}); });
    });
  });

  auto tex = create_instance<Texture>(
      "mesh", Dict()
                  .set("resolution", Vector3(n))
                  .set("translate", Vector3(0.55, 0.35, 0.47))
                  .set("scale", Vector3(1.1))
                  .set("adaptive", false)
                  .set("filename", "$mpm/bunny_small.obj"));

  for (int i = 1; i < n - 2; i++) {
    for (int j = 1; j < n - 2; j++) {
      for (int k = 1; k < n - 2; k++) {
        bool inside = tex->sample((Vector3(0.5f) + Vector3(i, j, k)) *
                                  Vector3(1.0f / (n - 1)))
                          .x > 0.5f;
        // inside = pow<2>(i - n / 2) + pow<2>(k - n / 2) < pow<2>(n / 2) / 2;
        // inside = i < n * 0.8 && j < n * 0.8 && k < n * 0.8;
        if (inside) {
          D[i][j][k] = 1;
          active[i][j][k] = true;
          lambda.val<float32>(i, j, k) = lambda_0;
          mu.val<float32>(i, j, k) = mu_0;
          for (int K = 0; K < 8; K++) {
            // populate neighbouring nodes
            x(0).val<float32>(i + K / 4, j + K / 2 % 2, k + K % 2) = 0.0f;
          }
        }
      }
    }
  }
  r(1).val<float32>(n / 2, n / 2, n / 2) = F;
  R[n / 2][n / 2][n / 2][1] = F;

  std::deque<Vector3i> q;
  q.push_back(Vector3i(n / 2));  // Assuming the center voxel is active
  std::function<void(int, int, int)> enqueue = [&](int i, int j, int k) {
    if (active[i][j][k]) {
      active[i][j][k] = false;
      q.push_back(Vector3i(i, j, k));
    }
  };
  while (!q.empty()) {
    auto x = q.front();
    q.pop_front();
    auto i = x[0];
    auto j = x[1];
    auto k = x[2];
    enqueue(i + 1, j, k);
    enqueue(i - 1, j, k);
    enqueue(i, j + 1, k);
    enqueue(i, j - 1, k);
    enqueue(i, j, k + 1);
    enqueue(i, j, k - 1);
  }

  for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - 1; j++) {
      for (int k = 0; k < n - 1; k++) {
        TC_ASSERT(!active[i][j][k]);
      }
    }
  }

  // r = b - Ax = b    since x = 0
  // copy_b_to_r();
  // p = r = r + 0 p
  update_p();
  sum.val<float32>() = 0;
  reduce_r();
  auto old_rTr = sum.val<float32>();

  for (int i = 0; i < 1000; i++) {
    TC_P(i);
    compute_Ap();
    sum.val<float32>() = 0;
    reduce_pAp();
    auto pAp = sum.val<float32>();
    // alpha = rTr / pTAp
    alpha.val<float32>() = old_rTr / pAp;
    TC_P(old_rTr);
    // TC_P(pAp);
    // TC_P(alpha.val<float32>());
    // x = x + alpha p
    update_x();
    // r = r - alpha Ap
    update_r();
    // return if |r| small
    sum.val<float32>() = 0;
    reduce_r();
    auto new_rTr = sum.val<float32>();
    // TC_P(new_rTr);
    if (new_rTr < 1e-5f)
      break;
    // beta = new rTr / old rTr
    beta.val<float32>() = new_rTr / old_rTr;
    // TC_P(beta.val<float32>());
    // p = r + beta p
    update_p();
    old_rTr = new_rTr;
    get_current_program().profiler_print();
  }

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      for (int k = 0; k < n; k++) {
        for (int d = 0; d < dim; d++) {
          p(d).val<float32>(i, j, k) = x(d).val<float32>(i, j, k);
        }
      }
    }
  }

  compute_Ap();
  auto residual = 0.0f;
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      for (int k = 0; k < n; k++) {
        for (int d = 0; d < dim; d++) {
          residual += std::abs(R[i][j][k][d] - Ap(d).val<float32>(i, j, k));
        }
      }
    }
  }
  TC_P(residual);
  auto difference = 0.0f;
  auto difference_max = 0.0f;
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      for (int k = 0; k < n; k++) {
        for (int d = 0; d < dim; d++) {
          difference += std::abs(X[i][j][k][d] - x(d).val<float32>(i, j, k));
          difference_max =
              std::max(difference_max,
                       std::abs(X[i][j][k][d] - x(d).val<float32>(i, j, k)));
        }
      }
    }
  }
  TC_P(difference);
  TC_P(difference_max);

  int gui_res = 512;
  GUI gui("FEM", Vector2i(gui_res + 200, gui_res), false);
  int gt = 0;
  int k = 0;
  gui.slider("z", k, 0, n - 1).slider("Ground truth", gt, 0, 1);

  int scale = gui_res / n;
  auto &canvas = gui.get_canvas();
  for (int frame = 1;; frame++) {
    for (int i = 0; i < gui_res - scale; i++) {
      for (int j = 0; j < gui_res - scale; j++) {
        real dx, dy, dz;
        if (!gt) {
          dx = x(0).val<float32>(i / scale, j / scale, k);
          dy = x(1).val<float32>(i / scale, j / scale, k);
          dz = x(2).val<float32>(i / scale, j / scale, k);
        } else {
          dx = X[i / scale][j / scale][k][0];
          dy = X[i / scale][j / scale][k][1];
          dz = X[i / scale][j / scale][k][2];
        }
        canvas.img[i][j] = Vector4(0.5f) + Vector4(dx, dy, dz, 0) * 0.5f;
      }
    }
    gui.update();
  }
};
TC_REGISTER_TASK(fem);

TC_NAMESPACE_END
