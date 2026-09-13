# MiniTorch implementation roadmap

MiniTorch is the assessment spine for every phase. The stable scope and dependency policy live in [MINITORCH_SPEC.md](MINITORCH_SPEC.md); the inference-first matrix lives in [INFERENCE_SCOPE.md](INFERENCE_SCOPE.md); dual hardware integration lives in [PRIVATEUSE_BACKEND_SPEC.md](PRIVATEUSE_BACKEND_SPEC.md); the full knowledge audit lives in `curriculum/COVERAGE_AUDIT.md`. Calendar estimates are planning aids; a milestone advances only after its quality gate passes.

Each milestone is split into session-sized increments. Before an increment, the learner writes the design or patch plan and expected tests. The mentor may create only the minimum scaffolding needed to expose the learning task. After implementation, assessment uses the diff, focused tests, debugging evidence, PyTorch comparison and an unassisted code defense.

## Depth and capacity policy

Every numbered increment is assigned one delivery depth:

- **Core (C):** required runnable mechanism; blocks the local gate.
- **Representative (R):** one executable case that proves a broader mechanism without reproducing production breadth.
- **Survey (S):** pinned-source location plus a focused official-PyTorch experiment; it does not add MiniTorch surface unless a target model requires it.

The depth line under each milestone assigns every increment. Do not silently turn an S item into implementation work. A normal increment is timeboxed to roughly 4–10 focused learner hours for C, 3–8 for R and 1–3 for S; debugging may extend a gate when it exposes a real prerequisite.

| Milestone | Planning range | First useful outcome |
|---|---:|---|
| M0 | 35–55 h | M0a imports one native function |
| M1 | 45–70 h | CPU Tensor owns real storage |
| M2 | 55–90 h | schema-dispatched CPU operator |
| M2.5 | 15–25 h | first CPU model inference |
| M3 | 65–105 h | real CUDA execution/runtime slice |
| M4 | 65–100 h | CNN and decoder inference frontend |
| M5 | 35–55 h | minimal Autograd/MLP boundary |
| M6 | 70–110 h | profiler plus two-rank DP/TP |
| M7 | 65–105 h | compiled inference and AOT slice |
| M8 | 90–150 h | dual PrivateUse contract-ready routes |
| M9 | 40–65 h | clean package and capstone |

The total planning range is approximately 580–930 focused hours. At 20 hours per week this is 29–47 active study weeks; with work interruptions and delayed reviews, 9–18 calendar months is realistic. Gates and evidence determine progress, not the estimate.

## M0 — Repository, architecture and staged build/import loop

Goal: create an independent `mini-torch/` Git repository and understand how source becomes an installable Python package with a native extension.

### M0a — Fast native-import success

1. learner-authored map from PyTorch directories to the reduced MiniTorch layout;
2. repository initialization, ignore policy, README and one architecture decision record;
3. minimal root/subdirectory CMake target producing one C++ library;
4. pybind11 module exposed as `minitorch._C`, imported by `minitorch`, with one native smoke test.

Depth: C = 1–4. Gate: a clean local build can run `import minitorch` and call one native function. The learner explains the repository boundary, source→object/library→extension path and staged diff. M0a is the Foundation Gate and unlocks M1.

### M0b — Package and test loop

5. `pyproject.toml`, setuptools bridge and isolated development environment;
6. pytest, CTest and explicit build/install/import commands;
7. editable install plus clean wheel build/install smoke.

Depth: C = 5–7. Gate: editable and wheel installs work in isolated environments; pytest and CTest each exercise the native boundary. M0b must pass before M2 code generation expands the build graph.

### M0c — Native boundary and debugging clinic

8. Python↔C++ conversion, ownership and exception translation;
9. one GIL-release concurrency case;
10. ABI/RPATH inspection, debug symbols, native stack trace, logging, `compile_commands.json`, sanitizer and linter entry points.

Depth: R = 8–10. Gate: a translated exception and GIL case pass, and one symbolized native failure is located. M0c may interleave with M1 and M2, but must pass before M3 introduces asynchronous CUDA failures.

## M1 — C10 foundations, Storage and CPU Tensor

Goal: build the minimum ownership and metadata model needed by later operators.

Increments:

1. `ScalarType`, `DeviceType`, `Device`, error/check utilities;
2. allocator and `DataPtr`-like ownership boundary;
3. `StorageImpl`, lifetime and shared ownership;
4. `TensorImpl` sizes, strides, storage offset, dtype and device;
5. lightweight Tensor handle and pybind11 ownership/lifetime policy;
6. construction, indexing, contiguous copy, reshape/view/clone and representation.
7. scalar types, promotion, broadcasting, accumulation dtype and conversion policy;
8. NaN/Inf/overflow/tolerance, RNG seed/state and deterministic-behavior tests for the supported subset.

