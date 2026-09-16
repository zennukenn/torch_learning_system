# PyTorch knowledge and learning-path coverage audit

Audit date: 2026-09-15
PyTorch reference: `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`)

## Audit standard

PyTorch is too large for a reduced implementation to reproduce every API or specialized backend. “Comprehensive” therefore means:

- every major architecture and engineering boundary is taught and mapped to current source;
- every I0 subsystem has a runnable MiniTorch mechanism and representative vertical slice;
- source-scale variants are sampled through I1/I2 reading and focused experiments;
- learner evidence covers explanation, location, trace, debugging, modification, transfer and retention;
- the final project runs independently on CPU, on available CUDA, and through mock-tested PrivateUse contracts; real third-party hardware claims require private adapter execution evidence.

The size rule is **mechanism-complete, surface-small**. Empty directory mirroring and operator-count inflation do not count as coverage.

## Findings and remediation

The 2026-09-13 pre-audit plan already covered Tensor/Storage, dispatcher/codegen, CPU/CUDA kernels, Python frontend, minimal Autograd, CUDA memory/streams, distributed DP/TP, compiler, packaging and simulated devices. The audit identified these under-specified areas and adds them to the gated path:

- numerical semantics: broadcasting, type promotion, tolerance, NaN/Inf, overflow, determinism and RNG;
- CPU inference/runtime: allocator/alignment, parallel loops, vectorization, BLAS/oneDNN-style library boundaries and thread control;
- CUDA execution depth: grid/block mapping, coalescing, shared memory, atomics, occupancy and representative cuBLAS/cuDNN-style integration;
- CPython/native boundary: extension loading, GIL release, exception translation, ownership, ABI, symbols and RPATH;
- custom operators and testing: schema/library registration, fake/meta, opcheck-style contracts, OpInfo-style parametrization, sanitizers and failure tests;
- deployment: state loading safety, mmap/lazy loading concepts, export/AOT artifact, wheel/ABI/version matrix;
- quantized inference: quantization parameters, packing, error/tolerance behavior and representative compiler lowering;
- dual PrivateUse integration: MiniTorch plugin ABI plus native PyTorch `PrivateUse1` out-of-tree package;
- backend hardware conformance: capability negotiation, allocator/copy/stream/event/kernel/compiler contracts and sanitized private execution evidence.

The 2026-09-15 pedagogical audit found a separate execution defect: although
the documents called the curriculum project-driven, the session protocol and
manifest could still reward a long chain of oral diagnostics and required at
least one question row. This allowed teaching to drift away from the MiniTorch
worktree. The remediation is now explicit and machine-checked:

- one opening diagnostic set of at most three questions;
- 10–20 minute prerequisite blocks followed immediately by learner-authored
  MiniTorch edits, diff inspection and focused verification;
- no repeated oral repair loop; unresolved gaps become code/test/source tasks;
- structured `practice_cycles` and `authorship` in completed session manifests;
- question rows are optional and never a quota;
- `COURSE_PRACTICE_MAP.csv` assigns all 41 concepts to a first accountable
  project course with an immediate learner action and runnable evidence.

The product/engineering audit then found excessive hot-context loading,
duplicated policy text and a 135–220 hour delay before the first model. The
scope remains intact, but delivery now uses three independently useful releases:
Release A reaches a restricted real CPU model in 30–50 hours; Release B replaces
the walking-skeleton shortcuts with durable Tensor/Dispatcher/CUDA/model
contracts; Release C completes Autograd, distributed, compiler, dual PrivateUse
and deployment depth. Course order, hours and ownership now come from one
machine-readable course map and the learner-facing tables are generated.

## Coverage by architecture area

