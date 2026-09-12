# Inference-first scope and PyTorch correspondence

This document refines the accepted MiniTorch specification. Inference is the dominant product and learning path. Training remains only where it is needed to understand Autograd, state mutation and distributed boundaries.

All PyTorch paths below were observed in the pinned checkout `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`) on 2026-09-13. They are starting anchors, not claims that one file owns an entire subsystem.

## Priority model

- **I0 — required runnable inference mechanism:** implement a reduced but executable MiniTorch path, test it and defend it.
- **I1 — representative implementation plus PyTorch study:** implement one representative case, then use source/runtime experiments to understand variants that would add mostly scale.
- **I2 — architecture/source extension:** locate ownership and run a focused official-PyTorch experiment; add to MiniTorch only when a target model needs it.
- **T1 — training boundary:** minimal runnable behavior required to explain inference consequences.
- **T2 — training extension:** postponed until the inference capstone is complete.

The priority says how deeply MiniTorch implements a topic. It does not remove the obligation to understand where the topic sits in native PyTorch.

## Execution and model state

| Topic | Priority | MiniTorch deliverable | PyTorch anchors |
|---|---|---|---|
| `Module.eval()` and mode-dependent state | I0 | recursive mode propagation; inference behavior for supported modules | `torch/nn/modules/module.py` |
| `no_grad` and inference mode | I0 | thread-local guards; graph/version behavior documented and tested | `torch/autograd/grad_mode.py`, `c10/core/InferenceMode.*` |
| autocast and mixed precision | I0 | explicit FP32/FP16/BF16 policy for selected CPU/CUDA ops; autocast guard and error policy | `torch/amp/autocast_mode.py`, `aten/src/ATen/autocast_mode.*` |
| dtype/device/layout conversion | I0 | `to`, copy/cast, contiguous and supported memory-format transitions | `aten/src/ATen/core/TensorBase.h`, `aten/src/ATen/native/Resize.cpp` |
| hooks, tensor modes and overrides | I1 | one interception mechanism and explicit redispatch rule | `torch/nn/modules/module.py`, `torch/utils/_python_dispatch.py`, `torch/overrides.py` |

`eval`, `no_grad` and inference mode are assessed separately: they affect different state and cannot be treated as synonyms.

## Inference operator and model coverage

The goal is not operator-count parity. The operator set must support two distinct model families and exercise shape, reduction, indexing, layout and high-arithmetic-intensity kernels.

| Slice | Priority | Required reduced support | Main PyTorch anchors |
|---|---|---|---|
| Tensor plumbing | I0 | creation, copy/to, view/reshape/transpose, contiguous, slice/select, cat, broadcasting | `aten/src/ATen/native/`, Tensor/Storage anchors from M1 |
| Numeric core | I0 | elementwise add/mul, reduction, matmul/bmm, Linear | `aten/src/ATen/native/BinaryOps.cpp`, `ReduceOps.cpp`, `Linear.cpp` |
| CNN | I0 | Conv2d, ReLU, pooling, inference BatchNorm, channels-first; one channels-last comparison | `aten/src/ATen/native/Convolution.cpp`, pooling sources, `torch/nn/modules/normalization.py` |
| Transformer block | I0 | Embedding, Linear, LayerNorm, GELU, Softmax, masking and naive scaled dot-product attention | `aten/src/ATen/native/Embedding.cpp`, `SoftMax.cpp`, `transformers/attention.cpp` |
| KV cache | I0 | prefill/decode shapes, append or indexed update, lifetime and memory-growth tests | attention/operator sources plus `torch/nn/attention/experimental/_paged_attention.py` as an advanced comparison |
| Optimized attention variants | I1 | one naive MiniTorch implementation; inspect backend selection and compare with an available optimized PyTorch path | `aten/src/ATen/native/transformers/`, `torch/nn/attention/` |
| Quantized inference | I1 | one weight-only or int8 Linear path with scale/zero-point/error tests | `aten/src/ATen/quantized/`, `torch/ao/quantization/` |
| Sparse/nested/special layouts | I2 | architecture map and one focused official-PyTorch experiment | relevant `aten/src/ATen/native/sparse/`, `torch/nested/` paths |

Required model demonstrations are a small CNN and a small decoder-style Transformer block. They are deliberately small enough for debugging while exercising different native PyTorch subsystems.

## CUDA memory, streams and execution

| Topic | Priority | MiniTorch deliverable | PyTorch anchors |
|---|---|---|---|
| Device allocation | I0 | allocator interface, allocated/reserved counters, OOM and cleanup behavior | `c10/cuda/CUDACachingAllocator.*`, `torch/cuda/memory.py` |
| Caching and fragmentation | I0 | reduced block cache, reuse/split policy, fragmentation metric and deterministic scenario | `c10/cuda/CUDACachingAllocator.cpp` |
| Pinned host memory and transfer | I0 | pinned allocation boundary and blocking/non-blocking H2D/D2H tests | `aten/src/ATen/cuda/CachingHostAllocator.cpp` |
| Streams | I0 | current/default stream, per-stream enqueue order and explicit wait/synchronize | `c10/cuda/CUDAStream.*` |
| Events | I0 | record/query/wait and cross-stream dependency test | `c10/cuda/CUDAEvent.h`, `aten/src/ATen/cuda/CUDAEvent.h` |
| Allocator/stream lifetime | I0 | `record_stream`-like contract preventing premature reuse; failing test without it | `c10/core/CachingDeviceAllocator.h`, `c10/cuda/CUDACachingAllocator.*` |
| CUDA Graphs | I1 | capture/replay one static inference path and document allocation/shape constraints | `aten/src/ATen/cuda/CUDAGraph.*`, `torch/cuda/graphs.py` |
| Memory snapshot/configuration | I1 | MiniTorch statistics/snapshot schema and one OOM/fragmentation debug report | `torch/cuda/memory.py`, `torch/csrc/cuda/memory_snapshot.cpp` |
| Communication/compute overlap | I0 in distributed phase | separate streams plus events for one TP collective overlap experiment | `ProcessGroupNCCL` and allocator/stream anchors |

