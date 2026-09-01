# 学习笔记 — 2026-09-02 — 第一次 `torch.add` 源码追踪

- Status: `complete`
- Phase/week: Phase 0 / Week 0
- PyTorch revision/tag: `cf30153c4c131c8164ee7798e5022d810682e2cb` / `v2.13.0`
- Concepts: `BIND-CODEGEN`, `DISPATCH`, `ATEN-KERNEL`, `CPP-CORE`
- Evidence IDs: `E-20260902-01`, `E-20260902-02`, `E-20260902-03`, `E-20260902-04`
- Session artifact: [call-chain](../../artifacts/2026-09-02-first-add-source-trace/call-chain.md)

## 今日目标与结论

- Observable question: 在当前 revision 中，如何从 `torch.add(x, y)` 找到 schema、codegen 和 CPU 实现候选？
- Outcome: 在导师引导下检查了 `add.Tensor`/`add.out` schema、meta function 和生成的 CPU ufunc；闭卷时未能重建调用链或源码锚点。
- Runtime/build limitations: `torch`、CMake、Ninja、GDB 均不可用；只完成 source/schema/codegen evidence，runtime dispatch **unverified**。

## 我的闭卷复述（反馈前）

> 1. 不知道
>
> 2. 不知道
>
> 3. `meta function` 和 CPU kernel 的职责分别是记录计算信息和执行计算操作。
>
> `const Tensor&` 相比 `Tensor` 按值传参避免了重复申请空间。

初始诊断还包括：认为 `torch/` 是库的执行代码，`aten/` 是计算算子，`c10/` 是通信算子；不知道 `torch.add` 的调用层次，也不清楚 C++ 编译与链接。

## 查漏补缺

| 检查项 | 判断（correct/missing/incorrect/uncertain） | 证据或缺口 |
|---|---|---|
| 目标与结论 | missing | 未能闭卷表述今天回答的问题 |
| 调用链或核心机制 | missing | 未能重建 `binding → schema → dispatcher → structured/meta → generated kernel` |
| 源码锚点 | missing | 未能说出一个检查过的路径 |
| Python/C++ 语法 | partial/incorrect | 能算出 `alpha` 示例；误解 `*`，并把 `const Tensor&` 误解为避免底层空间申请 |
| 实验结果与限制 | missing | 未复述 codegen 结果或 runtime 限制 |

## 追问与修正

| Question ID | 问题 | 我的原始回答 | Hint | 我的修正后表述 | Verdict |
|---|---|---|---|---|---|
| `Q-20260902-01` | 阅读 `add.Tensor` schema | operands/return 正确；`alpha` 被当成维度；`*`、variants、delegate 不知道 | H2 | 尚未独立复述 | partial |
| `Q-20260902-02` | 区分 meta 与 CPU kernel | “记录计算信息”和“执行计算操作” | H2 | 尚需明确 shape/dtype、checks、`TensorIterator` 与 elementwise loop | partial |
| `Q-20260902-03` | 闭卷重建 `torch.add` CPU 路径和锚点 | “不知道” | H2 | 尚未修正 | fail |
| `Q-20260902-04` | 解释编译/链接与 `const Tensor&` | 编译/链接不知道；认为避免重复申请空间 | H2 | 尚未修正 | fail |

## 整理后的知识

### 我已经证明掌握的内容

- 在导师解释后，正确算出 `10 + 2 * 3 = 16`。
- 在 H2 条件下，能粗略区分 meta information handling 与 kernel execution；尚不足以独立解释。

### 导师补充（不计作掌握证据）

- `torch/` 主要包含 Python frontend 与 binding；`aten/` 包含 operator schema、native implementation 和 kernels；`c10/` 提供 tensor/dispatcher 等底层 core infrastructure。通信主要位于 `torch/distributed/` 与 `torch/csrc/distributed/`。
- 第一版链条是 `generated binding → add.Tensor schema → dispatcher → structured/meta/TensorIterator → add_stub → generated dtype dispatch → cpu_kernel[_vec] → ufunc::add`。
- `const Tensor&` 避免复制 `Tensor` wrapper 和相应引用计数操作；按值复制也不会复制底层 tensor storage。

## 源码与验证地图

| 层/主题 | Symbol/path/command | 它证明什么 | Observed/Documented/Inferred |
|---|---|---|---|
| Schema | `aten/src/ATen/native/native_functions.yaml:536` | `add.Tensor` schema、structured delegate、variants | Observed |
| Meta | `aten/src/ATen/native/BinaryOps.cpp:151` | 构造 binary iterator 并检查 `alpha` | Observed |
| Generator | `torchgen/gen.py:2387` | 为 structured ufunc 生成 CPU sources | Observed |
| CPU generation | focused `python3 -m torchgen.gen ...` | 生成 dtype cases、CPU loop 和 stub registration | Observed |
| Runtime dispatch | not run | CPU key selection and result execution | Unverified |

## Python/C++ 语法卡

- Construct: Python keyword-only `*`; C++ `const Tensor&`。
- Semantics: `*` 后参数必须使用关键字；`const&` 是只读引用，避免 wrapper copy。
- PyTorch purpose: 稳定 operator API；降低 wrapper/refcount 开销并表达 non-mutating intent。
- 我的练习结果: `alpha` 算例正确；两种语法都未通过闭卷解释。

## 错题与未解决问题

- Misconception: `c10` 被误认为通信算子；`Tensor` 按值传递被误认为复制底层数据空间。
- Correction evidence: checkout 中的 `c10/core/DispatchKey.h` 等 core anchors，以及 `Tensor` wrapper/`const&` 的导师说明。
- Still unverified: generated Python binding、真实 `DispatchKeySet`、runtime dispatch、output/storage effects、编译/链接心智模型。

## 复习安排

- Review dates: 2026-09-03, 2026-09-05, 2026-09-09, 2026-09-16, 2026-10-02（以后续表现调整）。
- Retrieval prompt: 不看笔记补全 `torch.add → binding → schema → dispatcher → meta/TensorIterator → generated CPU kernel`，并说出两个源码锚点。
- Exactly one next action: 2026-09-03 先做 5 分钟 H0 检索，再继续 Phase 0。
