# Knowledge graph and architecture map

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

学习任何后层概念失败时，先回到图中最早的薄弱前置，而不是继续堆术语。

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

## 跨层 vertical slices

课程反复使用以下 slice，而不是每次换一个不相关模块：

1. `torch.add` 或同类 elementwise op：schema、dispatch、TensorIterator、CPU/CUDA、Autograd、compile。
2. `nn.Linear`：Module state、matmul/addmm family、weights/layout、serialization、compile/model compatibility。
3. view/in-place op：storage alias、version counter、functionalization、Autograd、backend view semantics。
4. reduction：dtype policy、parallelism、shape/meta、dynamic shapes、lowering。
5. 一个小 inference model：eager execution、export/compile、memory/profiler、distributed boundary、custom backend。

## 掌握层次

每个 node 分别评估 `explain → locate → trace → debug → modify → transfer → retain`。能复述概念不等于会定位；能按教程修改不等于能迁移到新的 operator 或 backend。
