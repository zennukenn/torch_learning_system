# Call chain — `torch.add`

- Exact revision: `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`)
- Minimal input program: intended `torch.add(x, y, alpha=2)` with CPU strided tensors; runtime unavailable
- Tensor metadata: CPU and dense/strided assumed; dtype, shape/stride, grad mode, and compile mode were not executed or observed
- Question being answered: How does `torch.add` reach a generated CPU add loop in this revision?

| Layer | Symbol/path | What happens | Evidence | Observed/Documented/Inferred |
|---|---|---|---|---|
| Public Python API | `torch.add` | Function variant accepts two tensors and keyword-only `alpha` | Schema has `variants: function, method` | Inferred; generated binding was not inspected |
| Override/mode | Not inspected | `__torch_function__`, modes, and subclasses are outside this first trace | Not inspected | Unresolved |
| Binding/generated wrapper | `tools/autograd/gen_autograd.py`; generated build output absent | Python binding is generated from native operator metadata | Generator comments and entry points inspected | Inferred for this operator |
| Schema/overload | `aten/src/ATen/native/native_functions.yaml:536` | Defines `add.Tensor`, delegates structured generation to `add.out` | Direct source inspection | Observed |
| DispatchKeySet/selection | Generated registration; runtime table unavailable | CPU is expected to be selected from input tensor dispatch keys | CPU-only codegen produced registration sources | Inferred; runtime selection unverified |
| Fallback/redispatch | Not inspected | Sparse and special layouts have explicit schema dispatch entries | `native_functions.yaml:540` | Observed only at schema level |
| ATen meta | `aten/src/ATen/native/BinaryOps.cpp:151` | Builds the binary `TensorIterator`, infers output metadata, and checks `alpha` | Direct source inspection | Observed |
| Generated structured CPU | temporary `UfuncCPU_add.cpp` | Defines `add_stub` and calls it with `device_type()`, iterator, and `alpha` | Focused `torchgen` output | Observed generated evidence |
| Generated CPU kernel | temporary `UfuncCPUKernel_add.cpp` | Switches on common dtype, invokes `cpu_kernel`/`cpu_kernel_vec`, and registers `add_kernel` to `add_stub` | Focused `torchgen` output | Observed generated evidence |
| Tensor/storage/runtime effect | Not inspected | Output allocation and storage effects remain unresolved | No runtime/build evidence | Unresolved |
| Result | Expected `10 + 2 * 3 = 16` | Learner predicted the scalar result correctly after `alpha` explanation | Learner answer | Conceptual only; runtime unverified |

## Optional branches

- Autograd: not inspected.
- Dynamo/FX/export/AOT/Inductor: not inspected.
- allocator/device guard/stream/event: not inspected.
- distributed: not involved in this focused trace.

## Verification

- Prediction: `ufunc_inner_loop` causes `torchgen` to emit CPU structured and dtype-specialized kernel sources.
- Command/test/debugger setup: `python3 -m torchgen.gen -s aten/src/ATen -d <temp> --per-operator-headers --op-registration-whitelist aten::add --backend-whitelist CPU --generate headers sources`
- Actual result: exit 0 in about 5 seconds; generated `UfuncCPU_add.cpp` and `UfuncCPUKernel_add.cpp`. The latter contained dtype cases, `cpu_kernel`/`cpu_kernel_vec`, `ufunc::add`, and `REGISTER_DISPATCH(add_stub, &add_kernel)`.
- Remaining uncertainty: no installed `torch`, source build, dispatch-table query, generated Python binding inspection, or runtime execution. End-to-end runtime dispatch is **unverified**.
- Learner's no-notes reconstruction: “不知道”; no independent trace or source-anchor recall was demonstrated.
