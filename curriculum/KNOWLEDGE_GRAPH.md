# Knowledge graph and architecture map

The learner-facing top-to-bottom inference course and its immediate MiniTorch
applications are indexed in `curriculum/COURSE_PRACTICE_PLAN.md`; the
machine-validated first accountable course for every mastery concept is stored
in `curriculum/COURSE_PRACTICE_MAP.csv`.

## MiniTorch project map

The course revisits the same architecture through learner implementation:

```text
M0a native import → M0b local development/test loop
  → M2.5 restricted first CPU model walking skeleton
    → M1 durable c10 foundations + Storage/Tensor/numerics
      → M2 schema/codegen/Dispatcher/CPU hardening of the same model
        → M0c advanced native debugging → M3 CUDA memory/streams + kernels/libraries + precision
          → M4 Python frontend + CNN/Transformer/KV cache + quantized inference state
        → M5 minimal Autograd/training boundary
        → M6 runtime/profiler + inference DP/TP
          → M7 graph IR/capture/compiler/dynamic shapes
            → M8 MiniTorch PrivateUse + native PyTorch PrivateUse1
              → M9 wheel/CI/inference capstone
```

The major directory mapping is `PyTorch torch/ → MiniTorch minitorch/` and `torch/csrc/ → minitorch/csrc/`, with `aten/`, `c10/`, `torchgen/`, `tools/`, `test/`, `cmake/` and root build files retaining their architectural roles at reduced scale. The compiled binding is exposed as `minitorch._C`. Empty directory coverage has no learning value; each node becomes complete only through a runnable vertical slice, tests, debugging and learner defense.

## 初学者全景图

先掌握这张职责图，再阅读下面的源码依赖图：

```text
用户数据
   ↓
Python program / model.forward
   ↓
Tensor + operators ───────────────┐
   ↓                              │
eager execution                  optional graph/compiler path
   ↓                              │
runtime + CPU/GPU kernels ←───────┘
   ↓
输出

training 时 Autograd 记录并计算梯度
distributed 在多进程/多机器之间协调 tensor computation
backend 把框架请求落实到具体硬件和软件栈
```

第一轮只要求知道每层“做什么”和相邻层如何连接。`schema`、`Dispatcher`、`TensorIterator`、generated binding、Autograd Engine、Dynamo/Inductor 等都属于后续放大后的内部机制，不应在第一次全景课同时展开。

## 主依赖

```text
Python data model ─┐
                  ├─> Python frontend/bindings ─> schema/codegen ─> Dispatcher
C++/build/linking ┘                                      │             │
                                                         │             ├─> ATen kernels/TensorIterator
Tensor metadata/storage/views ────────────────────────────┘             ├─> Autograd/fallback/modes
                                                                       └─> device backend/runtime

Dispatcher + Tensor/runtime ─> accelerator eager backend ─┐
FX/FakeTensor/shapes ─> Dynamo/export/AOT ─> lowering ─────┼─> inference compatibility
allocator/streams/events/profiler/serialization ──────────┤
distributed/process group ────────────────────────────────┘
```

学习任何后层概念失败时，先回到图中最早的薄弱前置，而不是继续堆术语。只有通过 Foundation Gate，下面的依赖图才成为主要授课地图。

## 子系统问题表

