# PyTorch 学习笔记本

这里保存面向学习者阅读的长期笔记。每次完整学习会话必须先由学习者闭卷复述，再由 Agent 查漏补缺并生成一篇 session note；AI 补充内容与学习者已证明掌握的内容必须分开。

机器可校验的原始证据仍以 `EVIDENCE_LOG.csv`、`QUESTION_HISTORY.csv` 和 `MASTERY.csv` 为准。本笔记本负责把它们组织成可复习的知识记录。

## 最近会话

| Date | Status | Phase | Topic | Concepts | Evidence | Note |
|---|---|---|---|---|---|---|
| 2026-09-02 | complete | Phase 0 | Foundation 0.2 — Tensor minimal data model | TENSOR-MODEL, PY-DATAMODEL | E-20260902-09..12 | [session note](sessions/2026-09-02-foundation-02-tensor-minimal-model.md) |
| 2026-09-02 | complete | Phase 0 | Foundation 0.1 — PyTorch and inference basics | PYTORCH-BASICS, ARCH-MAP, PY-DATAMODEL | E-20260902-05..08 | [session note](sessions/2026-09-02-foundation-01-pytorch-inference-basics.md) |
| 2026-09-02 | complete | Phase 0 | First `torch.add` source trace | BIND-CODEGEN, DISPATCH, ATEN-KERNEL, CPP-CORE | E-20260902-01..04 | [session note](sessions/2026-09-02-first-add-source-trace.md) |

## 主题导航

主题笔记只在同一机制经过多次验证后整理，不能用 AI 总结代替 session evidence。

| Topic | Verified sessions | Topic note | Current weak point |
|---|---|---|---|

## 使用规则

- Session notes：`learning/notebook/sessions/YYYY-MM-DD-short-session-name.md`。
- 所有 `partial` 或 `fail` 题目同时进入 [错题本](MISTAKES.md)。
- 保留原始复述、原始错误答案和后来修正，不覆盖历史。
- 笔记中的 source claim 必须带 exact PyTorch revision 与可核验 anchor。
- `mentor supplement` 不自动提高 mastery；必须通过之后的无提示复述或迁移任务。
