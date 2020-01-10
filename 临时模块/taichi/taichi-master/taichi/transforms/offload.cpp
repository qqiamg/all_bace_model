#include <set>
#include "../ir.h"

TLANG_NAMESPACE_BEGIN

namespace irpass {

class Offloader {
 public:
  Offloader(IRNode *root) {
    run(root);
  }

  void fix_loop_index_load(Stmt *s,
                           Stmt *loop_var,
                           int index,
                           bool is_struct_for) {
    replace_statements_with(
        s,
        [&](Stmt *load) {
          if (auto local_load = load->cast<LocalLoadStmt>()) {
            return local_load->width() == 1 &&
                   local_load->ptr[0].var == loop_var &&
                   local_load->ptr[0].offset == 0;
          }
          return false;
        },
        [&]() { return Stmt::make<LoopIndexStmt>(index, is_struct_for); });
  }

  void run(IRNode *root) {
    auto root_block = dynamic_cast<Block *>(root);
    auto root_statements = std::move(root_block->statements);
    root_block->statements.clear();

    auto pending_serial_statements =
        Stmt::make_typed<OffloadedStmt>(OffloadedStmt::TaskType::serial);

    auto assemble_serial_statements = [&]() {
      if (!pending_serial_statements->body->statements.empty()) {
        root_block->insert(std::move(pending_serial_statements));
        pending_serial_statements =
            Stmt::make_typed<OffloadedStmt>(OffloadedStmt::TaskType::serial);
      }
    };

    for (int i = 0; i < (int)root_statements.size(); i++) {
      auto &stmt = root_statements[i];
      if (auto s = stmt->cast<RangeForStmt>(); s && !s->strictly_serialized) {
        assemble_serial_statements();
        auto offloaded =
            Stmt::make_typed<OffloadedStmt>(OffloadedStmt::TaskType::range_for);
        offloaded->body = std::make_unique<Block>();
        offloaded->begin = s->begin->as<ConstStmt>()->val[0].val_int32();
        offloaded->end = s->end->as<ConstStmt>()->val[0].val_int32();
        offloaded->block_dim = s->block_dim;
        offloaded->num_cpu_threads = s->parallelize;
        fix_loop_index_load(s, s->loop_var, 0, false);
        for (int j = 0; j < (int)s->body->statements.size(); j++) {
          offloaded->body->insert(std::move(s->body->statements[j]));
        }
        root_block->insert(std::move(offloaded));
      } else if (auto s = stmt->cast<StructForStmt>()) {
        assemble_serial_statements();
        emit_struct_for(s, root_block);
      } else {
        pending_serial_statements->body->insert(std::move(stmt));
      }
    }
    assemble_serial_statements();
  }

  void emit_struct_for(StructForStmt *for_stmt, Block *root_block) {
    auto leaf = for_stmt->snode;
    TC_ASSERT(leaf->type == SNodeType::place)
    // make a list of nodes, from the leaf block (instead of 'place') to root
    std::vector<SNode *> path;
    // leaf is the place (scalar)
    // leaf->parent is the leaf block
    // so listgen should be invoked from the root to leaf->parent->parent
    for (auto p = leaf->parent; p; p = p->parent) {
      path.push_back(p);
    }
    std::reverse(path.begin(), path.end());

    for (int i = 1; i < path.size(); i++) {
      auto snode_child = path[i];
      auto offloaded_clear_list =
          Stmt::make_typed<OffloadedStmt>(OffloadedStmt::TaskType::clear_list);
      offloaded_clear_list->snode = snode_child;
      root_block->insert(std::move(offloaded_clear_list));
      auto offloaded_listgen =
          Stmt::make_typed<OffloadedStmt>(OffloadedStmt::TaskType::listgen);
      offloaded_listgen->snode = snode_child;
      root_block->insert(std::move(offloaded_listgen));
    }

    auto offloaded_struct_for =
        Stmt::make_typed<OffloadedStmt>(OffloadedStmt::TaskType::struct_for);

    for (int i = 0; i < for_stmt->loop_vars.size(); i++) {
      fix_loop_index_load(for_stmt, for_stmt->loop_vars[i],
                          leaf->physical_index_position[i], true);
    }

    for (int i = 0; i < (int)for_stmt->body->statements.size(); i++) {
      offloaded_struct_for->body->insert(
          std::move(for_stmt->body->statements[i]));
    }

    offloaded_struct_for->block_dim = for_stmt->block_dim;
    offloaded_struct_for->snode = for_stmt->snode;
    offloaded_struct_for->num_cpu_threads = for_stmt->parallelize;

    root_block->insert(std::move(offloaded_struct_for));
  }
};

/*
After offloading, some local variables are accessed across offloaded blocks.
This pass promote these local variables into global variables.

Steps:
  1. Traverse offloaded blocks to identify out-of-block local LD/ST
  2. Replace alloca with global var initializtion (set to 0)
     Replace local LD/ST with global LD/ST
*/

class IdentifyLocalVars : public BasicStmtVisitor {
 public:
  using BasicStmtVisitor::visit;

  std::map<Stmt *, std::size_t> local_to_global;
  std::map<Stmt *, Stmt *> local_to_offloaded;
  Stmt *current_offloaded;
  std::size_t global_offset;

  std::size_t allocate_global(VectorType type) {
    TC_ASSERT(type.width == 1);
    auto ret = global_offset;
    global_offset += data_type_size(type.data_type);
    TC_ASSERT(global_offset < taichi_max_num_global_vars);
    return ret;
  }

