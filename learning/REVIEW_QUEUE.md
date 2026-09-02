# Review queue

| Due date | Concept | Dimension | Last evidence | Hint ceiling | Retrieval prompt | Status |
|---|---|---|---|---|---|---|
| 2026-09-03 | BIND-CODEGEN | explain | E-20260902-01 | H0 | 解释 `add.Tensor` 的 `*`、variants 和 `structured_delegate`。 | deferred-prerequisite |
| 2026-09-03 | ATEN-KERNEL | explain | E-20260902-02 | H0 | 区分 meta/TensorIterator 与 generated CPU kernel 的职责。 | deferred-prerequisite |
| 2026-09-03 | DISPATCH | trace | E-20260902-03 | H0 | 补全 `torch.add` 到 CPU ufunc 的链条，并说出两个源码锚点。 | deferred-prerequisite |
| 2026-09-03 | CPP-CORE | explain | E-20260902-04 | H0 | 解释 compile/link，并说明 `const Tensor&` 实际避免什么。 | deferred-prerequisite |
| 2026-09-03 | PYTORCH-BASICS | explain | E-20260902-05 | H0 | 不看笔记解释 Tensor、operator、Module/forward、device、training 和 inference。 | scheduled |
| 2026-09-03 | ARCH-MAP | explain | E-20260902-06 | H0 | 用一个 Linear 例子复述 input 到 output 的高层顺序。 | scheduled |
| 2026-09-03 | ARCH-MAP | locate | E-20260902-07 | H0 | 写出 `Linear.forward` 的源码路径和 direct Python callee。 | scheduled |
| 2026-09-03 | PY-DATAMODEL | explain | E-20260902-08 | H0 | 解释 method signature 中的 `self` 与 `-> Tensor`。 | scheduled |
| 2026-09-03 | TENSOR-MODEL | explain | E-20260902-09 | H0 | 解释 element/axis/ndim/shape/dtype/device，并推导一个 NCHW Flatten 输出。 | scheduled |
| 2026-09-03 | TENSOR-MODEL | locate | E-20260902-10 | H0 | 写出 `Flatten.forward` 的源码路径和 direct callee。 | scheduled |
| 2026-09-03 | TENSOR-MODEL | explain | E-20260902-11 | H0 | 区分 source evidence、installed-binary runtime evidence 和仍未验证项。 | scheduled |
| 2026-09-03 | PY-DATAMODEL | explain | E-20260902-12 | H0 | 解释 `start_dim=1`、`end_dim=-1` 和 zero-based axis。 | scheduled |

这些 evidence 的原始 review date 保留以维持历史真实性。`CPP-CORE` 在 Foundation 0.7 讲授 reduced compile/link model 后恢复；其余三项在 Foundation Gate 通过后恢复，不作为近期课程入口。
