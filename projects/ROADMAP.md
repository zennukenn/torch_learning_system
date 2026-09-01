# Phase projects

所有项目先由学习者提交 hypothesis、设计草图和 focused tests。Agent 可帮助缩小范围、搭脚手架、review 和 debug，但默认不代写决定性实现。

## P0 — Build, locate, trace, patch

- 目标：建立源码开发闭环。
- 工作：固定 revision；完成 CPU-first editable build 或在资源不足时完成 binary+source 对照；选择一个小行为，添加 focused test 和一个可逆的学习 patch/instrumentation。
- 必须证明：Python 与 native source 搜索、构建/运行命令、失败诊断、diff、测试前后结果。
- 禁止：只提交仓库目录截图或纯文字架构图。

## P1 — Tensor/view semantics laboratory

- 目标：把 Tensor/storage/view 知识变为可观察行为。
- 工作：扩展 upstream test 或本地 learning test，系统覆盖 `view/reshape/clone/detach/in-place` 的 sizes、strides、storage offset、alias 和 version 行为；加一处小型 source instrumentation 或 diagnostic patch。
- 验收：能解释每个 case 的 ownership 与 mutation consequence；patch 不改变默认行为或可被干净撤销。

## P2 — Operator end-to-end

- 目标：贯通 schema、registration、dispatcher 和 kernel。
- 推荐低成本路径：先在独立 extension 以 `TORCH_LIBRARY`/`TORCH_LIBRARY_IMPL` 风格实现 CPU op、Meta/fake 行为和 tests；资源允许后再做 codegen/native-functions learning branch。
- 验收：正负测试、dispatch evidence、dtype/layout/device policy、benchmark 基线、generated/manual registration 对比说明。
- 风险：修改 `native_functions.yaml` 可能触发大量重编译，执行前必须评估当前内存和时间。

## P3 — Autograd/inference/runtime debug dossier

- 目标：从一个 inplace/view/version 或 inference-mode 问题出发做完整 debugging。
- 工作：先写错误预测与最小 reproduction；定位 Autograd/runtime 机制；添加 focused regression test 和最小 patch或 instrumentation；解释 inference-only backend 的相关义务。
- 验收：至少两条被证据排除的假设、native/Python source anchors、测试结果和延迟复述。

## P4 — Graph capture and custom compiler backend

- 目标：理解 Dynamo/FX/export/AOT/Inductor 边界，而非只会调用 `torch.compile`。
- 工作：实现一个最小 custom backend，记录 FX graph，支持一个明确子集，拒绝或 fallback 其他情况；构造 graph break、guard/recompile、dynamic shape 和错误路径 tests。
- 源码修改：在本项目 backend source 与 tests 中完成；另对 checkout 中一个 compiler test 或 diagnostic 做学习性小改动并解释其位置。
- 验收：eager equivalence、ownership diagram、日志解释、至少一个未知 graph 的 transfer task。

## P5 — Simulated out-of-tree accelerator

- 目标：为无真实硬件条件下的 `VENDOR_DEVICE` 建立可执行或 contract-driven prototype。
- 工作：分离 eager `PrivateUse1` backend 与 compile backend；定义 allocator/device guard/registration/fallback/serialization/RNG/stream-event 等能力矩阵；实现环境允许的最小路径。
- 验收：安装包结构、positive/negative tests、unsupported matrix、模型片段、fallback semantics、PyTorch version CI plan。
- 边界：不得把 CPU/CUDA proxy test 写成“真实硬件验证通过”。

## P6 — Inference adaptation capstone

- 目标：交付一份可用于未来真实硬件项目启动的公开信息版 blueprint。
- 内容：
  - PyTorch full-stack architecture map；
  - eager/compile 两种接入路线及选择准则；
  - model-first compatibility matrix；
  - correctness、memory、concurrency、profiling、performance methodology；
  - fallback/partition/error policy；
  - packaging、ABI/API versioning、cross-repository CI/upstream upgrade；
  - confidential information boundary；
  - 90 天实现里程碑与最高风险实验。
- 源码产物：在公开 CPU/CUDA proxy 环境中完成一项 learner-authored compatibility harness、focused test 或小型源码/诊断修改，并说明它如何迁移到未来 `VENDOR_DEVICE`；不能只提交架构文档。
- 最终考试：未预告 operator/model 的 source trace、debug challenge、C++ syntax reading 和 architecture defense。

## 通用质量门

- revision、commands、tests 和 observed output 可复现；
- 新增行为有正向、边界和错误测试；
- benchmark 有 warmup、同步、输入规格和对照；
- 每个设计判断区分 observed/documented/inferred；
- 学习者能在 H0/H1 下解释和迁移；
- 无 proprietary identifiers、日志、源码或硬件细节进入仓库。
