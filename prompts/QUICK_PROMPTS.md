# Quick prompts

总提示词已经加载后，日常只需使用下面的短入口。

如果 Codex 的 `$` 列表暂时没有显示 Skill，仍可直接说：

```text
请读取并严格遵循 .agents/skills/pytorch-source-mentor/SKILL.md，然后执行下面的学习任务：...
```

## 下一次学习

```text
读取学习状态，先处理到期复习并诊断最早薄弱前置。为我运行下一次 90–120 分钟 PyTorch 源码会话，结束时更新全部学习证据与状态。
```

## 追踪调用链

```text
在当前 exact revision 中追踪 `<API/OP>` 的 vertical call chain。先让我预测每一层，再用当前源码和一个最小 runtime experiment 验证；用 CALL_CHAIN 模板记录，不得凭记忆填路径。
```

## Python/C++ 语法门诊

```text
针对这段 PyTorch 源码做 syntax clinic：`<snippet/path:symbol>`。先诊断我卡在哪里，再解释 syntax、semantics、ownership/lifetime 和 PyTorch 设计目的，最后给 reduced example 与一个小练习。
```

## Debug 教练

```text
把这个问题作为 source-level debugging session：`<error/reproduction>`。不要直接给答案；先记录我的 hypothesis，建立可证伪假设树，用最小命令逐层验证，并把错误认识写入 ERROR_LOG。
```

## 闭卷考试

```text
根据 MASTERY 和 QUESTION_HISTORY 给我一次 45 分钟闭卷考试，避免重复原题，覆盖 explain/locate/trace/transfer。逐题记录原始答案，考试结束后统一反馈并安排复习。
```

## 周复盘

```text
执行 weekly audit：抽查一个旧知识点，审计本周是否有可执行证据，找出最早薄弱前置，判断下周 keep/slow/revise，并更新 REVIEW_QUEUE。不要因计划周数自动放行 phase gate。
```

## 源码修改项目

```text
启动当前 Phase 项目。先要求我写 problem statement、hypothesis、design、focused tests 和预计 build cost；你只做质询与 review，等我提交第一版后再给分级提示。
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
这是新对话。先读取 PROFILE、STATE、MASTERY、REVIEW_QUEUE 和最后 SESSION_LOG；用不超过 10 行复述当前证据状态和唯一下一步，不要重新询问已记录的信息。
```
