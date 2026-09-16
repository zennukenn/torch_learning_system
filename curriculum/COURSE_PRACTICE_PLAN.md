# Project-integrated PyTorch source curriculum

This file is the learner-facing course index. `projects/ROADMAP.md` remains the
authoritative milestone specification, `curriculum/COVERAGE_MATRIX.csv` remains
the concept/source/evidence audit, and `COURSE_PRACTICE_MAP.csv` is the
machine-validated bridge from knowledge to immediate MiniTorch work.

## Non-negotiable lesson unit

Every lesson uses one or more short project cycles:

```text
place the topic in the inference map
  -> teach only the prerequisite needed for the next edit
  -> learner immediately authors a MiniTorch file/config/test/change
  -> inspect the real diff
  -> predict and run the narrowest verification
  -> debug the actual result
  -> compare one responsibility with pinned PyTorch source
  -> brief defense of the work just completed
```

The mentor may create mechanical scaffolding only when it leaves the learning
decision and decisive logic to the learner. A mentor-created README, ADR,
configuration, implementation, test output, or explanation is labeled mentor
work and cannot raise mastery. Diagnostics are limited to one opening set of at
most three short questions; an incomplete oral answer changes how the next
project step is taught, but does not start a repeated quiz loop.

## Inference from upper layer to hardware

The stable map below is introduced at M0 and revisited through executable
vertical slices. It is a responsibility map rather than a claim that every
request passes through one fixed call chain.

```text
request / input / preprocessing
  -> Python package and model API
  -> Module state: parameters buffers eval hooks serialization
  -> Tensor semantics: shape stride dtype device layout view alias ownership
  -> operator API and schema / generated or manual binding
  -> eager Dispatcher: key selection registration fallback redispatch
  -> backend implementation: composite native CPU CUDA or PrivateUse kernel
  -> runtime: allocation threads libraries device guard streams events RNG
  -> hardware execution and synchronization
  -> output Tensor / postprocessing / correctness check

Cross-cutting branches:
  Autograd and version/mutation rules -- required inference boundary
  autocast and inference modes       -- state and dispatch policy
  compiler                           -- capture guards decomposition lowering cache
  distributed inference             -- replicas shards collectives and reconstruction
  observability/deployment           -- profiler memory serialization wheel AOT CI
```

The course uses a spiral rather than a lecture-first or strictly bottom-up
sequence. Release A builds a deliberately narrow contiguous-FP32 walking
skeleton, including a real CPU model, before the framework internals are wide.
Release B then replaces its temporary assumptions with durable Tensor,
Dispatcher, CPU/CUDA runtime and model contracts. Release C adds the remaining
source-mastery and accelerator-integration depth. Temporary shortcuts are
listed and removed by a later gate; they are never presented as final design.

## Course sequence

`COURSE_PRACTICE_MAP.csv` is the authoritative structured source for order,
hours, dependencies, knowledge ownership and outcomes. The table below is
generated; update the CSV and run `scripts/sync_course_plan.py --write`.

<!-- GENERATED COURSE TABLE START -->
| Course | Milestone | Knowledge taught immediately before use | Learner-owned MiniTorch outcome | Gate evidence |
|---|---|---|---|---|
| C00 Architecture and native bootstrap | M0a | Inference panorama repository boundaries Git Python import compile link CMake and a basic pybind11 module | Create the independent repository then author its architecture map README ignore policy ADR CMake target and first native module | Git boundary checks plus a clean native import and learner explanation prove the source-to-extension path |
| C01 Development build and tests | M0b | CMake target graph editable development install pytest and CTest without release packaging | Author the reproducible local configure build editable-install pytest and CTest entry points | A fresh development environment configures builds imports and passes both focused test layers |
| C02 First CPU inference walking skeleton | M2.5 | A deliberately narrow contiguous FP32 Tensor plus manual add ReLU matmul and minimal Module Parameter Linear frontend | Implement and run Linear ReLU Linear through the native extension while recording every temporary restriction | The first CPU model matches an oracle within 30 to 50 cumulative hours and its temporary direct boundaries are explicit |
| C03 Tensor Storage and numerics depth | M1 | Allocator Storage Tensor metadata ownership views dtype promotion broadcasting and numerical contracts | Replace walking-skeleton assumptions with the real CPU Tensor and adversarial lifetime alias numerical and determinism tests | Native and Python tests prove ownership stride mutation promotion tolerance and deterministic supported behavior |
| C04 Operator lifecycle and CPU hardening | M2 | Schema codegen Dispatcher CPU kernels parallelism vectorization libraries custom registration and model state | Route the walking-skeleton model through generated schemas and Dispatcher then add reduction view custom-op state round-trip and error paths | Reproducible generation dispatch traces CPU path evidence model parity serialization and positive boundary negative tests pass |
| C05 Native debugging and packaging clinic | M0c | Advanced pybind11 lifetime exception GIL ABI RPATH symbols debugger sanitizer and package inspection | Extend the working model boundary with conversion exception and GIL cases then diagnose one symbolized native failure | Import error concurrency symbol RPATH sanitizer debugger and package evidence identify the actual boundary before CUDA |
| C06 CUDA execution and runtime | M3 | CUDA build kernels allocator pinned transfer streams events libraries precision and measurement | Implement real CUDA execution plus one reproducible allocator stream-lifetime failure and repair | CPU-only build remains valid while CUDA correctness memory synchronization error and benchmark evidence pass where hardware exists |
| C07 Model inference semantics | M4 | Python nn state CNN decoder attention KV cache modes autocast layouts batching and representative quantization | Implement CPU-first CNN and decoder slices then add CUDA mode precision cache and quantized paths | Model parity save-load mode precision dynamic shape cache lifetime and explicit unsupported tests pass |
| C08 Autograd inference boundary | M5 | Reverse-mode Autograd and the inference mutation and mode boundary | Implement the minimal backward formulas version checks SGD MLP smoke and one gradient all-reduce boundary | Gradient checks and seeded in-place failures pass while no-grad and inference behavior remain separately explained |
| C09 Runtime and distributed inference | M6 | Runtime observability process groups collectives DeviceMesh placements inference DP and row column TP | Implement profiling plus two-process collectives DP and TP model slices with failure cases | Per-rank shape collective reconstruction timeout profiler and unsharded-oracle evidence pass |
| C10 Compiler and AOT inference | M7 | Graph IR capture fake symbolic shape guards decomposition lowering fusion cache and reduced AOT | Implement a supported graph compiler for the existing models and debug one wrong transformation | Eager compiled and AOT equivalence dynamic guard recompile fallback and generated-plan evidence pass |
| C11 Dual accelerator integration | M8 | MiniTorch PrivateUse C ABI and native PyTorch PrivateUse1 eager compiler runtime and package contracts | Implement both CPU-backed routes gate by gate with capability negotiation fault injection and shared conformance tests | P0 through P5 mock or proxy evidence passes and real hardware claims remain explicitly gated |
| C12 Deployment and full capstone | M9 | Release wheel CI compatibility upgrades and the complete inference capstone | Build a release-grade clean wheel and defend CPU CUDA eager compiled full mixed DP TP and PrivateUse model results | Fresh-install correctness latency throughput memory transfer communication startup and compatibility evidence is reproducible |
<!-- GENERATED COURSE TABLE END -->