  IdentifyLocalVars() {
    allow_undefined_visitor = true;
    current_offloaded = nullptr;
    global_offset = 0;
  }

  void visit(OffloadedStmt *stmt) override {
    current_offloaded = stmt;
    if (stmt->body)
      stmt->body->accept(this);
    current_offloaded = nullptr;
  }

  void visit(AllocaStmt *stmt) override {
    TC_ASSERT(current_offloaded);
    local_to_offloaded[stmt] = current_offloaded;
  }

  void test_and_allocate(Stmt *stmt) {
    if (local_to_offloaded[stmt] == current_offloaded)
      return;
    if (local_to_global.find(stmt) == local_to_global.end()) {
      local_to_global[stmt] = allocate_global(stmt->ret_type);
    }
  }

  void visit(LocalLoadStmt *stmt) override {
    TC_ASSERT(current_offloaded);
    TC_ASSERT(stmt->width() == 1);
    test_and_allocate(stmt->ptr[0].var);
  }

  void visit(LocalStoreStmt *stmt) override {
    TC_ASSERT(current_offloaded);
    TC_ASSERT(stmt->width() == 1);
    test_and_allocate(stmt->ptr);
  }

  void visit(AtomicOpStmt *stmt) override {
    TC_ASSERT(current_offloaded);
    TC_ASSERT(stmt->width() == 1);
    if (stmt->dest->is<AllocaStmt>()) {
      test_and_allocate(stmt->dest);
    }
  }

  static std::map<Stmt *, std::size_t> run(IRNode *root) {
    IdentifyLocalVars pass;
    root->accept(&pass);
    return pass.local_to_global;
  }
};

class PromoteLocals : public BasicStmtVisitor {
 public:
  using BasicStmtVisitor::visit;

  std::map<Stmt *, std::size_t> local_to_global_offset;
  std::map<Stmt *, VectorType> local_to_global_vector_type;

  PromoteLocals(std::map<Stmt *, std::size_t> local_to_global_offset)
      : local_to_global_offset(local_to_global_offset) {
    allow_undefined_visitor = true;
  }

  void visit(AllocaStmt *stmt) override {
    if (local_to_global_offset.find(stmt) == local_to_global_offset.end())
      return;
    VecStatement replacement;
    auto ret_type = stmt->ret_type;
    local_to_global_vector_type[stmt] = ret_type;
    auto ptr = replacement.push_back<GlobalTemporaryStmt>(
        local_to_global_offset[stmt], ret_type);
    LaneAttribute<TypedConstant> zeros(std::vector<TypedConstant>(
        stmt->width(), TypedConstant(stmt->ret_type.data_type)));
    auto const_zeros = replacement.push_back<ConstStmt>(zeros);
    replacement.push_back<GlobalStoreStmt>(ptr, const_zeros);

    stmt->parent->replace_with(stmt, replacement, false);
    throw IRModified();
  }

  void visit(LocalLoadStmt *stmt) override {
    TC_ASSERT(stmt->width() == 1);
    auto alloca = stmt->ptr[0].var;
    if (local_to_global_offset.find(alloca) == local_to_global_offset.end())
      return;

    VecStatement replacement;
    auto ret_type = stmt->ret_type;

    auto ptr = replacement.push_back<GlobalTemporaryStmt>(
        local_to_global_offset[alloca], ret_type);
    replacement.push_back<GlobalLoadStmt>(ptr);

    stmt->parent->replace_with(stmt, replacement);
    throw IRModified();
  }

  void visit(LocalStoreStmt *stmt) override {
    TC_ASSERT(stmt->width() == 1);
    auto alloca = stmt->ptr;
    if (local_to_global_offset.find(alloca) == local_to_global_offset.end())
      return;

    VecStatement replacement;
    auto ret_type = stmt->ret_type;

    auto ptr = replacement.push_back<GlobalTemporaryStmt>(
        local_to_global_offset[alloca], ret_type);
    replacement.push_back<GlobalStoreStmt>(ptr, stmt->data);

    stmt->parent->replace_with(stmt, replacement);
    throw IRModified();
  }

  void visit(AtomicOpStmt *stmt) override {
    TC_ASSERT(stmt->width() == 1);
    auto alloca = stmt->dest;
    if (local_to_global_offset.find(alloca) == local_to_global_offset.end())
      return;

    VecStatement replacement;
    auto ret_type = stmt->dest->ret_type;

    auto ptr = replacement.push_back<GlobalTemporaryStmt>(
        local_to_global_offset[alloca], ret_type);
    replacement.push_back<AtomicOpStmt>(stmt->op_type, ptr, stmt->val);

    stmt->parent->replace_with(stmt, replacement);
    throw IRModified();
  }

  static void run(IRNode *root,
                  std::map<Stmt *, std::size_t> local_to_global_offset) {
    PromoteLocals pass(local_to_global_offset);
    while (true) {
      try {
        root->accept(&pass);
      } catch (IRModified) {
        continue;
      }
      break;
    }
  }
};

void offload(IRNode *root) {
  Offloader _(root);
  irpass::typecheck(root);
  irpass::fix_block_parents(root);
  {
    auto local_to_global = IdentifyLocalVars::run(root);
    PromoteLocals::run(root, local_to_global);
  }
  irpass::typecheck(root);
  irpass::re_id(root);
}

}  // namespace irpass

TLANG_NAMESPACE_END
