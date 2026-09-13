# Mastery-paced PyTorch and MiniTorch roadmap

原 20 周/约 400 小时只保留为节奏基线。2026-09-13 起，学习者接受延长周期，以全面性和深度优先；阶段是否通过只看证据和 MiniTorch 项目关卡。基础阶段可以重复或延长，未通过 gate 时不得用日历进度强行进入深层源码。

MiniTorch 是课程的连续实现主线，稳定范围见 `projects/MINITORCH_SPEC.md`，inference-first feature matrix 见 `projects/INFERENCE_SCOPE.md`，双 PrivateUse 路线见 `projects/PRIVATEUSE_BACKEND_SPEC.md`，全面覆盖审计见 `curriculum/COVERAGE_AUDIT.md`，增量和 gate 见 `projects/ROADMAP.md`。真实 PyTorch 源码仍是每个设计的权威对照。课程不再把阶段项目放在知识讲授之后：每个主题都以 `讲清 prerequisite → 查看 PyTorch anchor → 学习者实现 MiniTorch increment → tests/debug → code defense → delayed extension` 完成闭环。

## 每周节奏

- 3–5 × 90–120 分钟：围绕当前 MiniTorch increment 讲 prerequisites、读对应源码、设计、实现与 review。
- 2 × 2–3 小时：完成 learner-authored code、focused tests 和 debugging。
- 1 × 1–2 小时：对较早 increment 做小扩展/修复并更新架构图与知识图。
- 构建等待时间不计入有效学习时数；每周只承诺一个主要 increment，避免同时铺开多个半成品子系统。

Foundation Gate 之前每周至少留下：一份学习者画的架构/目录图、一个 M0 工程增量、一处浅层源码观察、focused build/test evidence 和一次对已实现内容的无提示解释。Gate 之后每周至少留下 MiniTorch diff/commit、PyTorch source comparison、tests/debug evidence 和 delayed extension/review。

源码锚点均为“候选入口”，Agent 必须在当前 checkout 中确认实际路径和 symbol，不能照表臆测。

## Phase 0 — 架构、词汇、语言与源码阅读基础（Week 1–2，可按 gate 延长）

本阶段默认使用 architecture-first foundation mode：约 `60%` 详细讲解、`25%` 练习、`15%` 浅层源码观察。每节课从同一张全局图开始，只放大一个区域。下面是顺序而不是必须一天一节的日历。

项目主线：`MiniTorch M0`。不要求学习者在未知 C++/构建概念上猜实现；先讲最小模型，再让学习者完成相应架构图、配置或代码。M0 的 build/import loop 取代原来的 Foundation 纸面考试。

### Foundation 0.1：PyTorch 是什么

- 目标：用日常语言区分 library、Tensor、operator、model/`Module`、`forward`、device、training 和 inference。
- 例子：一个输入经过简单模型得到输出；先讲数据和职责，不讲 dispatcher、codegen 或 kernel specialization。
- 练习：给概念配角色、按一次 inference 的先后排序、用自己的例子复述。
- 源码观察：只看 `torch/` 顶层和一个可读的 Python API 所在文件，建立“概念有真实位置”的感觉。

### Foundation 0.2：Tensor 与数据的最小模型

- 目标：理解 Tensor 是带有 shape、dtype、device 的多维数据容器，能区别 scalar/vector/matrix/tensor。
- 例子：图片 batch 或两行三列数字；解释 shape 改变了什么、dtype/device 描述什么。
- 暂不进入：`TensorImpl`、`StorageImpl`、stride/view ownership、allocator。

### Foundation 0.3：一次 inference 的全景

- 目标：解释 `input → model.forward → operators → CPU/GPU execution → output`。
- 只在地图上标出 Autograd、compiler 和 distributed 的位置与“为什么存在”，不讲内部数据结构。
- 练习：区分 user code、framework work 和 hardware work；比较 training 与 inference 的高层差异。

### Foundation 0.4：PyTorch 全局分层架构

- 目标：能在一张图上放置 Python frontend、Tensor/operator core、eager execution、Autograd、runtime、compiler、distributed 和 hardware/backend。
- 方法：先按职责分层，再把一个 inference 例子放回图中；每层只保留一个核心问题。
- 产物：学习者自己画或补全的第一版架构图。

### Foundation 0.5：源码仓库地图

- 目标：把已经理解的架构层映射到 `torch/`、`aten/`、`c10/`、`test/`、`tools/`，能说明它们不是一一对应的封闭模块。
- 候选锚点：`README.md`、顶层目录、一个 Python frontend 文件和一个测试文件。
- 暂不要求：从 Python API 追到 schema、dispatcher 或 concrete kernel。