| Area | Required knowledge | MiniTorch evidence | Milestones | Priority |
|---|---|---|---|---|
| Global architecture | Python API, native core, dispatcher, kernels, Autograd, runtime, compiler, distributed, backend ownership | learner architecture/directory map and repeated vertical slices | M0–M9 | F0/I0 |
| Python execution | import/package, object model, descriptors/hooks, context managers, typing, traceback | frontend/config changes and code defense | M0, M4 | F0/I0 |
| C++ foundations | declarations/definitions, compile/link, RAII, pointer/reference, move, template/macro, type erasure, concurrency | learner native library and later core changes | M0–M3 | F0/I0 |
| CPython/pybind11 | extension module, conversion, lifetime, GIL, exception mapping, shared-library ABI | `minitorch._C` plus lifetime/GIL/error tests | M0, M1 | F0/I0 |
| Build/package/tooling | `pyproject.toml`, setuptools, CMake target graph, generated sources, wheel, RPATH, CI, debugger/sanitizers | clean editable/wheel installs and debug/tooling lab | M0, M9 | F0/I0 |
| Tensor core | Tensor handle, TensorImpl, StorageImpl, allocator/DataPtr, sizes/strides/offset, view/alias/version | CPU Tensor implementation and mutation/lifetime tests | M1 | I0 |
| Numerical semantics | scalar/dtype, promotion, broadcasting, accumulation dtype, errors/tolerance, RNG/determinism | reference matrix and adversarial tests | M1–M4 | I0 |
| Operator system | schema/overload/alias, codegen, boxed/unboxed concepts, registration lifetime, key set, fallback/redispatch | generated representative operators and dispatch trace | M2 | I0 |
| CPU backend | TensorIterator-like iteration, parallelism, vectorization, threading, BLAS/oneDNN boundary | scalar then parallel/vector/library comparison | M2 | I0/I1 |
| Custom ops | library/schema/kernel/fake registration, mutation/alias contract and testing | one external custom-op package or plugin | M2, M8 | I1 |
| CUDA execution | host/device compilation, launch, error, device guard, streams/events, libraries | focused CUDA kernels and dispatch tests | M3 | I0 |
| CUDA memory | caching allocator, reserved/allocated, fragmentation/OOM, pinned memory, async lifetime, CUDA Graph constraints | deterministic memory and stream-lifetime dossier | M3 | I0 |
| Python `nn` | Module call/state, parameter/buffer, eval, serialization, hooks | CNN and decoder Transformer frontend | M4 | I0 |
| Inference semantics | modes, mixed precision, layout, dynamic batch/sequence, KV cache, batching | CPU/CUDA CNN and Transformer parity matrix | M4 | I0 |
| Quantized inference | observer/calibration boundary, scale/zero-point, packing, weight-only/int8 Linear, backend lowering | one representative eager and compiled path | M4, M7, M9 | I1 |
| Autograd boundary | graph/Node/edge, saved tensors, engine, version checks, Autograd dispatch, inference/no-grad | minimal backward and MLP smoke only | M5 | T1 |
| Runtime/observability | allocator, TLS, thread pool, RNG, profiler, serialization and error propagation | profile/memory timeline and reproducible failures | M3, M6 | I0 |
| Distributed core | Store/rendezvous, rank/world, ProcessGroup/Work, collectives, timeout/failure | local two-process runtime | M6 | I0 |
| Distributed inference | DeviceMesh/DTensor placement, DP, row/column TP, checkpoint, overlap; PP/CP/EP overview | two-rank DP and TP model slices | M6 | I0/I2 |
| Graph representation | FX-like IR, node/value/meta, fake tensor, symbolic shapes | graph capture and metadata propagation | M7 | I0 |
| Compiler stack | frame capture/guards/breaks, export, functionalization, decomposition, AOTAutograd boundary, lowering/fusion/codegen/cache | eager/compiled model equivalence and debug | M7 | I0 |
| Ahead-of-time deployment | export contract, stable artifact, generated/native runner, version compatibility | reduced AOT package or executable plan | M7, M9 | I1 |
| PrivateUse Route A | MiniTorch device/plugin ABI, runtime, kernels, fallback, compiler and conformance | CPU mock plus private hardware command bundle | M8 | I0 |
| PrivateUse Route B | native PyTorch `PrivateUse1`, OpenReg-like OOT package and public hooks | mock/proxy package and tests | M8 | I0 |
| Compatibility/performance | supported matrix, errors/fallback, correctness, memory, concurrency, latency/throughput/startup, upgrade | inference capstone report and delayed maintenance task | M9 | I0 |
| Source engineering | Git/history, generated-vs-source, test selection, debugging, logging, review and change isolation | evidence from every milestone | M0–M9 | I0 |

