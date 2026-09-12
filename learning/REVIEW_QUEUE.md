# Review queue

| Due date | Concept | Dimension | Last evidence | Hint ceiling | Retrieval prompt | Status |
|---|---|---|---|---|---|---|
| 2026-09-03 | BIND-CODEGEN | explain | E-20260902-01 | H0 | 在 M2 schema/codegen increment 中解释 `add.Tensor` 的 `*`、variants 和 `structured_delegate`，并指出 MiniTorch 简化。 | deferred-to-M2 |
| 2026-09-03 | ATEN-KERNEL | explain | E-20260902-02 | H0 | 在 M2 kernel increment 中用自己的实现区分 meta/TensorIterator 与 generated CPU kernel 职责。 | deferred-to-M2 |
| 2026-09-03 | DISPATCH | trace | E-20260902-03 | H0 | 在 M2 中先追踪自己的 elementwise op，再补全 `torch.add` 到 CPU ufunc 链和源码对照。 | deferred-to-M2 |
| 2026-09-03 | CPP-CORE | explain | E-20260902-04 | H0 | 在 M0 native build increment 中解释自己的 compile/link path；`const Tensor&` 在 M1 Tensor handle 中复测。 | active-in-M0/M1 |
| 2026-09-03 | PYTORCH-BASICS | explain | E-20260902-05 | H0 | 在 M0 目录架构图中放置 Tensor、operator、Module/forward、device、training 和 inference。 | active-in-M0 |
| 2026-09-03 | ARCH-MAP | explain | E-20260902-06 | H0 | 用目标 CNN inference 说明 MiniTorch 各里程碑最终如何连接 input 到 output。 | active-in-M0 |
| 2026-09-03 | ARCH-MAP | locate | E-20260902-07 | H0 | 在 M0 目录 mapping 中定位真实 `Linear.forward` 与计划中的 MiniTorch frontend 位置。 | active-in-M0 |
| 2026-09-03 | PY-DATAMODEL | explain | E-20260902-08 | H0 | 在 M0 `minitorch` import/binding code 中解释 method、`self` 和 type annotation。 | active-in-M0 |
| 2026-09-03 | TENSOR-MODEL | explain | E-20260902-09 | H0 | 在 M1 Tensor tests 中用 shape/dtype/device 与 NCHW Flatten 建立 cases。 | deferred-to-M1 |
| 2026-09-03 | TENSOR-MODEL | locate | E-20260902-10 | H0 | 在 M1/M4 实现 Flatten 时对照 `Flatten.forward` 和 direct callee。 | deferred-to-M1/M4 |
| 2026-09-03 | TENSOR-MODEL | explain | E-20260902-11 | H0 | 在首个 MiniTorch runtime test 中区分 MiniTorch、pinned PyTorch source 和 official binary evidence。 | active-in-M0 |
| 2026-09-03 | PY-DATAMODEL | explain | E-20260902-12 | H0 | 在 M1/M4 的 Flatten API 和 tests 中解释 defaults 与 zero-based/negative axis。 | deferred-to-M1/M4 |

这些 evidence 的原始 review date 保留以维持历史真实性。2026-09-13 assessment transition 后不再逐条口头复测；每条都已映射到 MiniTorch implementation、test、source comparison 或 code defense。只有 prerequisites 与对应 milestone 到达时才激活，新的完成证据不会覆盖原始回答。