### Foundation 0.6：Python 最小执行模型

- 目标：理解 module/import、class/object、method/function、argument/return 和 call stack 的基础意义。
- 方法：先用十几行普通 Python reduced example，再观察 PyTorch Python source 中同一种构造。
- 暂不进入：descriptor、metaclass、`__torch_function__` 或复杂 decorator。

### Foundation 0.7：C++ 与构建的最小模型

- 目标：解释 source/header、declaration/definition、compile、object file、link、library，以及 pointer/reference 的第一层含义。
- 方法：先画出一个两文件小程序如何变为 executable/library，再看 PyTorch 为什么需要 Python/C++ 边界。
- 暂不进入：template metaprogramming、宏生成、RAII/intrusive pointer 细节和 native stack 调试。

### Foundation 0.7b：native extension 与工程调试闭环

- 目标：理解 CPython extension/pybind11、Python↔C++ conversion、ownership、exception translation、GIL、shared-library ABI/RPATH、debug symbol 和 stack trace。
- 方法：先建立一个 native function import/error/GIL-release 小闭环，再加入 debugger、sanitizer、linter 和 `compile_commands.json`；复杂 Tensor binding 留到 M1。

### Foundation 0.8：第一次浅层源码定位闭环

- 目标：在已理解的层内完成 `问题 → 候选目录 → rg → 打开文件 → 用小证据核对`。
- 推荐路径：可读的 Python frontend 调用，例如 `nn.Linear.forward` 到其直接 Python-level callee；不继续钻入 dispatcher/codegen。
- 环境并行项：固定 revision，审计 Python/torch/CMake/Ninja/GDB；安装或构建仍需单独确认成本和授权。
- 产物：基础架构图、词汇表、仓库地图、最小 Python/C++ 程序图和一次浅层定位记录。
- MiniTorch 产物：独立仓库、PyTorch→MiniTorch 目录映射、`pyproject.toml`/CMake/pybind11 最小 build-install-import loop、pytest 与 CTest smoke tests。

Foundation Gate：

- `PYTORCH-BASICS.explain >= 2`，能用自己的例子解释 Tensor、operator、Module/forward、device、training/inference；
- `ARCH-MAP.explain >= 2` 且 `ARCH-MAP.locate >= 1`，能重画全局层次并把主要顶层目录放到合理区域；
- `PY-DATAMODEL.explain >= 1`、`CPP-CORE.explain >= 1`、`ENV-BUILD.explain >= 1`；
- 能完成一次仅跨已学层次的查找—解释—小验证循环。
- 通过 `projects/ROADMAP.md` 的 M0 gate，并能无笔记解释自己编写的配置和 native import path。

未通过此 gate 时，advanced source trace 只能作为 preview，不安排 schema/codegen/dispatcher 的实现或独立复习。通过后才进入以 MiniTorch implementation 和 vertical call chain 为主的教学模式。

## Phase 1 — Tensor 与 Python frontend（Week 3–5）

项目主线：先完成 `MiniTorch M1`，再完成 `M4` 中只依赖当前算子集合的 frontend increments；复杂算子由 M2 补齐。

### Week 3：Tensor 对象模型

- 目标：区分 Python `Tensor`、C++ `at::Tensor`、`TensorImpl`、`StorageImpl`、`DataPtr` 的角色和 ownership。
- 主题：sizes/strides/storage_offset、dtype/device/layout、contiguous、alias/view、version counter；补齐 type promotion、broadcasting、accumulation dtype、NaN/Inf/overflow、tolerance、RNG 与 determinism。
- 候选锚点：`c10/core/TensorImpl.h`、`c10/core/StorageImpl.h`、`aten/src/ATen/core/Tensor.h`。
- 实验：view/clone/detach/reshape 的 storage alias、stride 和 mutation 行为。

### Week 4：Python frontend、`nn.Module` 与 state

- 目标：掌握 module/parameter/buffer 注册、attribute 机制、hooks、`state_dict`、serialization 基本路径。
- 补课：`__getattr__`/`__setattr__`、descriptor、iterator/generator、context manager、typing。
- 候选锚点：`torch/nn/modules/module.py`、`torch/nn/parameter.py`、`torch/serialization.py`。
- 实验：先追踪 `nn.Linear` 初始化、参数注册、forward、保存与加载；随后用 CNN 与 decoder-style Transformer block 扩展到 Conv2d、inference BatchNorm、Embedding、LayerNorm、attention、KV cache、`eval`、inference mode 和 autocast；在算子层完成后加入一个 weight-only 或 int8 quantized Linear。

