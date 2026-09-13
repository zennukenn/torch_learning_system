# Review queue

| Due policy | Activation milestone | Eligible after | Concept | Dimension | Last evidence | Hint ceiling | Retrieval prompt | Status |
|---|---|---|---|---|---|---|---|---|
| activation + 7d | M2 | schema parser introduced | BIND-CODEGEN | explain | E-20260902-01 | H0 | 在 M2 schema/codegen increment 中解释 `add.Tensor` 的 `*`、variants 和 `structured_delegate`，并指出 MiniTorch 简化。 | waiting-prerequisite |
| activation + 7d | M2 | first generated CPU kernel | ATEN-KERNEL | explain | E-20260902-02 | H0 | 在 M2 kernel increment 中用自己的实现区分 meta/TensorIterator 与 generated CPU kernel 职责。 | waiting-prerequisite |
| activation + 7d | M2 | first registered elementwise op | DISPATCH | trace | E-20260902-03 | H0 | 在 M2 中先追踪自己的 elementwise op，再补全 `torch.add` 到 CPU ufunc 链和源码对照。 | waiting-prerequisite |
| activation + 7d | M0a/M1 | native target or Tensor handle introduced | CPP-CORE | explain | E-20260902-04 | H0 | 在 M0a 解释自己的 compile/link path；`const Tensor&` 在 M1 Tensor handle 中复测。 | eligible-M0a |
| activation + 7d | M0a | architecture map drafted | PYTORCH-BASICS | explain | E-20260902-05 | H0 | 在 M0a 目录架构图中放置 Tensor、operator、Module/forward、device、training 和 inference。 | eligible-M0a |
| activation + 7d | M0a | architecture map drafted | ARCH-MAP | explain | E-20260902-06 | H0 | 用目标 CNN inference 说明 MiniTorch 各里程碑最终如何连接 input 到 output。 | eligible-M0a |
| activation + 7d | M0a | directory mapping drafted | ARCH-MAP | locate | E-20260902-07 | H0 | 在 M0a 目录 mapping 中定位真实 `Linear.forward` 与计划中的 MiniTorch frontend 位置。 | eligible-M0a |
| activation + 7d | M0a | `minitorch` import package exists | PY-DATAMODEL | explain | E-20260902-08 | H0 | 在 M0a `minitorch` import/binding code 中解释 method、`self` 和 type annotation。 | eligible-M0a |
| activation + 7d | M1 | Tensor construction tests exist | TENSOR-MODEL | explain | E-20260902-09 | H0 | 在 M1 Tensor tests 中用 shape/dtype/device 与 NCHW Flatten 建立 cases。 | waiting-prerequisite |
| activation + 7d | M1/M4 | Flatten API is implemented | TENSOR-MODEL | locate | E-20260902-10 | H0 | 在 M1/M4 实现 Flatten 时对照 `Flatten.forward` 和 direct callee。 | waiting-prerequisite |
| activation + 7d | M0a | first native runtime test passes | TENSOR-MODEL | explain | E-20260902-11 | H0 | 在首个 MiniTorch runtime test 中区分 MiniTorch、pinned PyTorch source 和 official binary evidence。 | eligible-M0a |
| activation + 7d | M1/M4 | Flatten API is implemented | PY-DATAMODEL | explain | E-20260902-12 | H0 | 在 M1/M4 的 Flatten API 和 tests 中解释 defaults 与 zero-based/negative axis。 | waiting-prerequisite |
<!-- SESSION_REVIEW_ROWS -->

原始 review date 保留在 immutable evidence/question rows 中。队列使用 activation milestone 和 prerequisite 决定何时开始计算 due date，避免把尚未具备先修条件的项目复习误报为逾期。2026-09-13 assessment transition 后不再逐条口头复测；新的完成证据不会覆盖原始回答。
