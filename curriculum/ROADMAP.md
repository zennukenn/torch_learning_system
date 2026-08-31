# 20-week PyTorch source roadmap

计划总量约 400 小时。20 周是节奏基线，不是强制日历；阶段是否通过只看证据和项目关卡。

## 每周节奏

- 5 × 90–120 分钟：概念诊断、vertical source trace、Python/C++ syntax clinic。
- 2 × 2–3 小时：调试、实验或局部实现。
- 1 × 2 小时：闭卷检索、错题复盘、知识图更新。
- 1 × 2–4 小时：阶段项目。若构建耗时很长，等待时间不计入有效学习时数。

每周至少留下：一份调用链、一份实验记录、一张语法卡、一次延迟检索证据和一次项目提交或可审阅 diff。

源码锚点均为“候选入口”，Agent 必须在当前 checkout 中确认实际路径和 symbol，不能照表臆测。

## Phase 0 — 工具、语言与源码阅读闭环（Week 1–2）

### Week 1：环境、仓库与基线诊断

- 目标：固定 stable tag/commit，理解仓库顶层、submodule、build/test/codegen 基本流程。
- 补课：Python import/package；C++ translation unit、header、编译、链接、动态库；CMake/Ninja/GDB 基础。
- 实验：二进制安装版先跑最小 tensor；源码 checkout 后用 `rg` 找一个 public API、test 和实现候选。
- 候选锚点：`README.md`、`CONTRIBUTING.md`、`setup.py`、`CMakeLists.txt`、`torch/`、`aten/`、`c10/`、`test/`、`tools/`。
- 产物：环境审计、revision 记录、仓库地图、首次 baseline assessment。

### Week 2：Python/C++ 边界和调试方法

- 目标：能解释 Python 调用如何可能进入 extension module，并能读懂 native stack 的基本结构。
- 补课：decorator/context manager/descriptor；pointer/reference、RAII、smart pointer、template、macro、symbol visibility。
- 实验：Python stack、native stack、断点或可替代 instrumentation；区分 generated source 与 generator。
- 产物：一个最小 API 的初版 vertical trace 和 Phase 0 项目。

Gate 0：`ENV-BUILD`、`PY-DATAMODEL`、`CPP-CORE` 的 `explain/locate` 至少 2；能独立复现一个查找—假设—验证循环。

## Phase 1 — Tensor 与 Python frontend（Week 3–5）

### Week 3：Tensor 对象模型

- 目标：区分 Python `Tensor`、C++ `at::Tensor`、`TensorImpl`、`StorageImpl`、`DataPtr` 的角色和 ownership。
- 主题：sizes/strides/storage_offset、dtype/device/layout、contiguous、alias/view、version counter。
- 候选锚点：`c10/core/TensorImpl.h`、`c10/core/StorageImpl.h`、`aten/src/ATen/core/Tensor.h`。
- 实验：view/clone/detach/reshape 的 storage alias、stride 和 mutation 行为。

### Week 4：Python frontend、`nn.Module` 与 state

- 目标：掌握 module/parameter/buffer 注册、attribute 机制、hooks、`state_dict`、serialization 基本路径。
- 补课：`__getattr__`/`__setattr__`、descriptor、iterator/generator、context manager、typing。
- 候选锚点：`torch/nn/modules/module.py`、`torch/nn/parameter.py`、`torch/serialization.py`。
- 实验：追踪 `nn.Linear` 初始化、参数注册、forward、保存与加载。

### Week 5：overrides、modes 与 tensor subclass

- 目标：比较 `__torch_function__`、`__torch_dispatch__`、mode/subclass 与普通 dispatcher 的边界。
- 候选锚点：`torch/overrides.py`、`torch/utils/_python_dispatch.py` 及 checkout 中对应 tests。
- 实验：最小 tensor subclass/mode，记录哪些调用被截获以及何时 redispatch。
- 产物：Tensor lifetime/alias 图、`nn.Linear` 调用链、Phase 1 源码修改项目。

Gate 1：`TENSOR-MODEL` 和 `PY-FRONTEND` 的 `explain/locate/trace` 至少 2；能从未知 tensor 行为定位到 metadata、view 或 frontend 层。

## Phase 2 — schema、codegen、Dispatcher 与 kernel（Week 6–9）

### Week 6：operator schema 与生成链

- 目标：从 Python API 找到 schema、derivative/decomposition/registration 信息和 generated wrapper。
- 主题：overload、alias annotation、structured kernel、manual vs generated binding。
- 候选锚点：`aten/src/ATen/native/native_functions.yaml`、`tools/codegen/`、build tree generated files。
- 补课：YAML 驱动 codegen、C++ overload、function pointer、template instantiation。

### Week 7：Dispatcher 核心

- 目标：理解 operator handle、dispatch table、`DispatchKey`/`DispatchKeySet`、registration、fallback、redispatch。
- 候选锚点：`c10/core/DispatchKey.h`、`aten/src/ATen/core/dispatch/`、`torch/library.py`。
- 实验：检查一个 operator 的 dispatch table；对 CPU、Meta、Autograd 等路径作预测并验证。

### Week 8：ATen native、TensorIterator 与 CPU/CUDA kernel

- 目标：沿一个 pointwise op 和一个 reduction/matmul op 到 concrete kernel；理解 device/dtype/layout specialization。
- 候选锚点：`aten/src/ATen/native/`、`aten/src/ATen/native/cpu/`、`aten/src/ATen/native/cuda/`、`aten/src/ATen/TensorIterator*`。
- 补课：lambda、type dispatch macro、vectorization、parallel loop、CUDA launch/synchronization。

