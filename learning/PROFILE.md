# Learner profile

更新日期：2026-09-15

## 目标与约束

- 第一目标：全方位、深入掌握 PyTorch 架构和源码。
- 综合项目：未来为自有硬件适配 PyTorch，目标为较完整的推理兼容性。
- 目标硬件当前不可用；学习与实验先基于 CPU/CUDA。
- 未来软件栈已有算子库、通信库等，但硬件、源码、日志与 API 细节保密。
- backend 路线：C++ extension、`PrivateUse1`、out-of-tree、`torch.compile` backend 分阶段比较和实现。
- 模型兼容性、正确性、性能、内存、动态图、编译、分布式边界和可维护升级均重要；不以单纯算子覆盖率为主要指标。
- 产品只要求 inference，但学习必须理解 Autograd、训练边界和 distributed 全局位置。
- 2026-09-13 起，以独立 `mini-torch/` Git 仓库作为贯穿课程的实现项目；尽可能镜像 PyTorch 的主要目录、工程边界和命名，只缩小功能与规模。
- MiniTorch 核心不依赖官方 `torch`：C++ 实现 Tensor/Storage/operator/dispatcher/Autograd/runtime，pybind11 暴露 Python API，包名为 `minitorch`。官方 PyTorch 与 NumPy只作源码和数值 oracle。
- MiniTorch 先完成 CPU，再实现少量真实 CUDA kernel/runtime，最后以 CPU mock 驱动 MiniTorch PrivateUse 和原生 PyTorch PrivateUse1 双路线。主要子系统必须形成可运行的最小闭环，不接受只有空接口的覆盖。
- 项目以 inference 为重；只保留足以理解 Autograd 和训练边界的小型 MLP training smoke case，不把训练功能作为主要投入。
- Inference 必修范围扩展到 CNN 与 decoder-style Transformer/KV cache、`eval`/`no_grad`/inference mode、autocast/mixed precision、显存缓存与碎片/OOM、pinned transfer、stream/event/跨 stream lifetime、CUDA Graph、dynamic shapes、quantized representative path、profiling 与性能方法。
- Distributed inference 必须区分并实现两进程 inference DP、minimal DDP gradient-sync boundary 和 row/column TP；学习 DeviceMesh/DTensor placement、collectives、sharded checkpoint 与 communication/computation overlap。sequence/context/pipeline/expert parallel 先做到架构与源码层，按 capstone 模型需要再实现。
- 训练降级为 supporting track：保留最小 Autograd、SGD、MLP 和一次 gradient all-reduce；optimizer zoo、GradScaler、full DDP reducer/FSDP 与训练性能放到 inference capstone 之后。
- 第三方硬件路线同时要求：MiniTorch 自有的 PrivateUse 可插拔 backend，以及原生 PyTorch `PrivateUse1` out-of-tree adapter/prototype。
- 假定真实硬件侧最终由学习者在私有环境提供 C/C++ adapter shared library；公开仓库只保存 versioned C ABI、CPU mock、capability manifest 和 conformance tests，不保存专有接口或日志。
- MiniTorch 采用“机制完整、API 小”的规模控制：通常约 20–30 schemas、10–15 个 backend-native kernels，以 CNN、decoder Transformer 和硬件接入所需 vertical slices 为准。
- 完整路线约 547–875 focused hours，仍按证据和 9–18 个自然月的长期尺度规划；Release A 先在累计 30–50 小时内交付受限但真实的 CPU model inference，再由 Releases B/C 补齐全部已接受深度。

## 2026-09-02 重新校准的起点（不是掌握分数）

- `Tensor`、神经网络 `forward`、Autograd/`backward`：听说过，需要从直觉、用途和简单例子开始。
- CPU 与 GPU：自评能解释；后续仍用小任务验证具体边界。
- Python `class` / `import`：听说过，需要从 reduced example 系统建立执行模型。
- C++ pointer / reference：听说过；compile/link：不了解。
- 更早的 Python 5/10、C++ 3/10、深度学习 5/10、系统 3/10 是宽泛自评，不能作为进入深层源码的 prerequisite evidence。
- 数学学过线性代数、微积分、概率统计和数值计算，按实际模型/算子语境激活。

## 学习偏好

- 周投入约 20 小时；接受超出原 4–5 个月，以完整性和理解深度优先。
- 单次以 90–120 分钟为主；工作繁忙时允许缩短，但不靠赶进度跳过 gate。
- 当前偏好 architecture-first：先用类比和图建立直觉，再讲术语、代码和源码。
- 单节课目标比例约为 `60%` 详细讲解、`25%` 练习、`15%` 源码观察。
- 前期讲解需要详细、简单、由浅入深；先建立全局架构和 inference flow，再逐层放大到源码机制。
- 架构地图、垂直调用链、模块阅读和实验驱动仍需结合，但 vertical trace 在 Foundation Gate 后成为主方法。
- Python/C++ 语法在源码上下文中系统讲解，并配小练习。
- AI 先诊断再授课，使用间隔复习；主要考核改为逐步实现 MiniTorch，而不是脱离项目的知识题。
- AI 讲解并提供源码锚点、接口、必要脚手架和验收测试；学习者编写决定性实现，接受 code review、debug challenge 和无笔记 code defense。
- 教学必须紧密嵌入 MiniTorch：每讲完一个短 prerequisite block，立即由学习者创建或修改对应的 repository document、config、source 或 test，再根据真实 diff/build/failure 继续教学。即使是 Git 初始化、`.gitignore`、README 和 ADR，也希望先讲其工程意义再亲手完成。
- 不希望用连续问答或反复复述导师答案代替项目实践。开场问题只用于快速调整讲解深度；掌握度主要从 learner-authored diff、commands、tests、debug hypothesis、PyTorch source comparison 和对自己实现的简短 defense 推断。
- 希望普通会话使用紧凑 hot context，不重复加载完整 specs/roadmaps/history；完整性由结构化课程映射、按需冷加载和自动 validator 保证，而不是用每轮大量 prompt 换取安全感。
- 接受 Release A/B/C 分阶段交付：先获得可运行 CPU inference，再逐层替换 shortcut，最终仍完成全部已确认的 PyTorch/source/backend 覆盖。
- 中文讲解，English terminology、symbol、API 和代码标识保留英文。
- 工具：ChatGPT 与 Codex；Codex 可搜索、构建、调试、修改、测试并维护学习状态。

## 第一阶段期望结果

- 看懂并能用自己的话重画 PyTorch 全局架构图。
- 知道一次模型 inference 从输入、`forward`、operators 到 CPU/GPU execution 和输出会经过哪些主要模块。
- 每周约 20 小时是目标容量，会因工作变化；计划按 mastery gate 自适应，不因周投入波动惩罚或压缩基础课。

## AI 角色

按任务动态组合：architecture mentor、source navigator、Python/C++ tutor、debug coach、Socratic tutor、examiner、project mentor、learning manager、spaced-review scheduler。角色服务于证据化学习，不制造冗长的角色扮演文本。
