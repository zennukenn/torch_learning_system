# Learner profile

更新日期：2026-09-01

## 目标与约束

- 第一目标：全方位、深入掌握 PyTorch 架构和源码。
- 综合项目：未来为自有硬件适配 PyTorch，目标为较完整的推理兼容性。
- 目标硬件当前不可用；学习与实验先基于 CPU/CUDA。
- 未来软件栈已有算子库、通信库等，但硬件、源码、日志与 API 细节保密。
- backend 路线：C++ extension、`PrivateUse1`、out-of-tree、`torch.compile` backend 分阶段比较和实现。
- 模型兼容性、正确性、性能、内存、动态图、编译、分布式边界和可维护升级均重要；不以单纯算子覆盖率为主要指标。
- 产品只要求 inference，但学习必须理解 Autograd、训练边界和 distributed 全局位置。

## 起始自评（不是掌握证据）

- Python：5/10。
- C++：3/10。
- 深度学习：5/10。
- 系统/底层：3/10。
- 数学：学过线性代数、微积分、概率统计和数值计算。
- Linux、Git、CMake/Ninja、GDB、多线程、编译链接、库、模板/宏、CUDA、计算图、自动微分、IR：均接触过但不深入。

## 学习偏好

- 周投入约 20 小时，持续 4–5 个月。
- 单次 90–120 分钟。
- 架构地图、垂直调用链、模块阅读和实验驱动结合。
- Python/C++ 语法在源码上下文中系统讲解，并配小练习。
- AI 先诊断再授课，使用间隔复习；每个大阶段完成源码修改项目。
- 中文讲解，English terminology、symbol、API 和代码标识保留英文。
- 工具：ChatGPT 与 Codex；Codex 可搜索、构建、调试、修改、测试并维护学习状态。

## AI 角色

按任务动态组合：architecture mentor、source navigator、Python/C++ tutor、debug coach、Socratic tutor、examiner、project mentor、learning manager、spaced-review scheduler。角色服务于证据化学习，不制造冗长的角色扮演文本。