## Learning-path dependency audit

The optimized spiral order is:

```text
M0a fast native import → M0b local development/test loop
 → M2.5 Release-A contiguous-FP32 CPU model walking skeleton
   → M1 Tensor/Storage + numerical depth
     → M2 schema/codegen/dispatcher + CPU hardening of the same model
       → M0c advanced native debugging/package inspection
         → M3 CUDA kernels + memory/streams
         → M4 nn + CNN/Transformer inference semantics
         → M5 minimal Autograd/training boundary
         → M6 runtime/profiler + distributed inference DP/TP
           → M7 graph/compiler/AOT inference
             → M8 dual PrivateUse backends + conformance
               → M9 packaging/CI/model compatibility capstone
```

Reasons for this order:

- M0 prevents C++ and build mechanics from blocking every later source lesson.
- M0a provides a native success quickly; M0b proves only the local development loop, while release-wheel work remains in M9.
- M2.5 first provides a deliberately restricted CPU model within 30–50 cumulative hours, then M1/M2 replace its recorded shortcuts before CUDA.
- Basic pybind module/ownership concepts appear at first use; M0c owns advanced GIL, exception, ABI, RPATH, debugger and sanitizer depth.
- Tensor/numerics precede dispatcher/kernels so operators have explicit invariants.
- CPU establishes semantics and debugging before CUDA adds asynchronous state.
- Real model slices start only after storage, dispatch and kernels exist.
- Minimal Autograd follows eager inference primitives and remains a bounded boundary study.
- Distributed TP depends on model operators, device runtime and collectives.
- Compiler depends on eager semantics, mutation/view rules and representative models.
- PrivateUse integrates all prior contracts and therefore belongs after eager/compiler/runtime foundations.
- Packaging and compatibility close the project only after clean rebuild and model evidence are possible.

## Scope controls

- Target 20–30 operator schemas and 10–15 backend-native kernels; use correct composite decomposition for higher APIs.
- Keep one pointwise, one reduction, one view/mutation, one matrix, one convolution and one attention vertical slice as recurring examples.
- Implement CNN and a small decoder block, not full model zoos.
- Implement two-process DP/TP; treat larger-scale algorithms and topology tuning as I2.
- Implement one reduced caching allocator, compiler and collective runtime; do not reproduce production schedulers or every optimization.
- Implement one quantized Linear path; sample additional quantization modes, TorchScript, ONNX, ExecuTorch/mobile, sparse/nested, FSDP, RPC, PP/CP/EP and platform backends as I1/I2 extensions. Promote one only when the capstone or target hardware requires it.
- Keep production security, release and governance topics at architectural awareness unless they affect package loading, model serialization or ABI compatibility.

## Gate against omissions

`curriculum/COVERAGE_MATRIX.csv` maps every mastery concept to a priority, declared milestone, inspected PyTorch path, named source symbol/ownership point, learner deliverable and required evidence dimensions. `curriculum/COURSE_PRACTICE_MAP.csv` additionally maps each concept to an ordered course, immediate learner-owned MiniTorch action and runnable evidence. `scripts/validate_curriculum_coverage.py` rejects missing/extra concepts, invalid or reordered courses, absent immediate practice, undeclared milestones, nonexistent paths, malformed symbol entries and weak I0/F0/I1/T1 evidence plans. `scripts/system_health_check.py` runs positive and negative checks before simulating a manifest-driven project learning session with explicit practice and authorship provenance.

`curriculum/COURSE_PRACTICE_MAP.csv` is also the sole authority for course
titles, release, hours and dependency order. `scripts/sync_course_plan.py`
renders the public tables and the validator rejects stale generated output or a
Release A that no longer reaches CPU-model evidence within 50 hours.
