# Quick prompts

总提示词已经加载后，日常只需使用下面的短入口。

如果 Codex 的 `$` 列表暂时没有显示 Skill，仍可直接说：

```text
请读取并严格遵循 .agents/skills/pytorch-source-mentor/SKILL.md，然后执行下面的学习任务：...
```

## 下一次学习

```text
读取学习状态、projects/MINITORCH_SPEC.md、projects/INFERENCE_SCOPE.md 和当前 milestone。选择唯一的 session-sized MiniTorch increment，I0 inference 优先于 T2 training extension：先讲 prerequisites 并检查固定 PyTorch revision 的对应源码，再让我提交设计和决定性实现；按 acceptance matrix 运行 focused tests、调试一个实际失败，并让我无笔记解释自己的 diff、调用路径和限制。更新 notebook、证据和状态。
```

## Inference 专题

```text
从 projects/INFERENCE_SCOPE.md 选择当前最早未完成的 I0 increment。围绕 CNN/Transformer、KV cache、mixed precision、CUDA allocator/stream、DP/TP、compiler 或 inference performance 建立 contract；先核对 pinned PyTorch ownership，再让我实现 MiniTorch 代表性闭环并用 correctness、memory、latency/throughput 或 communication evidence 验收。不要用训练扩展挤占未完成的 I0 工作。
```

## 基础架构课

```text
从 curriculum/ROADMAP.md 的当前 Foundation lesson 和 MiniTorch M0 increment 开始。先用具体 inference/build 故事和简单架构图讲清 prerequisites，再让我完成一个目录图、配置或小型 C++/binding change，运行 focused build/test，并解释自己完成的工作。不让我猜未讲过的内部机制。
```

## 追踪调用链

```text
先确认我已通过这条 trace 所需的 foundation prerequisites；否则先补前置。然后在当前 exact revision 中追踪 `<API/OP>` 的 vertical call chain，让我用已学架构模型预测每一层，再用当前源码和最小 runtime experiment 验证；用 CALL_CHAIN 模板记录，不得凭记忆填路径。
```

## Python/C++ 语法门诊

```text
针对这段 PyTorch 源码做 syntax clinic：`<snippet/path:symbol>`。先诊断我卡在哪里，再解释 syntax、semantics、ownership/lifetime 和 PyTorch 设计目的，最后给 reduced example 与一个小练习。
```

## Debug 教练

```text
把这个问题作为 source-level debugging session：`<error/reproduction>`。不要直接给答案；先记录我的 hypothesis，建立可证伪假设树，用最小命令逐层验证，并把错误认识写入 ERROR_LOG。
```

## 里程碑验收

```text
根据当前 MiniTorch milestone 做验收：检查 learner-authored diff，运行正向/边界/错误/必要的 oracle tests，让我定位并修复一个 bounded failure，再无笔记解释 contract、build/runtime path、ownership、PyTorch source 对照、简化和限制。不要出脱离项目的知识题。
```

## 周复盘

```text
执行 weekly audit：审计本周 MiniTorch commits/diffs、tests/debug 与 learner authorship；把一个旧知识点转化为小扩展、修复或代码解释，找出最早薄弱前置，判断下周 keep/slow/revise，并更新 REVIEW_QUEUE。不要因计划周数自动放行 phase gate。
```

## 笔记与错题复习

```text
读取 learning/notebook/INDEX.md、MISTAKES.md 和到期复习队列。把具备 prerequisites 的旧错题转成当前 MiniTorch 代码解释、测试、扩展或修复；不具备条件的继续 deferred。记录我的原始处理过程，再对照源码和运行证据更新状态。
```

## MiniTorch increment

```text
启动当前 MiniTorch increment。先定义 public contract、supported/unsupported、invariants、error behavior、可能修改的文件和 acceptance matrix，再要求我写 design/hypothesis。你只提供 prerequisite teaching、PyTorch anchors、最小脚手架、review、instrumentation 和分级提示，决定性逻辑由我完成。
```

## `PrivateUse1` / OOT backend

```text
以公开的 `VENDOR_DEVICE` 抽象设计 `<feature>`。严格分开 eager `PrivateUse1` backend 与 compile backend，列出 ownership、required hooks、fallback、positive/negative tests 和当前无法由真实硬件验证的部分。
```

## `torch.compile` backend

```text
围绕一个最小模型实现 custom `torch.compile` backend。先让我解释 `(GraphModule, example_inputs) -> callable` contract，再设计 supported subset、graph rejection/fallback、equivalence、dynamic-shape 与 error tests。
```

## 英文文档或 GitHub issue

```text
辅助我读这份英文资料：`<URL/text>`。先列关键术语与上下文，再区分 API contract、implementation detail、version applicability 和对当前源码学习/硬件适配的影响；重要结论回到当前 checkout 验证。
```

## 状态恢复

```text
这是新对话。先读取 PROFILE、STATE、MASTERY、REVIEW_QUEUE、notebook/INDEX 和最后 SESSION_LOG；用不超过 10 行复述当前证据状态和唯一下一步，不要重新询问已记录的信息。
```