`COURSE_PRACTICE_MAP.csv` assigns every mastery concept to its first accountable
course. Concepts are then revisited in later slices; the single assignment is an
audit device, not a claim that knowledge is learned once.

## Capacity and gate order

These are planning ranges rather than deadlines. C00 and C01 establish basic
pybind and local development packaging; advanced lifetime/GIL/ABI debugging is
deliberately revisited at C05. C01 does not duplicate C12: the former proves a
local editable development loop, while the latter owns the release-grade wheel,
CI, ABI and upgrade contract.

<!-- GENERATED CAPACITY TABLE START -->
| Course | Focused hours | Dependency/gate | Release |
|---|---:|---|---|
| C00 M0a | 6–10 | none | A |
| C01 M0b | 6–10 | C00 | A |
| C02 M2.5 | 18–30 | C01 | A |
| C03 M1 | 27–40 | C02 | B |
| C04 M2 | 45–75 | C03 | B |
| C05 M0c | 15–20 | C04 | B |
| C06 M3 | 65–105 | C05 | B |
| C07 M4 | 65–100 | C06 | B |
| C08 M5 | 35–55 | C07 | C |
| C09 M6 | 70–110 | C08 | C |
| C10 M7 | 65–105 | C09 | C |
| C11 M8 | 90–150 | C10 | C |
| C12 M9 | 40–65 | C11 | C |
<!-- GENERATED CAPACITY TABLE END -->

## Product releases and time to value

Every release is independently useful. Release A is a walking skeleton, not a
claim that Tensor or Dispatcher depth is complete. All previously accepted
knowledge remains in Releases B and C.

<!-- GENERATED RELEASE TABLE START -->
| Release | Independently useful outcome | Courses | Increment hours | Cumulative hours |
|---|---|---|---:|---:|
| A | Working CPU inference | C00–C02 | 30–50 | 30–50 |
| B | Robust eager inference engine | C03–C07 | 217–340 | 247–390 |
| C | Full source and backend mastery | C08–C12 | 300–485 | 547–875 |
<!-- GENERATED RELEASE TABLE END -->

At roughly 20 focused hours per week the full 547–875 hour path is about 27–44
active weeks; interruptions and delayed retention checks still make 9–18
calendar months realistic. Evidence gates rather than elapsed time control
advancement.

## Inference priority and retained training scope

- I0 mechanisms must be runnable and defended before unrelated breadth is
  added: Tensor/numerics, CPU/CUDA execution, model state and modes, CNN and
  decoder/KV cache, memory/streams, mixed precision, dynamic shapes, compiler,
  inference DP/TP, deployment, compatibility, performance, and both PrivateUse
  routes.
- I1 implements one representative case where production breadth would add
  scale rather than a new mechanism: quantized Linear, CUDA Graph, custom op,
  communication overlap, and reduced AOT packaging.
- I2 remains source map plus focused official-PyTorch experiment unless a target
  model needs it.
- T1 keeps minimal reverse-mode Autograd, SGD, a small MLP, version/mutation
  safety, and one gradient all-reduce boundary. Optimizer families, full DDP
  reducer/FSDP, and training-performance work remain T2 until the inference
  capstone passes.

## How mastery is inferred

The system first inspects what the learner actually changed and ran. It scores
separate dimensions only when the evidence supports them:

- `explain`: defend the implemented contract and invariant;
- `locate`: find the corresponding MiniTorch and pinned PyTorch ownership;
- `trace`: reconstruct an observed build/runtime path;
- `debug`: form and test a hypothesis on a reproducible failure;
- `modify`: author decisive code/config/tests;
- `transfer`: extend the mechanism without replaying the solution;
- `retain`: repeat a repair or extension after a delay.

An opening diagnostic, mentor-authored file, passing test without authorship, or
repeated prompted restatement is not project mastery. The final defense is brief
and tied to the diff; misunderstandings normally become the next code edit,
test, or debugging task instead of another oral quiz.
