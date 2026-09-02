# Foundation map — Tensor minimal data model

- Date/revision: 2026-09-02 / source `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`); runtime `binary:2.7.1+cu126`
- Foundation lesson: Foundation 0.2
- Observable learner outcome: Explain a Tensor through elements, axes, shape, dtype and device; reason about a simple flatten transformation and its evidence boundary.
- Teaching balance: approximately 60% explanation / 25% practice / 15% source and focused runtime observation

## Starting point

- Learner's initial explanation: For `(8,3,224,224)`, “8 代表张数，3 代表rgb，224, 224 是rgb的值。dtype 是tensor的数据类型，device 是存在的硬件”。
- Known prerequisites: Could identify batch and channel counts and had a first vocabulary-level distinction for dtype/device.
- Earliest missing prerequisite: Shape positions count locations rather than hold pixel values; device identifies tensor placement rather than being the hardware object itself.

## Current zoom

```text
user data
   ↓
Tensor = elements arranged along axes
         + shape / dtype / device metadata
   ↓
Module.forward → operators → compatible device execution → output Tensor
```

`TensorImpl`, `StorageImpl`, stride/view ownership and allocator details were explicitly postponed.

## Vocabulary

| Term | Plain-language meaning | Concrete example | Place in the map | Learner restatement |
|---|---|---|---|---|
| element | One stored value | One channel value at one image position | Tensor contents | “单个数” |
| axis/dimension | One direction used to organize elements | N, C, H or W | Tensor structure | “维度” |
| ndim | Number of axes | NCHW has four axes | Tensor metadata | “维度数” |
| shape | Size of every axis | `(4,3,32,64)` | Tensor metadata | “各维大小” |
| dtype | Representation/type of every element | `float32` | Tensor metadata and operation contract | “数据类型” |
| device | Device placement of tensor data and compatible execution | `cpu` or CUDA | Runtime/hardware boundary | “所在设备” |
| flatten | Merge a contiguous range of axes while preserving element count | `(4,3,32,64) → (4,6144)` | Shape transformation | Correctly identified changed/preserved properties |

## Concrete inference story

- Input: Image batch with `shape=(4,3,32,64)`, `dtype=float32`, `device=cpu`.
- Ordered events: Interpret NCHW → count 24,576 elements → default `nn.Flatten` preserves axis 0 and merges axes 1..-1 → output `(4,6144)`.
- Output: Same number of elements, dtype and device; different shape and ndim.
- What PyTorch owns: Tensor metadata, `nn.Flatten` Module API and the `input.flatten` operation.
- What hardware/runtime owns: Actual CPU/CUDA execution in the installed binary; version-specific native details were not traced.

## Practice

- Classification/ordering/explanation task: Interpret NCHW, calculate element counts, decide legal reshape targets, distinguish dtype/device, and derive default/non-default Flatten output shapes.
- Learner's original answer: Correctly calculated `(2,3,4)` as 3 axes/24 elements, accepted `(2,12)` and rejected `(5,5)`, preserved batch axis during flatten, and distinguished dtype from device.
- Hint level: H0 for Tensor reasoning; H1 to correct the direct callee; H2 for immediate source-versus-binary evidence restatement.
- Corrected learner restatements: “在 `torch/nn/modules/flatten.py` 中，`Flatten.forward` 把工作直接交给 `input.flatten(self.start_dim, self.end_dim)`”; “从 C，N 被保留”。

## Shallow source observation

- Anchor: `torch/nn/modules/flatten.py:12`, `torch/nn/modules/flatten.py:51`
- What was observed: `Flatten` stores `start_dim`/`end_dim`; `forward` directly calls `input.flatten(self.start_dim, self.end_dim)`.
- Focused command/check: `rg -n '^class Flatten|^    def forward|return input\.flatten' sources/pytorch/torch/nn/modules/flatten.py`
- Runtime verification: Existing `/root/miniconda3/bin/python` with `torch 2.7.1+cu126` produced `(4,3,32,64) → (4,6144)` on CPU and a small CUDA case; dtype, device and `numel` were preserved.
- Limitation: The binary was not built from the pinned `v2.13.0` checkout, so it does not verify revision-specific `v2.13.0` runtime behavior or the implementation below `input.flatten`.

## Learner's no-notes map

> `element`：单个数；`axis/dimension`：维度；`ndim`：维度数；`shape`：各维大小；`dtype`：数据类型；`device`：所在设备。scalar 0维，vector 1维，matrix 2维。
>
> `(4,3,32,64)`：`N=4` 张图，`C=3` 通道，`H=32`，`W=64`。总 elements = `4×3×32×64=24576`。
>
> `nn.Flatten()` → `(4,6144)`。改变：`shape`、`ndim`；不变：元素总数、`dtype`、`device`。
>
> 源码：`torch/nn/modules/flatten.py`。直接 callee：`input.flatten()`。`start_dim=1`：从第 1 维开始；`end_dim=-1`：到最后一维。没有不清楚。

Focused follow-ups established that `start_dim=1` means axis 1 (`C`) rather than the first axis (`N`), and that axis 0 (`N`) remains. The learner first omitted the evidence limitation. After the source/binary distinction was explicitly taught, the learner restated it accurately.

## Gap audit

- Correct: Definitions, scalar/vector/matrix dimensionality, NCHW meanings, element count, legal reshape reasoning, default Flatten output, changed/preserved properties, source path, negative last-axis meaning, and final evidence distinction.
- Missing: The first teach-back omitted the runtime/source evidence boundary.
- Incorrect: Initially called `forward` the direct callee; initially used the ambiguous phrase “第 1 维” before correctly identifying `C`/axis 1.
- Uncertain: Learner reported no remaining uncertainty.
- Explicitly postponed details: Storage ownership, view/copy decision, strides, allocator, dispatcher and native kernels.
- Next prerequisite: Foundation 0.3 — reconstruct the full inference panorama and place optional Autograd/compiler/distributed branches.
