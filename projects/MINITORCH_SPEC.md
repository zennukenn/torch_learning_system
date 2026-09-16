# MiniTorch accepted project specification

本文件记录 2026-09-13 与学习者确认的稳定边界。Inference 的详细必修范围、训练降级策略和 pinned-PyTorch 对照见 [INFERENCE_SCOPE.md](INFERENCE_SCOPE.md)；双 PrivateUse 路线和真实硬件验证边界见 [PRIVATEUSE_BACKEND_SPEC.md](PRIVATEUSE_BACKEND_SPEC.md)；全面知识审计见 `curriculum/COVERAGE_AUDIT.md`。后续课程可按证据调整顺序和时间，但改变这些边界前必须再次与学习者确认。

## Purpose

MiniTorch 是贯穿 PyTorch、C++、CUDA 与工程知识学习的独立实现项目。它尽可能复刻 PyTorch 的主要目录、分层职责、构建、binding、codegen、测试和打包路径，只缩小支持的 API、dtype、device、operator 与模型范围。

它不是生产级 PyTorch 替代品，也不是只用 Python/NumPy 包装出的教学库。每个纳入主线的主要子系统都必须最终留下一个可运行的最小闭环，并与固定 revision 的真实 PyTorch 源码做职责和取舍对照。

## Repository boundaries

- Learning system: current repository; stores curriculum, evidence, session notes and artifacts.
- Reference source: `sources/pytorch/`; independent Git repository pinned by `config/PYTORCH_SOURCE_PIN`.
- Learner project: `mini-torch/`; a third, independent Git repository, ignored by the learning-system repository.
- Always run project revision, status, history and diff commands as `git -C mini-torch ...`.
- Never copy generated/build products between these repositories or record one repository's commit as another's revision.

The Python import name is `minitorch`, deliberately avoiding collision with the official `torch` package. Other major directory names mirror PyTorch where useful.

## Target layout

Milestone M0 creates the layout progressively. Empty directories are not evidence of coverage.

```text
mini-torch/
├── .github/workflows/       # CI introduced after local build/test is stable
├── aten/
│   └── src/ATen/            # Tensor API, native ops, CPU/CUDA kernels
├── c10/
│   ├── core/                # Device, dtype, dispatch and core abstractions
│   ├── cuda/                # minimal CUDA runtime abstractions
│   └── util/                # ownership, errors and utility code
├── cmake/                   # CMake modules and package configuration
├── minitorch/               # Python frontend; corresponds to PyTorch `torch/`
│   ├── amp/                  # inference autocast policy
│   ├── autograd/
│   ├── cuda/                 # memory, streams, events and graphs
│   ├── compiler/
│   ├── csrc/                # C++ sources for Python/native bindings
│   ├── distributed/         # process group, collectives, mesh/DTensor, DP/TP
│   └── nn/
├── test/                    # Python integration, parity and error tests
├── tools/                   # build/package helpers
├── torchgen/                # reduced schema-driven code generation
├── benchmarks/
├── backends/
│   └── privateuse/           # public ABI loader and CPU mock plugin
├── CMakeLists.txt
├── pyproject.toml
└── setup.py                 # retained when a PyTorch-like build bridge is taught
```

`minitorch/` intentionally replaces the upstream `torch/` package directory. Binding sources live under `minitorch/csrc/`; the built extension is imported as `minitorch._C`. Every other divergence from the reference layout must be recorded in a short architecture decision record with its educational reason.

## Native-PyTorch consistency rules

For the supported subset, prefer the native PyTorch public shape and vocabulary: `minitorch.Tensor`, `minitorch.nn.Module`, `minitorch.no_grad`, `minitorch.inference_mode`, `minitorch.amp.autocast`, `minitorch.cuda.Stream/Event`, `minitorch.cuda.memory_stats`, `minitorch.distributed`, DeviceMesh/distributed-tensor placement and tensor-parallel styles. The import prefix changes from `torch` to `minitorch`; signatures may omit unsupported options but must reject them explicitly rather than silently changing semantics.