| 子系统 | 必须能回答的问题 | 典型证据 |
|---|---|---|
| Python frontend | API 如何注册 state、处理 overrides 并进入 native op？ | Python source、minimal hook/subclass experiment |
| Tensor/storage | metadata、ownership、alias 与 mutation 谁负责？ | object/source graph、storage/view experiment |
| Binding/codegen | schema 如何产生 Python/C++ API 和 registration？ | schema、generator、generated file 三点闭环 |
| Dispatcher | key set 如何形成，哪个 kernel/fallback 被选中，怎样 redispatch？ | dispatch table、registration site、runtime trace |
| ATen/kernel | dtype/device/layout specialization 在哪里发生？ | native implementation、kernel launch/CPU path |
| Autograd | graph/node/edge 如何产生，inference mode 改变什么？ | forward/backward trace、version/inplace experiment |
| Runtime | allocator、guard、stream/event、RNG、profiler 各自拥有何状态？ | focused test、stack/log/profile |
| Distributed | collective API 到 ProcessGroup/backend 的边界是什么？ | minimal trace、source/test anchors |
| Compiler | frame/graph/guards/decomposition/lowering/codegen 如何连接？ | graph/log/generated code/equivalence test |
| Accelerator | eager device backend 与 graph compiler backend 各负责什么？ | ownership diagram、prototype、negative tests |
| Compatibility | “模型可用”如何被正确性、动态 shape、fallback、内存、并发、性能、升级共同证明？ | versioned matrix、model tests、benchmark protocol |
| Build/package | `pyproject.toml`、setuptools、CMake targets、compile/link、extension module 与 wheel 如何连接？ | early clean local editable loop; M9 release wheel/ABI/CI evidence |
| pybind11 | Python object 如何跨到 C++ type，谁持有 lifetime，异常和 conversion 如何传播？ | native import path、lifetime/error tests、binding source |
| Test engineering | unit/integration/parity/negative/performance/package test 各证明什么、不能证明什么？ | acceptance matrix、seeded failure、isolated install |
| CUDA | host/device、kernel launch、allocation、stream/event 和 synchronization 如何影响正确性与测量？ | CUDA tests、dispatch trace、synchronized benchmark |
| CUDA memory | allocated/reserved、cache reuse、fragmentation/OOM、pinned transfer 与跨 stream lifetime 如何连接？ | allocator counters/snapshot、OOM reproduction、`record_stream` failure/repair |
| Inference modes | `eval`、`no_grad`、inference mode 和 autocast 分别改变什么状态与 dispatch？ | mode matrix、TLS/source trace、version/precision tests |
| Transformer inference | attention mask、prefill/decode、KV cache shape/lifetime 和 dynamic sequence 怎样保持正确？ | decoder block parity、cache update/memory tests |
| Quantized inference | scale/zero-point、observer/calibration boundary、weight packing、accumulation 和 backend lowering 怎样保持精度与 device ownership？ | representative quantized Linear eager/compiled parity and error tests |
| Inference DP | model replica、input partition、weight broadcast、output reconstruction 各由谁负责？ | two-rank shard/gather trace、throughput/correctness comparison |
| Tensor parallel | DeviceMesh/placement 如何导出 row/column Linear 的 shard shape 与 collective？ | two-rank TP Linear/Transformer parity、collective trace |
| Inference performance | latency、throughput、memory、transfer、communication、compile/startup cost 怎样分别测量？ | synchronized benchmark、profiler timeline、memory statistics |
| Numerical semantics | promotion、broadcasting、accumulation、NaN/Inf/overflow、tolerance 和 determinism 怎样跨 backend 保持？ | adversarial parity matrix、seed/state tests |
| CPU runtime | allocator、thread pool、parallel loop、vectorization 与 math library 如何选择？ | scalar/parallel/vector/library trace and benchmark |
| Native boundary | pybind conversion/lifetime、GIL、exception、ABI/RPATH 如何影响 Python 调 C++？ | import/error/GIL test、symbolized stack、wheel inspection |
| PrivateUse plugin ABI | 如何让 MiniTorch 调用不公开的 vendor runtime 而不泄露 C++ ABI 或专有信息？ | version negotiation、CPU mock、fault injection、private command bundle |
| Native PrivateUse1 | rename/module、guard/hooks、allocator、factory/copy、kernels/fallback、AMP/profiler/compiler 如何闭环？ | OpenReg source comparison、OOT package contract tests |

## 跨层 vertical slices

课程反复使用以下 slice，而不是每次换一个不相关模块：

1. `torch.add` 或同类 elementwise op：schema、dispatch、TensorIterator、CPU/CUDA、Autograd、compile。
2. `nn.Linear`：Module state、matmul/addmm family、weights/layout、serialization、compile/model compatibility。
3. view/in-place op：storage alias、version counter、functionalization、Autograd、backend view semantics。
4. reduction：dtype policy、parallelism、shape/meta、dynamic shapes、lowering。
5. 一个小 inference model：eager execution、export/compile、memory/profiler、distributed boundary、custom backend。
6. 一个 decoder-style Transformer block：Embedding/Linear/LayerNorm/attention、KV cache、mixed precision、dynamic sequence、compile 与 TP。
7. CUDA buffer lifetime：allocator cache、non-default stream、event/`record_stream`、OOM/fragmentation 与 CUDA Graph constraints。
8. quantized Linear：quantization parameters、packed weight、dispatcher/backend kernel、compiler lowering、float oracle 与 PrivateUse capability。

## 掌握层次

每个 node 分别评估 `explain → locate → trace → debug → modify → transfer → retain`。能复述概念不等于会定位；能按教程修改不等于能迁移到新的 operator 或 backend。
