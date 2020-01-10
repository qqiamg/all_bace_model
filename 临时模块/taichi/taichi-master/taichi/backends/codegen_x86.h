// x86 backend implementation

#pragma once

#include "kernel.h"

TLANG_NAMESPACE_BEGIN

class CPUCodeGen : public KernelCodeGen {
 public:
  std::map<int, std::string> masks;

 public:
  CPUCodeGen(const std::string &kernel_name) : KernelCodeGen(kernel_name) {
    suffix = "cpp";
  }

  void lower() override;

  void lower_cpp();
  void lower_llvm();

  void codegen() override;

  virtual FunctionType codegen_llvm() override;
};

TLANG_NAMESPACE_END