### Week 5：overrides、modes 与 tensor subclass

- 目标：比较 `__torch_function__`、`__torch_dispatch__`、mode/subclass 与普通 dispatcher 的边界。
- 候选锚点：`torch/overrides.py`、`torch/utils/_python_dispatch.py` 及 checkout 中对应 tests。
- 实验：最小 tensor subclass/mode，记录哪些调用被截获以及何时 redispatch。
- 产物：Tensor lifetime/alias 图、`nn.Linear` 调用链、Phase 1 源码修改项目。

Gate 1：通过 M1 gate；`TENSOR-MODEL` 和 `PY-FRONTEND` 的 `explain/locate/trace` 至少 2，`modify` 至少 2；能从未知 tensor 行为定位到 metadata、view、binding 或 frontend 层并修复 focused failure。

## Phase 2 — schema、codegen、Dispatcher 与 kernel（Week 6–9）

项目主线：完成 `MiniTorch M2`，然后完成 `M3` 的真实 CUDA backend。M3 必须覆盖 caching allocator、fragmentation/OOM、pinned transfer、stream/event、跨 stream lifetime 和 mixed precision；CPU-first，CUDA 环境未通过时不得用静态代码代替 runtime mastery。

### Week 6：operator schema 与生成链

- 目标：从 Python API 找到 schema、derivative/decomposition/registration 信息和 generated wrapper。
- 主题：overload、alias annotation、structured kernel、manual vs generated binding。
- 候选锚点：`aten/src/ATen/native/native_functions.yaml`、`torchgen/`、`tools/autograd/`、build tree generated files。当前固定版本中，ATen/operator codegen 主要位于 `torchgen/`，Python/Autograd 生成链仍有入口位于 `tools/autograd/`；每次以 checkout 为准。
- 补课：YAML 驱动 codegen、C++ overload、function pointer、template instantiation。

### Week 7：Dispatcher 核心

- 目标：理解 operator handle、dispatch table、`DispatchKey`/`DispatchKeySet`、registration、fallback、redispatch。
- 候选锚点：`c10/core/DispatchKey.h`、`aten/src/ATen/core/dispatch/`、`torch/library.py`。
- 实验：检查一个 operator 的 dispatch table；对 CPU、Meta、Autograd 等路径作预测并验证。

### Week 8：ATen native、TensorIterator 与 CPU/CUDA kernel

- 目标：沿一个 pointwise op 和一个 reduction/matmul op 到 concrete kernel；理解 device/dtype/layout specialization。
- 候选锚点：`aten/src/ATen/native/`、`aten/src/ATen/native/cpu/`、`aten/src/ATen/native/cuda/`、`aten/src/ATen/TensorIterator*`。
- 补课：lambda、type dispatch macro、vectorization、parallel loop、CUDA grid/block、coalescing、shared memory、atomics、occupancy 与 launch/synchronization。
- CPU inference 补课：thread control、parallel loop、vectorization、false sharing/oversubscription、BLAS/oneDNN-style library boundary 和正确 benchmark。
- CUDA library 补课：用一个代表算子比较 naive kernel 与 cuBLAS/cuDNN-style path，解释 handle、workspace、algorithm selection、determinism 和 dtype policy。
- 工程补课：用一个 out-of-tree custom op 学 schema/kernel/fake/meta/alias contract 和 conformance testing。

### Week 9：端到端 operator 生命周期

- 目标：完成 `Python → binding/codegen → schema → dispatcher → CPU/CUDA kernel → result`，并解释各层不变量。
- 实验：比较 eager CPU、Meta/Fake 或 CUDA（环境可用时）的选择差异；构造错误 dtype/layout/device 用例；完成 representative quantized Linear 的 scale/zero-point、packing、error/tolerance tests。
- 产物：两条可复现 full traces、Phase 2 operator/registration 项目。

Gate 2：通过 M2 gate，并在可用环境下通过 M3 gate；`BIND-CODEGEN`、`DISPATCH`、`ATEN-KERNEL`、`CUDA` 的 `trace` 至少 3，`modify` 至少 2；能解释一次 redispatch 并用 runtime evidence 证明 CPU/CUDA kernel 选择。

## Phase 3 — Autograd、runtime 与 distributed 架构（Week 10–12）

项目主线：完成 `MiniTorch M5` 和 `M6`。训练内容止于小型 MLP smoke case；inference mode、runtime、observability 与 distributed boundary 获得更多时间。

### Week 10：Autograd 数据结构与 generated wrappers