### Week 9：端到端 operator 生命周期

- 目标：完成 `Python → binding/codegen → schema → dispatcher → CPU/CUDA kernel → result`，并解释各层不变量。
- 实验：比较 eager CPU、Meta/Fake 或 CUDA（环境可用时）的选择差异；构造错误 dtype/layout/device 用例。
- 产物：两条可复现 full traces、Phase 2 operator/registration 项目。

Gate 2：`BIND-CODEGEN`、`DISPATCH`、`ATEN-KERNEL` 的 `trace` 至少 3，`modify` 至少 2；能解释一次 redispatch 并用 runtime evidence 证明 kernel 选择。

## Phase 3 — Autograd、runtime 与 distributed 架构（Week 10–12）

### Week 10：Autograd 数据结构与 generated wrappers

- 目标：理解 `requires_grad`、`grad_fn`、edge、Node、saved tensor、version check，以及 Autograd dispatch 层。
- 候选锚点：`torch/csrc/autograd/`、`tools/autograd/`、`derivatives.yaml` 及生成产物。
- 实验：追踪一个简单 forward/backward；随后比较 `no_grad` 与 `inference_mode`。

### Week 11：Engine、并发与 inference boundary

- 目标：理解 engine graph task/ready queue 的全局位置，并聚焦 inference mode、functionalization、mutation/view safety。
- 补课：thread、mutex/atomic、TLS、RAII guard、intrusive pointer。
- 实验：触发 inplace/version error，形成假设并用 source/runtime 证据解释。

### Week 12：allocator、device guard、stream/event、RNG、profiler、serialization、distributed

- 目标：建立 runtime subsystem 地图；理解 c10d/ProcessGroup/collective 的边界及其对 inference 的意义。
- 候选锚点：`c10/core/Allocator.*`、device guard/stream 相关目录、`torch/csrc/profiler/`、`torch/csrc/distributed/`、`torch/distributed/`。
- 实验：CPU allocator/profiler 小实验；单机最小 ProcessGroup 或只做 source/test trace（以环境为准）。
- 产物：Autograd/inference 对照链、runtime ownership 图、Phase 3 调试项目。

Gate 3：`AUTOGRAD` 的 `explain/trace` 至少 3，`RUNTIME` 与 `DISTRIBUTED` 的 `explain/locate` 至少 2；能说明 inference-only backend 仍必须处理哪些 Autograd/runtime 边界。

## Phase 4 — PyTorch 2 compiler stack（Week 13–16）

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

Gate 4：`FX-EXPORT`、`DYNAMO`、`INDUCTOR` 的 `explain/trace` 至少 3；能独立诊断一个 graph break，并说明 eager device backend 与 compiler backend 的 ownership 差异。

## Phase 5 — 扩展与 accelerator integration（Week 17–19）

### Week 17：C++/CUDA extension 与 library registration

- 目标：实现 schema、CPU kernel、可选 CUDA kernel、Meta/fake 支持、测试与 benchmark。
- 主题：ABI、build isolation、registration lifetime、error handling、opcheck/gradcheck 适用边界。
- 产物：可安装的 out-of-tree extension；不是只会复制 tutorial。

### Week 18：`PrivateUse1` eager backend prototype

- 目标：理解 device rename/module、tensor allocation、device guard、registration、fallback、serialization/RNG/stream/event 等接口的选择条件。
- 实验：在无真实硬件下建立 `VENDOR_DEVICE` abstraction，能跑的部分用 prototype，不能跑的部分用 contract test 与 architecture decision record。
- 产物：最小 prototype、unsupported matrix、negative tests。

### Week 19：`torch.compile` backend 与 OOT compatibility

- 目标：实现 `(GraphModule, example_inputs) -> callable` contract，设计 supported graph、partition/fallback、lowering/runtime boundary 和 version CI。
- 实验：代表性模型片段在 eager/reference/custom backend 上语义对比；动态 shape 与错误路径测试。
- 产物：compile backend、compatibility matrix、Phase 5 集成项目。

Gate 5：`EXTENSION`、`PRIVATEUSE1`、`COMPILE-BACKEND` 的 `modify` 至少 3，`transfer` 至少 2；明确哪些结果只是 CUDA/CPU proxy evidence，不能宣称已验证真实硬件。

## Phase 6 — 综合架构与迁移设计（Week 20）

- 重建 PyTorch 全局架构图，覆盖 Python frontend、Tensor/storage、dispatcher、ATen、Autograd、runtime、distributed、compiler、backend/testing/build。
- 对一个未预先练习的模型片段完成 eager 与 compile 双路径追踪。
- 完成 `VENDOR_DEVICE` inference adaptation blueprint：模块边界、风险、fallback、测试矩阵、性能方法、版本升级与 CI。
- 进行口试、源码定位考试、debug challenge 和 capstone review。

Final gate：关键概念 `explain/locate/trace` 至少 3；`DISPATCH`、`RUNTIME`、`COMPAT` 的 `debug/modify/transfer` 至少 3；至少一次 +14 天延迟复习通过。没有真实硬件时，结论必须标注为设计或 proxy validation。

## 范围控制

“全方位”表示理解所有主要子系统的职责、边界、关键数据结构和至少一条可执行调用链，不表示逐行读完数百万行代码。mobile/edge、quantization、sparse、MPS/XPU/ROCm、distributed algorithms、ONNX 等专题在主干完成后加入 2–6 周 extension track，由模型需求和目标 backend 决定深度。
