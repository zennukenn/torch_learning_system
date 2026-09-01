# Review queue

| Due date | Concept | Dimension | Last evidence | Hint ceiling | Retrieval prompt | Status |
|---|---|---|---|---|---|---|
| 2026-09-03 | BIND-CODEGEN | explain | E-20260902-01 | H0 | 解释 `add.Tensor` 的 `*`、variants 和 `structured_delegate`。 | deferred-prerequisite |
| 2026-09-03 | ATEN-KERNEL | explain | E-20260902-02 | H0 | 区分 meta/TensorIterator 与 generated CPU kernel 的职责。 | deferred-prerequisite |
| 2026-09-03 | DISPATCH | trace | E-20260902-03 | H0 | 补全 `torch.add` 到 CPU ufunc 的链条，并说出两个源码锚点。 | deferred-prerequisite |
| 2026-09-03 | CPP-CORE | explain | E-20260902-04 | H0 | 解释 compile/link，并说明 `const Tensor&` 实际避免什么。 | deferred-prerequisite |

这些 evidence 的原始 review date 保留以维持历史真实性。`CPP-CORE` 在 Foundation 0.7 讲授 reduced compile/link model 后恢复；其余三项在 Foundation Gate 通过后恢复，不作为近期课程入口。