- 目标：理解 `requires_grad`、`grad_fn`、edge、Node、saved tensor、version check，以及 Autograd dispatch 层。
- 候选锚点：`torch/csrc/autograd/`、`tools/autograd/`、`derivatives.yaml` 及生成产物。
- 实验：追踪一个简单 forward/backward；随后比较 `no_grad` 与 `inference_mode`。

### Week 11：Engine、并发与 inference boundary

- 目标：理解 engine graph task/ready queue 的全局位置，并聚焦 inference mode、functionalization、mutation/view safety。
- 补课：thread、mutex/atomic、TLS、RAII guard、intrusive pointer。
- 实验：触发 inplace/version error，形成假设并用 source/runtime 证据解释。

### Week 12+：allocator、stream/event、profiler 与 distributed inference

- 目标：建立 inference runtime 地图；深入显存 allocated/reserved、cache/fragmentation/OOM、pinned transfer、stream/event/`record_stream` lifetime；理解 c10d/ProcessGroup/Work、collectives、DeviceMesh/DTensor placement、inference DP 和 row/column TP。
- 候选锚点：`c10/cuda/CUDACachingAllocator.*`、`CUDAStream.*`、`CUDAEvent.h`、`torch/cuda/memory.py`、`torch/csrc/profiler/`、`torch/csrc/distributed/c10d/`、`torch/distributed/device_mesh.py`、`torch/distributed/_tensor/`、`torch/distributed/tensor/parallel/`。
- 实验：allocator fragmentation/OOM 与跨 stream lifetime；CPU 两进程 collectives；replicated inference DP；row/column parallel Linear 与 TP Transformer/MLP slice；有两张可用 GPU 时再验证 NCCL stream overlap。
- 训练边界：只保留小型 MLP、最小 SGD 和一次 gradient all-reduce；DDP bucket/reducer、FSDP optimizer state 和训练性能降为 inference capstone 后的 extension。
- 产物：Autograd/inference 对照链、runtime ownership 图、DP/TP shard-and-collective 图、MiniTorch M5/M6 debugging dossier。

Gate 3：通过 M5/M6 gate；`AUTOGRAD` 只需达到 inference boundary 所要求的 `explain/trace/modify`，`CUDA-MEMORY`、`INFERENCE-MODES`、`DISTRIBUTED-DP`、`DISTRIBUTED-TP` 成为主要门槛；能说明 inference DP、minimal DDP 和 TP 的不同通信语义，并用两进程结果证明 shard/reconstruct 正确性。

## Phase 4 — PyTorch 2 compiler stack（Week 13–16）

项目主线：完成 `MiniTorch M7`，用小 IR 和明确支持子集亲自实现 capture/meta/decomposition/lowering/fusion/cache/execution，再回看 Dynamo/FX/export/AOT/Inductor 的生产复杂度。重点验证 dynamic batch/sequence、mixed precision、representative quantized lowering、TP graph 与可选 CUDA Graph replay。

### Week 13：FX、Proxy、FakeTensor 与 symbolic shapes

- 目标：理解 graph representation、node semantics、metadata propagation、fake execution 与 shape reasoning。
- 候选锚点：`torch/fx/`、`torch/_subclasses/fake_tensor.py`、`torch/fx/experimental/symbolic_shapes.py`。
- 实验：trace/transform 一个小 module，验证等价性并故意制造 graph limitation。

### Week 14：TorchDynamo

- 目标：理解 frame evaluation、bytecode transformation、guards、cache、graph break 与 recompilation。
- 候选锚点：`torch/_dynamo/`、对应 C/C++ frame-eval 代码和 tests。
- 实验：用日志解释一个 graph break、guard failure 和 recompilation；修正自己的错误预测。

### Week 15：export、AOTAutograd、functionalization 与 decompositions

- 目标：理解 graph capture contract、functional graph、decomposition、partitioning，以及 inference-only 路径如何减少但不消除复杂性。
- 候选锚点：`torch/export/`、`torch/_functorch/`、`torch/_decomp/`。
- 实验：比较 eager、export、compile 所见 graph 与 constraints。

### Week 16：Inductor/Triton/codegen/runtime

- 目标：理解 lowering、scheduler、fusion、code generation、cache、wrapper/runtime 的大路径，不追求逐文件穷举。
- 候选锚点：`torch/_inductor/`、checkout 中的 Triton integration 与 tests。
- 实验：最小 compile trace、generated code inspection、correctness/performance measurement。
- 产物：compiler pipeline 图、graph-break dossier、Phase 4 custom backend 项目。