Internal structure should preserve the same responsibility boundaries where they are educationally meaningful: Python frontend versus `csrc` binding, Tensor/Storage versus allocator, schema/codegen versus dispatcher, backend registration versus kernels, Autograd/mode wrappers, runtime state, graph capture/lowering and distributed process-group/placement layers.

Every implemented feature records:

- the corresponding public PyTorch API and pinned source anchor;
- matching behavior and intentionally unsupported behavior;
- structural differences required by the reduced implementation;
- why the simplification is safe for current learning and where it would fail to scale.

Do not imitate incidental file count or copy production machinery whose responsibility has not been taught. Native consistency means aligned contracts and ownership, backed by source evidence and parity tests.

## Implementation and dependency policy

- Implement Tensor, Storage, views, operators, dispatcher, Autograd and core runtime in C++.
- Bind the native core into Python with pybind11 and expose a Pythonic `minitorch` frontend.
- Implement foundational CPU kernels directly. Add small real CUDA kernels and minimal allocator/stream/event behavior after the CPU and dispatch contracts are stable.
- Use the PrivateUse CPU mock for backend registration, unsupported behavior, fallback and fault-injection experiments before private hardware runs.
- Implement two hardware-integration routes: a MiniTorch `PrivateUse` plugin using a versioned public C ABI and a separate native PyTorch `PrivateUse1` out-of-tree package modeled on the pinned `OpenReg` reference. The learner supplies any real vendor adapter privately.
- Use CMake for native targets; use `pyproject.toml` plus setuptools for build isolation, editable installs and wheels. Study why `setup.py` remains as a bridge where applicable.
- Use pytest for Python/integration tests and CTest plus a suitable C++ test harness for native units.
- NumPy and official PyTorch may be used only as test oracles. The installed MiniTorch package must import and execute its supported subset without importing either one at runtime.
- Begin with direct scalar loops. Add BLAS/cuBLAS as later optimized backends so the learner can compare handwritten kernels, external-library integration and performance contracts.

## Required runnable subsystem coverage

The supported surface may be small, but the main course must include executable slices through:

1. CMake targets, compile/link, pybind11 and editable development installation,
   followed by a release-grade wheel at the deployment gate;
2. Tensor/Storage metadata, ownership, strides, views, dtype and device;
3. operator schema, reduced codegen, dispatcher, registration, redispatch/fallback and CPU kernels;
4. CUDA kernel launch, caching allocator, pinned memory, stream/event, allocator-stream lifetime, synchronization and CUDA Graph evidence;
5. Python `nn.Module`, Parameter/buffer state, CNN and decoder-style Transformer inference operators, one representative quantized Linear, serialization and model loading;
6. reverse-mode Autograd, saved values, version/in-place checks, `no_grad` and inference boundary;
7. allocator/threading/profiling, process groups/collectives, DeviceMesh/DTensor-like placements, inference DP and row/column TP;
8. a small graph IR, capture/tracing contract, shape/meta reasoning, decomposition, lowering, fusion, cache/guards and compiler backend;
9. simulated device registration, supported/unsupported matrix, fallback and error policy;
10. native PyTorch `PrivateUse1` hooks/registration/runtime/compiler package and shared conformance tests;
11. packaging, CI, AOT/deployment, compatibility matrix and final inference demonstrations.

Autograd and a tiny optimizer remain required architecture lessons. Training is limited to one small MLP smoke case and one two-rank gradient all-reduce boundary. Inference receives the main implementation, CUDA memory/stream, mixed-precision, CNN/Transformer, DP/TP, compiler, compatibility and performance effort. An unfinished inference requirement always takes priority over a training extension.

## Integration demonstrations

Completion requires these learner-defended demonstrations. Delivery is
spiral: the first item initially runs with an explicit contiguous-FP32/manual-op
walking skeleton in Release A, then becomes a permanent regression test after
M1/M2 replace those shortcuts in Release B.