Depth: C = 1–8.

Gate: positive, alias/mutation, lifetime, shape/stride, promotion/broadcasting, numerical edge, determinism and error tests pass. NumPy/PyTorch oracle tests confirm the supported behavior with dtype-appropriate tolerances. The learner diagnoses one ownership/stride and one numerical-contract bug and explains corresponding PyTorch source anchors and intentional omissions.

## M2 — Schema, code generation, dispatcher and CPU kernels

Goal: implement one full eager operator lifecycle rather than calling C++ methods directly.

Increments:

1. reduced operator schema and YAML parser;
2. generated declarations, wrappers or registration source;
3. operator name/overload, dispatch key/set and registration handles;
4. dispatcher table, lookup, backend fallback and redispatch boundary;
5. CPU elementwise kernels, then reduction and matrix operation;
6. dtype/device/layout checks and a minimal TensorIterator-like loop abstraction;
7. Python API generated/manual binding comparison.
8. CPU thread control, parallel loop and one vectorized kernel after the scalar reference;
9. BLAS/oneDNN-style external-library boundary for one matrix or convolution path;
10. one out-of-tree custom operator with schema, fake/meta, alias/mutation and conformance tests.

Depth: C = 1–9; R = 10.

Required representative slices: an elementwise op, a view-like op, a reduction and a matrix/linear op.

Gate: generated files are reproducible; manual and generated paths have tests; registration lifetime and duplicate/missing kernel errors are covered; runtime evidence identifies the chosen scalar/parallel/vector/library CPU path. Thread-count and benchmark evidence are reproducible. The learner transfers the pattern to one small unpracticed operator and can distinguish built-in from out-of-tree custom registration.

## M2.5 — First CPU inference vertical slice

Goal: produce an early, motivating end-to-end model before CUDA and the full `nn` surface.

Increments:

1. minimal Python `Tensor`, `Module`, Parameter and `Linear` wrappers over the existing native core;
2. deterministic `Linear → ReLU → Linear` inference using the M2 dispatcher and CPU kernels;
3. import-to-kernel trace, shape/error tests and official-PyTorch or NumPy oracle parity;
4. minimal state save/load round trip for this model;
5. pinned-source comparison with `Module._call_impl`, `Linear.forward` and the corresponding native operator path.

Depth: C = 1–3; R = 4; S = 5.

Gate: a clean CPU environment runs the tiny model and reproduces oracle outputs. The learner traces Python module call → binding → dispatcher → CPU kernel, diagnoses one seeded shape or registration failure and explains which M4 behaviors remain intentionally absent. M2.5 passes before M3 starts.

## M3 — CUDA backend and runtime boundary

Goal: add real CUDA execution without hiding synchronization and device ownership.

Increments:

1. CUDA build detection and conditional targets;
2. raw CUDA allocator/device guard/error checking, then a reduced caching allocator;
3. allocated/reserved statistics, reuse/split, deterministic fragmentation and OOM diagnostics;
4. pinned host allocation plus blocking/non-blocking transfer contracts;
5. elementwise and reduction or matrix CUDA kernels;
6. dispatcher registration for CUDA;
7. current/default streams, events, asynchronous launch and explicit synchronization tests;
8. allocator/stream lifetime and a `record_stream`-like contract;
9. CUDA execution clinic: grid/block mapping, coalescing, shared memory, reductions, atomics, occupancy and launch-resource reasoning on representative kernels;
10. naive versus cuBLAS/cuDNN-style library path, handle/workspace/algorithm selection and FP32/FP16/BF16 policy for supported ops;
11. static CUDA Graph capture/replay as an I1 optimization;
12. benchmark protocol with warmup, synchronization, memory metrics and CPU/oracle comparison.

Depth: C = 1–10 and 12; R = 11.

Gate: CPU-only builds remain valid; CUDA positive and error cases pass when the environment is available; focused failures demonstrate fragmentation/OOM, cross-stream premature reuse and misleading unsynchronized timing. The learner explains host/device code, allocation versus reservation, pinned transfer, kernel launch, stream/event dependency, memory lifetime, dispatch and precision selection. CUDA Graph work may remain I1, but allocator/stream correctness is required. CUDA claims stay unverified if prerequisites are unavailable.

## M4 — Python frontend, `nn` and inference state

Goal: turn the native core into a usable small inference framework.

Increments:

1. Python `Tensor` API boundary and operator exposure;
2. `Module.__call__/forward`, submodule, Parameter and buffer registration;
3. `Linear`, activations, `Sequential`, Flatten, Conv2d, pooling and inference BatchNorm for the target CNN;
4. Embedding, LayerNorm, GELU, Softmax, masking and naive scaled dot-product attention for a decoder-style Transformer block;
5. KV-cache prefill/decode shape, update and lifetime behavior;
6. `state_dict`, versioned serialization, safe load validation, device/dtype restoration and one rank-local sharded-load case;
7. `eval`, `no_grad`, inference-mode-like state and an autocast/mixed-precision policy;
8. hooks or override mechanism as a small explicit subset;
9. channels-first versus one channels-last path, batching and dynamic batch/sequence cases;
10. one weight-only or int8 Linear path covering scale/zero-point, packing, unsupported cases and float-oracle tolerance;
11. input/preprocessing boundary with pinned transfer and repeated-request state isolation.

Depth: C = 1–7, 9 and 11; R = 8 and 10.

Gate: a small CNN and decoder-style Transformer block run in eager inference on supported CPU/CUDA dtypes with oracle parity, save/load round trips, KV-cache prefill/decode, mode/precision distinctions, one representative quantized Linear and negative tests. The learner traces one CNN op and one attention/Linear path from Python `Module` through dispatcher to selected kernels.

## M5 — Autograd with an inference-first boundary

Goal: understand training machinery only deeply enough to reason about inference obligations, mutation safety and distributed boundaries.

Increments:

1. `requires_grad`, edge/Node and reverse topological execution;
2. generated or registered backward formulas for the minimal op subset;
3. saved values, accumulation and leaf behavior;
4. version counter and in-place/view safety;
5. `no_grad` and inference-mode-like behavior;
6. minimal SGD and one small MLP training smoke case;
7. one two-rank gradient all-reduce used later to contrast minimal DDP with inference DP.

Depth: C = 1–7. This is required T1 boundary work even though its implementation breadth remains deliberately small.

Gate: gradient checks pass for the supported subset, seeded in-place/version failures are diagnosed, and the learner compares normal, no-grad and inference behavior. Training breadth stops after the MLP smoke and gradient-sync boundary. Optimizer families, GradScaler, full DDP reducer/FSDP and training-performance work remain T2 until the inference capstone is complete.

## M6 — Runtime, observability and distributed inference

Goal: expose the runtime state that inference and backend integration depend on.

Increments:

1. allocator statistics and lifetime instrumentation;
2. thread pool or parallel CPU loop, thread-local modes and guards;
3. RNG and serialization interaction;
4. minimal event profiler with nested scopes;
5. local two-process rendezvous, process group and asynchronous `Work`-like handle;
6. broadcast, all-reduce, all-gather and reduce-scatter with timeout, mismatch and process-failure errors;
7. 1D DeviceMesh plus `Replicate`/`Shard(dim)` distributed-tensor metadata and redistribution;
8. inference DP: replicated weights, input partition, weight broadcast and output reconstruction;
9. minimal DDP gradient all-reduce contrast from M5, with no full reducer implementation;
10. column-parallel and row-parallel Linear with the appropriate collectives;
11. a two-rank TP Transformer/MLP slice and unsharded oracle comparison;
12. asynchronous communication/computation overlap using streams/events when multi-GPU CUDA is available;
13. rank-local sharded checkpoint metadata and load for TP inference;
14. source-level comparison of sequence/context/pipeline/expert parallel, implemented only if the capstone requires it.

Depth: C = 1–11; R = 12–13; S = 14.

Gate: profiling and allocator evidence explain a model run; concurrency tests are reproducible; collectives pass positive and negative cases; inference DP and row/column TP reconstruct unsharded results across two local ranks. The learner explains ProcessGroup/Work, DeviceMesh/placement, DP versus DDP versus TP, collective choice, shard shapes and MiniTorch simplifications of c10d/DTensor/tensor parallel. Multi-GPU NCCL overlap/performance remains explicitly unverified when fewer than two GPUs are available.

## M7 — Graph IR, capture and compiler backend

Goal: implement a small inference compiler path and understand its ownership boundaries.

Increments:

1. graph/Node/value IR and metadata;
2. capture or tracing of the supported Python/module subset;
3. fake/meta shape and dtype propagation;
4. graph validation, unsupported op and graph-break policy;
5. decompositions, mutation/view normalization and simple optimization such as constant folding or fusion;
6. lowering to an executable plan and cache/guard/recompile contract;
7. eager-versus-compiled equivalence with dynamic batch and sequence-length tests;
8. mixed-precision, representative quantized Linear lowering and TP graph behavior for the supported inference subset;
9. optional static CUDA Graph replay after compiled shapes and allocation addresses are stable.
10. reduced export/AOT artifact plus a clean native or Python runner with explicit version contract;
11. one Triton or generated-kernel source inspection/experiment without making it a runtime dependency of MiniTorch core.

Depth: C = 1–8; R = 9–10; S = 11.

Gate: the target CNN and decoder-Transformer inference subset executes through the compiler backend; logs show capture, guards, lowering and kernel selection; dynamic batch/sequence and reduced AOT artifact cases pass; unsupported graphs fail or fall back according to the documented policy. The learner debugs one incorrect graph transformation.