Gate 4：通过 M7 gate；`FX-EXPORT`、`DYNAMO`、`INDUCTOR` 的 `explain/trace` 至少 3，compiler 相关 `modify/debug` 至少 2；能独立诊断一个 graph/capture/lowering failure，并说明 eager device backend 与 compiler backend 的 ownership 差异。

## Phase 5 — 扩展与 accelerator integration（Week 17–19）

项目主线：完成 `MiniTorch M8`，并把在 MiniTorch 中形成的理解迁移到官方 C++/CUDA extension、`PrivateUse1` 和 `torch.compile` public contracts。

### Week 17：C++/CUDA extension 与 library registration

- 目标：实现 schema、CPU kernel、可选 CUDA kernel、Meta/fake 支持、测试与 benchmark。
- 主题：ABI、build isolation、registration lifetime、error handling、opcheck/gradcheck 适用边界。
- 产物：可安装的 out-of-tree extension；不是只会复制 tutorial。

### Week 18：`PrivateUse1` eager backend prototype

- 目标：完成两条独立路线：MiniTorch `PrivateUse` versioned C-ABI plugin，以及原生 PyTorch `PrivateUse1` OpenReg-style out-of-tree package。
- MiniTorch 路线：plugin loader/capability negotiation、allocator/copy/guard/stream/event、kernel registry/fallback、autocast/RNG/serialization/profiler、compiler interface 和 CPU mock。
- 原生 PyTorch 路线：rename/device module、guard/hooks/allocator/Storage factory、`TORCH_LIBRARY_IMPL`、Autograd/AutocastPrivateUse1、Meta/Fake、stream/event、profiler、compile 和 optional ProcessGroup。
- 真实硬件：学习者私下提供 C/C++ adapter shared library；仓库提供 sanitized device-smoke/model command bundle。无真实运行结果时只声明 contract-ready。
- 产物：双 prototype、public ABI、CPU mock、capability/unsupported matrix、positive/negative/fault tests 和 private hardware conformance plan。

### Week 19：`torch.compile` backend 与 OOT compatibility

- 目标：实现 `(GraphModule, example_inputs) -> callable` contract，设计 supported graph、partition/fallback、lowering/runtime boundary 和 version CI。
- 实验：代表性模型片段在 eager/reference/custom backend 上语义对比；动态 shape 与错误路径测试。
- 产物：compile backend、compatibility matrix、Phase 5 集成项目。

Gate 5：`EXTENSION`、`PRIVATEUSE1`、`PRIVATEUSE-ABI`、`PRIVATEUSE-RUNTIME`、`PRIVATEUSE-OPS`、`COMPILE-BACKEND` 的 `modify` 至少 3，`transfer` 至少 2；双路线 mock/proxy gate 都通过。只有私有 adapter 的 device-smoke 和 representative-model tests 通过后才可声明真实硬件验证。

## Phase 6 — 综合架构与迁移设计（Week 20）

项目主线：完成 `MiniTorch M9` 的 packaging、CI 与 inference capstone。

- 重建 PyTorch 全局架构图，覆盖 Python frontend、Tensor/storage、dispatcher、ATen、Autograd、runtime、distributed、compiler、backend/testing/build。
- 对一个未预先练习的模型片段完成 eager 与 compile 双路径追踪，并覆盖 mode/precision/device/shape 选择。
- 完成 `VENDOR_DEVICE` inference adaptation blueprint：模块边界、风险、fallback、测试矩阵、性能方法、版本升级与 CI。
- 完成 CNN、decoder-style Transformer/KV-cache 与 representative quantized Linear 的 CPU/CUDA、eager/compiled、full/mixed precision、unsharded/DP/TP 对照；报告 latency、throughput、peak allocated/reserved memory、transfer/communication 与 compile/startup cost。
- 进行 learner-authored extension、未提示源码定位、seeded debug challenge 和 capstone code defense。

Final gate：关键概念 `explain/locate/trace` 至少 3；`DISPATCH`、`RUNTIME`、`COMPAT` 的 `debug/modify/transfer` 至少 3；至少一次 +14 天延迟复习通过。没有真实硬件时，结论必须标注为设计或 proxy validation。

## 范围控制

“全方位”表示理解所有主要子系统的职责、边界、关键数据结构，并在 MiniTorch 中拥有可运行最小实现和至少一条可执行调用链；不表示逐行读完数百万行代码或达到生产性能。主线实现一个 quantized Linear；额外 quantization modes、mobile/edge、sparse/nested、MPS/XPU/ROCm、distributed algorithms、TorchScript、ONNX 等专题进入 extension track，由模型需求和目标 backend 决定深度。
