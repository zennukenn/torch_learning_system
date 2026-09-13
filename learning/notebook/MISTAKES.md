# PyTorch 错题本

这里汇总 `QUESTION_HISTORY.csv` 中 verdict 为 `partial` 或 `fail` 的题目，保留原始回答、纠正证据和后续复测。错题解决后不删除，只更新状态并链接新的 retrieval evidence。

| Question ID | Date | Concept | Question | Original answer/error | Correction evidence | Evidence | Next review | Status | Session note |
|---|---|---|---|---|---|---|---|---|---|
| Q-20260902-01 | 2026-09-02 | BIND-CODEGEN | Read `add.Tensor` schema | Misread `alpha` and `*`; variants/delegate unknown | `native_functions.yaml:536` and mentor supplement | E-20260902-01 | 2026-09-03 | open | [note](sessions/2026-09-02-first-add-source-trace.md) |
| Q-20260902-02 | 2026-09-02 | ATEN-KERNEL | Distinguish meta and kernel | Only vague information/execution distinction | `BinaryOps.cpp:151` and focused generated CPU sources | E-20260902-02 | 2026-09-03 | open | [note](sessions/2026-09-02-first-add-source-trace.md) |
| Q-20260902-03 | 2026-09-02 | DISPATCH | Reconstruct CPU chain and anchors | Unknown | call-chain artifact | E-20260902-03 | 2026-09-03 | open | [note](sessions/2026-09-02-first-add-source-trace.md) |
| Q-20260902-04 | 2026-09-02 | CPP-CORE | Compile/link and `const Tensor&` | Unknown; confused wrapper copy with storage allocation | `BinaryOps.cpp:151` and mentor supplement | E-20260902-04 | 2026-09-03 | open | [note](sessions/2026-09-02-first-add-source-trace.md) |
| Q-20260902-07 | 2026-09-02 | ARCH-MAP | Recall `Linear.forward` source file and direct callee | Recalled `F.linear`; called it the last function in the class instead of giving a path | Corrected after H1 to `torch/nn/modules/linear.py` and `F.linear` | E-20260902-07 | 2026-09-03 | review | [note](sessions/2026-09-02-foundation-01-pytorch-inference-basics.md) |
| Q-20260902-10 | 2026-09-02 | TENSOR-MODEL | Recall `Flatten.forward` source file and direct callee | Located the file but said `forward` was the callee | Corrected after H1 to `input.flatten(self.start_dim, self.end_dim)` | E-20260902-10 | 2026-09-03 | review | [note](sessions/2026-09-02-foundation-02-tensor-minimal-model.md) |
| Q-20260902-11 | 2026-09-02 | TENSOR-MODEL | Separate source and installed-binary runtime evidence | Omitted the verification boundary in the first teach-back | After H2 separated source direct-callee evidence from binary runtime and unverified pinned runtime | E-20260902-11 | 2026-09-03 | open | [note](sessions/2026-09-02-foundation-02-tensor-minimal-model.md) |
<!-- SESSION_MISTAKE_ROWS -->