Every CUDA benchmark must state device, dtype, shape, warmup, synchronization point and comparison baseline. Allocation counters and wall-clock timing are different evidence.

## Distributed inference

The distributed implementation starts on two local processes. GPU/NCCL evidence is required only when at least two usable GPUs are verified; otherwise CPU transport and single-device simulation prove the software contract, while multi-GPU performance remains unverified.

| Topic | Priority | MiniTorch deliverable | PyTorch anchors |
|---|---|---|---|
| Process group and asynchronous work | I0 | rank/world, rendezvous, `Work`-like handle, timeout/error propagation | `torch/distributed/distributed_c10d.py`, `torch/csrc/distributed/c10d/ProcessGroup.*` |
| Collectives | I0 | broadcast, all-reduce, all-gather and reduce-scatter with shape/dtype validation | ProcessGroup Gloo/NCCL sources |
| Device mesh and placement | I0 | 1D mesh plus `Replicate`/`Shard(dim)` metadata and redistribution rules | `torch/distributed/device_mesh.py`, `torch/distributed/_tensor/api.py`, `placement_types.py` |
| Inference data parallel | I0 | replicated model, input partition, weight broadcast, output gather and throughput/correctness comparison | process group sources; DDP source for contrast |
| Minimal DDP boundary | T1 | one gradient all-reduce MLP smoke case; explain why inference DP does not synchronize gradients | `torch/nn/parallel/distributed.py` |
| Tensor parallel Linear | I0 | `ColwiseParallel` and `RowwiseParallel` equivalents with all-gather/all-reduce or reduce-scatter | `torch/distributed/tensor/parallel/style.py`, `api.py` |
| TP Transformer block | I0 | shard selected attention/MLP projections across two ranks and verify against unsharded reference | tensor-parallel and DTensor anchors |
| Communication overlap | I1 | asynchronous collective, communication stream/event dependency and timeline evidence | `torch/csrc/distributed/c10d/ProcessGroupNCCL.*` |
| Sequence/context/pipeline/expert parallel | I2 | compare ownership, tensors and collectives; implement only if the capstone model requires it | `torch/distributed/tensor/parallel/`, `torch/distributed/pipelining/`, DTensor experimental attention paths |
| Sharded checkpoint loading | I1 | shard metadata plus rank-local load for TP inference | `torch/distributed/checkpoint/` |

DP and TP must be tested as distinct algorithms. “Two processes ran” is not evidence of either one.

## Compiler and optimized inference

| Topic | Priority | MiniTorch deliverable | PyTorch anchors |
|---|---|---|---|
| Graph capture and graph breaks | I0 | supported Python/module subset, explicit rejection/fallback and diagnostic | `torch/_dynamo/` |
| Fake/meta and symbolic shapes | I0 | metadata propagation, guards and dynamic batch/sequence cases | `torch/_subclasses/fake_tensor.py`, `torch/fx/experimental/symbolic_shapes.py` |
| Decomposition/functionalization | I0 | one compound-op decomposition and mutation/view normalization | `torch/_decomp/`, `torch/_functorch/` |
| Lowering, fusion and code generation | I0 | executable plan plus one elementwise fusion or pattern rewrite | `torch/_inductor/` |
| Cache/recompile behavior | I0 | guard-keyed cache and observable recompilation | Dynamo/Inductor cache paths selected during the session |
| CUDA Graph integration | I1 | static compiled inference replay and constraint comparison | `torch/_inductor/cudagraph_trees.py`, `cudagraph_utils.py` |
| Dynamic shapes and fallback | I0 | dynamic batch and sequence-length tests; explicit unsupported policy | symbolic-shape, Dynamo and backend paths |

## Inference engineering and observability

I0 coverage includes deterministic seeds where applicable, correctness tolerances by dtype, warmup/synchronization, profiler events, allocator statistics, model loading, versioned serialization, batching and failure behavior. The capstone compares eager versus compiled, CPU versus CUDA, full versus mixed precision, unsharded versus TP, and first-run versus steady-state execution.

The performance report separates latency, throughput, peak allocated/reserved memory, transfer time, communication time and compile/startup cost. It must explain measurement limitations rather than presenting one timing number.

## Training scope deliberately reduced

Required `T1` work:

- reverse-mode Autograd for the supported minimal op subset;
- saved values, leaf accumulation, version/in-place checks;
- one minimal SGD implementation and one small MLP training smoke case;
- one two-rank gradient all-reduce to expose the DDP boundary;
- source-level understanding of why Autograd keys, version counters and modes affect inference.

Postponed `T2` work:

- optimizer families, schedulers and large training loops;
- mixed-precision training and `GradScaler` implementation;
- activation checkpointing and sophisticated distributed training algorithms;
- full DDP bucket/reducer, FSDP optimizer state and advanced Autograd APIs;
- training performance tuning beyond what is needed to explain an inference boundary.

These remain visible on the architecture map and in PyTorch source study, but they cannot displace an unfinished I0 inference milestone.
