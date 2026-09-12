# MiniTorch implementation roadmap

MiniTorch is the assessment spine for every phase. The stable scope and dependency policy live in [MINITORCH_SPEC.md](MINITORCH_SPEC.md); the inference-first feature matrix and pinned-PyTorch anchors live in [INFERENCE_SCOPE.md](INFERENCE_SCOPE.md). Calendar estimates are planning aids; a milestone advances only after its quality gate passes.

Each milestone is split into session-sized increments. Before an increment, the learner writes the design or patch plan and expected tests. The mentor may create only the minimum scaffolding needed to expose the learning task. After implementation, assessment uses the diff, focused tests, debugging evidence, PyTorch comparison and an unassisted code defense.

## M0 — Repository, architecture and build/import loop

Goal: create an independent `mini-torch/` Git repository and understand how source becomes an installable Python package with a native extension.

Increments:

1. learner-authored map from PyTorch directories to the reduced MiniTorch layout;
2. repository initialization, ignore policy, README and architecture decision record;
3. `pyproject.toml`, setuptools bridge and isolated development environment;
4. root/subdirectory CMake targets and one C++ library;
5. pybind11 module exposed as `minitorch._C` and imported by `minitorch`;
6. pytest, CTest and build/install/import smoke commands.

Gate: from a clean build directory, an editable install and wheel install can call one native function. The learner explains Python import, compile, object/library, link, extension-module loading, CMake target flow, build isolation and why the MiniTorch layout differs at `torch/ → minitorch/`. No Tensor implementation is required yet.

## M1 — C10 foundations, Storage and CPU Tensor

Goal: build the minimum ownership and metadata model needed by later operators.

Increments:

1. `ScalarType`, `DeviceType`, `Device`, error/check utilities;
2. allocator and `DataPtr`-like ownership boundary;
3. `StorageImpl`, lifetime and shared ownership;
4. `TensorImpl` sizes, strides, storage offset, dtype and device;
5. lightweight Tensor handle and pybind11 ownership/lifetime policy;
6. construction, indexing, contiguous copy, reshape/view/clone and representation.

Gate: positive, alias/mutation, lifetime, shape/stride, overflow and error tests pass. NumPy/PyTorch oracle tests confirm the supported behavior. The learner diagnoses one ownership or stride bug and explains the corresponding PyTorch source anchors and intentional omissions.

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

Required representative slices: an elementwise op, a view-like op, a reduction and a matrix/linear op.

Gate: generated files are reproducible; manual and generated paths have tests; registration lifetime and duplicate/missing kernel errors are covered; runtime evidence identifies the chosen CPU kernel. The learner transfers the pattern to one small unpracticed operator.

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
9. naive versus cuBLAS backend and FP32/FP16/BF16 policy for supported ops;
10. static CUDA Graph capture/replay as an I1 optimization;
11. benchmark protocol with warmup, synchronization, memory metrics and CPU/oracle comparison.

Gate: CPU-only builds remain valid; CUDA positive and error cases pass when the environment is available; focused failures demonstrate fragmentation/OOM, cross-stream premature reuse and misleading unsynchronized timing. The learner explains host/device code, allocation versus reservation, pinned transfer, kernel launch, stream/event dependency, memory lifetime, dispatch and precision selection. CUDA Graph work may remain I1, but allocator/stream correctness is required. CUDA claims stay unverified if prerequisites are unavailable.

## M4 — Python frontend, `nn` and inference state

Goal: turn the native core into a usable small inference framework.

Increments:

1. Python `Tensor` API boundary and operator exposure;
2. `Module.__call__/forward`, submodule, Parameter and buffer registration;
3. `Linear`, activations, `Sequential`, Flatten, Conv2d, pooling and inference BatchNorm for the target CNN;
4. Embedding, LayerNorm, GELU, Softmax, masking and naive scaled dot-product attention for a decoder-style Transformer block;
5. KV-cache prefill/decode shape, update and lifetime behavior;
6. `state_dict`, versioned serialization, load validation and device/dtype restoration;
7. `eval`, `no_grad`, inference-mode-like state and an autocast/mixed-precision policy;
8. hooks or override mechanism as a small explicit subset;
9. channels-first versus one channels-last path, batching and dynamic batch/sequence cases.

Gate: a small CNN and decoder-style Transformer block run in eager inference on supported CPU/CUDA dtypes with oracle parity, save/load round trips, KV-cache prefill/decode, mode/precision distinctions and negative tests. The learner traces one CNN op and one attention/Linear path from Python `Module` through dispatcher to selected kernels.

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
8. mixed-precision and TP graph behavior for the supported inference subset;
9. optional static CUDA Graph replay after compiled shapes and allocation addresses are stable.

Gate: the target MLP/CNN inference subset executes through the compiler backend; logs show capture, guards, lowering and kernel selection; unsupported graphs fail or fall back according to the documented policy. The learner debugs one incorrect graph transformation.

## M8 — Simulated device and backend integration

Goal: integrate a new device-like backend and separate eager and compiler responsibilities.

Increments:

1. device registration, allocator and device guard contract;
2. supported kernel registration and explicit unsupported matrix;
3. fallback/redispatch and error reporting policy;
4. serialization, RNG and stream/event capability decisions;
5. compiler partition/lowering for the supported simulated device subset;
6. versioned compatibility tests.

Gate: positive, unsupported, fallback and mixed-graph cases pass; no test claims real proprietary hardware validation. The learner defends ownership of allocation, selection, lowering, execution, synchronization and errors.

## M9 — Packaging, CI and inference capstone

Goal: prove that the project is installable, testable and understandable as an engineering system.

Increments:

1. clean wheel build and isolated installation;
2. CPU-required and CUDA-conditional CI matrices;
3. reproducible generated-source checks, formatting/static checks and focused test layers;
4. ABI/API/versioning and upgrade notes;
5. final minimal MLP training/gradient-sync boundary;
6. CPU/CUDA CNN and Transformer/KV-cache inference in eager and compiled modes;
7. full/mixed-precision and unsharded/inference-DP/TP comparisons;
8. allocator fragmentation/OOM, stream/event lifetime and optional CUDA Graph demonstrations;
9. simulated-device and clean-wheel-install demonstrations;
10. correctness, latency, throughput, peak allocated/reserved memory, transfer, communication and compile/startup report.

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