- run an early CPU `Linear → ReLU → Linear` inference at M2.5 before beginning CUDA;
- train a small MLP to show the Autograd/optimizer boundary;
- run a small CNN inference on CPU and CUDA and compare against an oracle;
- run a decoder-style Transformer block with naive attention and KV-cache prefill/decode cases;
- run one weight-only or int8 Linear path with explicit quantization parameters, packing and float-oracle error evidence;
- lower a supported inference model to the MiniTorch IR and execute it through the custom compiler backend;
- run inference DP across two local processes and reconstruct the reference outputs;
- run row/column tensor-parallel Linear and a small TP Transformer/MLP slice across two ranks;
- demonstrate allocator reuse/fragmentation, cross-stream lifetime, events and one static CUDA Graph replay;
- execute supported work on a simulated device and verify unsupported/fallback behavior;
- compare eager/compiled, CPU/CUDA, full/mixed precision and unsharded/TP behavior with correctness, latency, throughput and memory evidence;
- build a wheel, install it into a clean environment and run representative inference checks.

## Authorship contract

The mentor explains prerequisites, points to verified reference-source anchors, defines interfaces and acceptance behavior, creates minimal non-decisive scaffolding when needed, reviews changes, helps instrument failures and supplies H0-H3 hints. The learner authors the decisive architecture choices and core implementation. When a repository document, build configuration or test is itself the current learning outcome, it is also learner-authored rather than silently generated by the mentor.

Teaching and implementation are interleaved: a focused prerequisite explanation is followed immediately by a learner edit in `mini-torch/`, diff inspection and the narrowest relevant verification. Mentor-created drafts are labeled permanently in session provenance and cannot become learner evidence through approval or recitation; the learner must materially revise or replace them.

A full implementation may be supplied by the mentor only when the learner explicitly requests it. Code written by the mentor cannot by itself raise the learner's mastery score.

## Size budget

MiniTorch remains mechanism-complete and surface-small:

- approximately 20–30 operator schemas and 10–15 backend-native kernels;
- one recurring pointwise, reduction, view/mutation, matrix, convolution and attention slice;
- one small CNN and one small decoder Transformer block;
- composite implementations for higher APIs when their children preserve required semantics;
- CPU mock plugins and two-process tests before hardware or scale-specific work;
- no operator is added unless it enables a target model or teaches a new mechanism.

Additional quantization modes, specialized mobile, sparse, nested, ONNX, TorchScript, FSDP, RPC, PP/CP/EP and platform backend breadth remain I1/I2 source/experiment tracks unless promoted by a capstone requirement.

The complete scope is delivered through three product checkpoints rather than
one distant finish line: Release A provides working CPU inference in 30–50
focused hours, Release B provides a robust eager CPU/CUDA inference engine, and
Release C completes source/backend mastery. Passing an earlier release is a
real project outcome but does not erase the remaining full-mastery curriculum.

## Final runnable definition

The project is complete only when:

- `minitorch` builds from a clean checkout and installs as a wheel in a clean environment;
- required CPU tests and supported eager/compiled CNN and Transformer inference pass;
- CUDA-required tests pass on a verified CUDA environment and CPU-only builds remain supported;
- Route A MiniTorch PrivateUse and Route B native PyTorch PrivateUse1 pass the mock/proxy conformance suite;
- the private vendor adapter can be built outside the repository from the public ABI and the learner has a sanitized real-device test command bundle;
- real third-party hardware is described as working only after that private run passes device-smoke and representative-model verification;
- unsupported behavior is deterministic and never silently executes on CPU while reporting a vendor device.

## Definition of learned

Passing tests is necessary but insufficient. A milestone increment is learned only when the learner can:

- explain the contract and invariants of their change without notes;
- identify the corresponding MiniTorch and inspected PyTorch locations;
- show focused positive, boundary and error tests with reproducible commands;
- diagnose a real or seeded defect using evidence;
- state material simplifications and their consequences;
- complete a later small extension or repair without replaying the original instructions.

Standalone trivia exams are retired. `QUESTION_HISTORY.csv` remains for historical compatibility and records project defense, diagnosis and review prompts from the transition onward.
