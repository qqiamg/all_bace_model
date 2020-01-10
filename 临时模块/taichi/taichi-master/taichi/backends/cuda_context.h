#if defined(TLANG_WITH_CUDA)
#include "llvm_jit.h"
#include <taichi/context.h>
#include <taichi/cuda_utils.h>

TLANG_NAMESPACE_BEGIN

class CUDAContext {
  CUdevice device;
  std::vector<CUmodule> cudaModules;
  CUcontext context;
  int dev_count;
  CUdeviceptr context_buffer;
  std::string mcpu;

 public:
  CUDAContext();

  bool detected() const {
    return dev_count != 0;
  }

  CUmodule compile(const std::string &ptx);

  CUfunction get_function(CUmodule module, const std::string &func_name);

  void launch(CUfunction func,
              void *context_ptr,
              unsigned gridDim,
              unsigned blockDim);

  std::string get_mcpu() const {
    return mcpu;
  }

  void make_current() {
    check_cuda_errors(cuCtxSetCurrent(context));
  }

  ~CUDAContext();

  class ContextGuard {
   private:
    CUcontext old_ctx;

   public:
    ContextGuard(CUDAContext *ctx) {
      check_cuda_errors(cuCtxGetCurrent(&old_ctx));
      ctx->make_current();
    }

    ~ContextGuard() {
      check_cuda_errors(cuCtxSetCurrent(old_ctx));
    }
  };

  ContextGuard get_guard() {
    return ContextGuard(this);
  }
};

extern std::unique_ptr<CUDAContext> cuda_context;

TLANG_NAMESPACE_END
#endif
