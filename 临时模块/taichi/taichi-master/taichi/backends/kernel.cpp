// Driver class for kernel codegen

#include "kernel.h"
#include <taichi/system/timer.h>

TLANG_NAMESPACE_BEGIN

FunctionType KernelCodeGen::compile(taichi::Tlang::Program &prog,
                                    taichi::Tlang::Kernel &kernel) {
  // auto t = Time::get_time();
  this->prog = &kernel.program;
  this->kernel = &kernel;
  lower();
  if (prog.config.use_llvm) {
    TC_PROFILER("codegen llvm")
    return codegen_llvm();
  } else {
    codegen();
    generate_binary("");
    // TC_P(Time::get_time() - t);
    return load_function();
  }
}

TLANG_NAMESPACE_END
