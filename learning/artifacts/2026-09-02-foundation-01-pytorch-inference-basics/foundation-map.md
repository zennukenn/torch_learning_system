# Foundation map — PyTorch purpose and inference basics

- Date/revision: 2026-09-02 / `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`)
- Foundation lesson: Foundation 0.1
- Observable learner outcome: Explain Tensor, operator, Module/forward, device, training/inference and place them in one inference example.
- Teaching balance: approximately 60% explanation / 25% practice / 15% source observation

## Starting point

- Learner's initial explanation: “tensor是一个向量对象，相比于数字他有维度信息和计算方式，相比于list 他有独特的操作。input是输入，input通过model中的计算得到output，model里面包含了一些神经网络，比如线性层 attention moe等，本质就是对向量做一些计算来得到概率分布。training就是反向传播神经网络，使model能够拟合数据特征。inference使前向传播神经网络，输入input通过model得到概率。”
- Known prerequisites: Could already describe input → model → output and name common neural-network layers.
- Earliest missing prerequisite: Tensor dimensionality, general model-output semantics, and the distinction between backward gradient computation and parameter update.

## Current zoom

```text
user/Python input
      ↓
Tensor → Module call → forward → operators
      ↓
execution on a compatible device
      ↓
output Tensor

training:  forward → loss → gradients → parameter update
inference: fixed parameters → forward → output
```

Dispatcher, code generation, kernels, compiler internals and Autograd internals were explicitly postponed.

## Vocabulary

| Term | Plain-language meaning | Concrete example | Place in the map | Learner restatement |
|---|---|---|---|---|
| Tensor | Multidimensional data object with metadata such as shape, dtype and device | A `(2, 3)` input matrix | Input/intermediate/output data | “多维数组，是 PyTorch 中保存数据的基本对象” |
| operator | A concrete tensor computation | add, matrix multiplication, ReLU | Computation used by forward | “具体的数学运算” |
| Module | An object that organizes computation, parameters and submodules | `nn.Linear` | Model structure | “对一组运算和参数的封装” |
| forward | Defines how a Module transforms input into output | `Linear.forward` | Module execution description | “定义一个 Module 接收到输入后，如何计算输出” |
| device | Where tensor data and compatible computation live | CPU or CUDA GPU | Hardware/runtime side | “Tensor 或模型实际存放、计算的位置” |
| training | Forward, loss, gradient computation and parameter update | `backward()` followed by `optimizer.step()` | Learning path | Correctly separated gradient computation from update |
| inference | Use fixed learned parameters to compute an output | A Linear layer producing an output Tensor | Serving/use path | “通常只做 forward……不更新参数” |

## Concrete inference story

- Input: A `(2, 3)` Tensor `x`.
- Ordered events: `x` → call `nn.Linear(3, 2)` Module → enter `forward` → call linear computation with `weight` and `bias` → return `y`.
- Output: A `(2, 2)` Tensor `y`; it need not itself be a probability distribution.
- What PyTorch owns: Tensor/Module/operator abstractions and orchestration of execution.
- What hardware/runtime owns: Performing the compatible numerical work on CPU/GPU; deeper runtime ownership is postponed.

## Practice

- Classification/ordering/explanation task: Infer shapes and roles; order the training loop; distinguish external input from parameters; identify the direct Python callee.
- Learner's original answer: Correctly gave `x.shape=(2,3)`, `y.shape=(2,2)`, classified `nn.Linear` as Module, ordered forward → loss → gradients → update, required compatible device placement, and identified `input` versus `weight`/`bias`.
- Hint level: H0 for concepts and inference flow; H1 for the exact source path correction.
- Corrected learner restatement: “在`torch/nn/modules/linear.py`中，`Linear.forward` 把计算交给 `F.linear`。”

## Shallow source observation

- Anchor: `torch/nn/modules/linear.py:130`
- What was observed: `Linear.forward(self, input: Tensor) -> Tensor` directly returns `F.linear(input, self.weight, self.bias)`.
- Focused command/check: `rg -n '^class Linear|^    def forward|return F\.linear' sources/pytorch/torch/nn/modules/linear.py`
- Limitation: Static source evidence only. `torch` is not installed, so runtime behavior, device execution and the path below `F.linear` remain **unverified**.

## Learner's no-notes map

> Tensor：多维数组，是 PyTorch 中保存数据的基本对象，比如输入、权重、输出。
>
> operator：具体的数学运算，如加法、矩阵乘法、ReLU。
>
> Module：对一组运算和参数的封装，例如 `nn.Linear`、`nn.Conv2d`。
>
> forward：定义一个 `Module` 接收到输入后，如何计算输出。
>
> device：Tensor 或模型实际存放、计算的位置，例如 CPU、CUDA GPU。
>
> `x`（Tensor）→ 调用 `layer`（Module）→ 进入 `forward` → 执行 linear operator → 使用 `weight` 和 `bias` 计算 → 得到输出 Tensor `y`。
>
> Training 需要计算 loss、求梯度并更新 parameters；inference 通常只做 forward，得到预测结果，不更新参数。`backward()` 是计算梯度；`optimizer.step()` 才是利用梯度更新 parameters。
>
> `self`：当前这个 `Module` 对象本身，例如可以通过 `self.weight` 访问它的参数。`-> Tensor`：Python 的返回值类型标注，表示这个函数预期返回一个 `Tensor`。

For the initial source-location retrieval, the learner answered “linear类里最后一个函数”; after an H1 directory/filename cue, the learner supplied the corrected path quoted above.

## Gap audit

- Correct: All seven vocabulary roles; `(2,3) → Linear(3,2) → (2,2)`; training/inference boundary; backward versus optimizer update; input versus parameters; `self`; return annotation; direct `F.linear` callee.
- Missing: Exact source file path on the first no-notes attempt.
- Incorrect: The initial “last function” description was not a verifiable source location and was factually inaccurate for the file.
- Uncertain: Learner reported no remaining uncertainty.
- Explicitly postponed details: `Module.__call__`, dispatcher, codegen, concrete kernels, detailed Autograd, compiler and distributed internals.
- Next prerequisite: Foundation 0.2 — Tensor shape, dtype and device as a minimal data model.