## M8 — Dual PrivateUse backend and hardware conformance

Goal: make MiniTorch pluggable on a private third-party runtime and separately build a native PyTorch `PrivateUse1` out-of-tree reference adapter. Follow `PRIVATEUSE_BACKEND_SPEC.md`; do not claim real hardware success from mock tests.

Increments:

1. learner-authored versioned C adapter ABI with opaque handles, feature flags, status/error boundary and capability query;
2. MiniTorch plugin loader, ABI negotiation and CPU mock/fault-injection adapter;
3. MiniTorch `PrivateUse` device registration, allocator/pinned allocator, guard, copy, stream/event and lifetime contract;
4. MiniTorch kernel registry, factory/copy ops, selected kernels, decomposition/fallback and explicit unsupported matrix;
5. MiniTorch autocast, RNG, serialization, profiler and optional distributed capabilities;
6. MiniTorch compiler partition/lowering/execute path for the supported private device subset;
7. native PyTorch OOT package: autoload/rename/device module, `C10_REGISTER_GUARD_IMPL`, hooks, allocators and Storage/Tensor factories;
8. native `TORCH_LIBRARY_IMPL` operators/fallback, `AutogradPrivateUse1`, `AutocastPrivateUse1`, Meta/Fake, RNG, serialization, profiler and stream/event;
9. native custom `torch.compile` backend and optional process group for the supported model slice;
10. shared capability manifest and contract suite against both mock routes;
11. sanitized command bundle for the learner's private real-adapter device-smoke and model verification;
12. versioned ABI/PyTorch compatibility and upgrade tests.

Depth: C = 1–12; the optional distributed clauses inside 5 and 9 are R unless the target hardware capability makes them necessary. The P0–P5 gates in `PRIVATEUSE_BACKEND_SPEC.md` control progression inside M8.

Gate: Route A MiniTorch PrivateUse and Route B native PyTorch `PrivateUse1` both pass mock/proxy contract-ready tests. ABI mismatch, missing capability, allocation/copy, stream/event lifetime, operator/fallback, autocast, serialization/profiler and compiled-graph cases are covered. The learner defends ownership of allocation, selection, lowering, execution, synchronization and errors. Real-device success is awarded only after the private adapter passes sanitized device-smoke and representative-model gates.

## M9 — Packaging, CI and inference capstone

Goal: prove that the project is installable, testable and understandable as an engineering system.

Increments:

1. clean wheel build and isolated installation;
2. CPU-required and CUDA-conditional CI matrices;
3. reproducible generated-source checks, formatting/static checks and focused test layers;
4. curriculum coverage validator proving every mastery concept maps to a milestone and inspected source anchor;
5. ABI/API/versioning and upgrade notes;
6. final minimal MLP training/gradient-sync boundary;
7. CPU/CUDA CNN, Transformer/KV-cache and representative quantized Linear inference in eager and compiled modes;
8. full/mixed-precision and unsharded/inference-DP/TP comparisons;
9. allocator fragmentation/OOM, stream/event lifetime and optional CUDA Graph demonstrations;
10. MiniTorch PrivateUse and native PyTorch PrivateUse1 mock/proxy demonstrations plus private hardware command bundle;
11. clean-wheel-install and reduced AOT artifact demonstrations;
12. correctness, latency, throughput, peak allocated/reserved memory, transfer, communication and compile/startup report.

Depth: C = 1–10 and 12; R = 11.

Gate: the learner rebuilds the architecture map from their implementation, traces one unpracticed eager op and one model path, repairs a seeded defect without a supplied location, and completes a delayed transfer task. The wheel works in a clean environment and all conclusions distinguish observed reference behavior, MiniTorch behavior and unverified scope.

## Common quality gate for every increment

- The MiniTorch base revision and resulting diff/commit are recorded separately from the PyTorch reference revision.
- The learner wrote the decisive code; mentor scaffolding and hints are identified.
- The public contract, supported subset, invariants and error behavior are explicit before implementation.
- Relevant positive, boundary and negative tests pass; an oracle test is used where meaningful.
- A failing test is investigated rather than patched by guesswork.
- At least one current PyTorch source location is inspected and its role is compared without copying production complexity blindly.
- The learner gives an unassisted code defense and names simplifications and limitations.
- A later extension, repair or review is scheduled to test retention and transfer.

## Four-week scope review

After every four active learning weeks or 20 substantive sessions, whichever comes first, pause new scope for one short review using `templates/SCOPE_REVIEW.md`. Check the operator/schema/kernel budgets, unfinished Core work, time spent on administration, target-model needs and active blockers. Remove or demote work that neither enables the CNN/decoder/PrivateUse capstone nor teaches a new mechanism. Scope review changes sequencing and C/R/S depth; it never awards mastery by itself.
