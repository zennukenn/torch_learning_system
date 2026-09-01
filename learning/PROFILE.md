# Learner profile

更新日期：2026-09-02

## 目标与约束

- 第一目标：全方位、深入掌握 PyTorch 架构和源码。
- 综合项目：未来为自有硬件适配 PyTorch，目标为较完整的推理兼容性。
- 目标硬件当前不可用；学习与实验先基于 CPU/CUDA。
- 未来软件栈已有算子库、通信库等，但硬件、源码、日志与 API 细节保密。
- backend 路线：C++ extension、`PrivateUse1`、out-of-tree、`torch.compile` backend 分阶段比较和实现。
- 模型兼容性、正确性、性能、内存、动态图、编译、分布式边界和可维护升级均重要；不以单纯算子覆盖率为主要指标。
- 产品只要求 inference，但学习必须理解 Autograd、训练边界和 distributed 全局位置。

## 2026-09-02 重新校准的起点（不是掌握分数）

- `Tensor`、神经网络 `forward`、Autograd/`backward`：听说过，需要从直觉、用途和简单例子开始。
- CPU 与 GPU：自评能解释；后续仍用小任务验证具体边界。
- Python `class` / `import`：听说过，需要从 reduced example 系统建立执行模型。
- C++ pointer / reference：听说过；compile/link：不了解。
- 更早的 Python 5/10、C++ 3/10、深度学习 5/10、系统 3/10 是宽泛自评，不能作为进入深层源码的 prerequisite evidence。
- 数学学过线性代数、微积分、概率统计和数值计算，按实际模型/算子语境激活。

## 学习偏好

- 周投入约 20 小时，持续 4–5 个月。
- 单次以 90–120 分钟为主；工作繁忙时允许缩短，但不靠赶进度跳过 gate。
- 当前偏好 architecture-first：先用类比和图建立直觉，再讲术语、代码和源码。
- 单节课目标比例约为 `60%` 详细讲解、`25%` 练习、`15%` 源码观察。
- 前期讲解需要详细、简单、由浅入深；先建立全局架构和 inference flow，再逐层放大到源码机制。
- 架构地图、垂直调用链、模块阅读和实验驱动仍需结合，但 vertical trace 在 Foundation Gate 后成为主方法。
- Python/C++ 语法在源码上下文中系统讲解，并配小练习。
- AI 先诊断再授课，使用间隔复习；每个大阶段完成源码修改项目。
- 中文讲解，English terminology、symbol、API 和代码标识保留英文。
- 工具：ChatGPT 与 Codex；Codex 可搜索、构建、调试、修改、测试并维护学习状态。

## 第一阶段期望结果

- 看懂并能用自己的话重画 PyTorch 全局架构图。
- 知道一次模型 inference 从输入、`forward`、operators 到 CPU/GPU execution 和输出会经过哪些主要模块。
- 每周约 20 小时是目标容量，会因工作变化；计划按 mastery gate 自适应，不因周投入波动惩罚或压缩基础课。

## AI 角色

按任务动态组合：architecture mentor、source navigator、Python/C++ tutor、debug coach、Socratic tutor、examiner、project mentor、learning manager、spaced-review scheduler。角色服务于证据化学习，不制造冗长的角色扮演文本。
