# Session log

Append one concise entry per substantive session:

## YYYY-MM-DD — session title

- Revision:
- MiniTorch revision/diff:
- Milestone/increment:
- Outcome:
- Learner artifact:
- Notebook:
- Source/runtime evidence:
- Syntax clinic:
- Assessment and hints:
- Review dates:
- Next action:

## 2026-09-02 — first `torch.add` source trace

- Revision: `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`)
- Outcome: Inspected schema, structured meta, and generated CPU ufunc evidence; learner did not independently reconstruct the chain or anchors.
- Learner artifact: [call-chain with preserved no-notes result](learning/artifacts/2026-09-02-first-add-source-trace/call-chain.md); [session note](learning/notebook/sessions/2026-09-02-first-add-source-trace.md).
- Source/runtime evidence: `native_functions.yaml:536`, `BinaryOps.cpp:151`, `torchgen/gen.py:2387`, and focused CPU codegen succeeded in 5s; runtime dispatch remains **unverified**.
- Syntax clinic: Python keyword-only `*`; C++ `const Tensor&` wrapper-copy semantics.
- Assessment and hints: `BIND-CODEGEN.explain=1`, `ATEN-KERNEL.explain=1` at H2; `DISPATCH.trace=0`, `CPP-CORE.explain=0` after failed retrieval.
- Review dates: 2026-09-03, 2026-09-05, 2026-09-09, 2026-09-16, 2026-10-02, adapted after each retrieval.
- Next action: On 2026-09-03, run a five-minute H0 retrieval of the repository roles and first `torch.add` chain before new material.

## 2026-09-02 — Foundation 0.1: PyTorch and inference basics

- Revision: `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`)
- Outcome: Independently explained Tensor/operator/Module-forward/device/training-inference and reconstructed a Linear inference example; exact source path required one H1 correction.
- Learner artifact: [foundation map](learning/artifacts/2026-09-02-foundation-01-pytorch-inference-basics/foundation-map.md); [session note](learning/notebook/sessions/2026-09-02-foundation-01-pytorch-inference-basics.md).
- Source/runtime evidence: Observed `torch/nn/modules/linear.py:130`, where `Linear.forward` returns `F.linear(input, self.weight, self.bias)`; runtime remains **unverified** because `torch` is unavailable.
- Syntax clinic: Python instance-method `self` and return type annotation `-> Tensor`, both retrieved correctly at H0.
- Assessment and hints: `PYTORCH-BASICS.explain=3`; `ARCH-MAP.explain=2`, `locate=1`; `PY-DATAMODEL.explain=1`. Concepts and flow passed at H0; source-path retrieval was partial and corrected at H1.
- Review dates: 2026-09-03, 2026-09-05, 2026-09-09, 2026-09-16, 2026-10-02, adapted after each retrieval.
- Next action: On 2026-09-03, run a five-minute H0 retrieval of today's basics and source anchor, then begin Foundation 0.2 on the Tensor minimal data model.

## 2026-09-02 — Foundation 0.2: Tensor minimal data model

- Revision: source `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`); runtime `binary:2.7.1+cu126`.
- Outcome: Independently explained element/axis/ndim/shape/dtype/device, NCHW, element counts, reshape constraints and Flatten invariants; source callee and evidence boundary needed H1/H2 correction.
- Learner artifact: [foundation map](learning/artifacts/2026-09-02-foundation-02-tensor-minimal-model/foundation-map.md); [session note](learning/notebook/sessions/2026-09-02-foundation-02-tensor-minimal-model.md).
- Source/runtime evidence: Observed `torch/nn/modules/flatten.py:51`; existing binary passed focused CPU and CUDA Flatten assertions. Binary is not the pinned source build, so v2.13 runtime remains **unverified**.
- Syntax clinic: Python default arguments, zero-based axes and negative `-1`; learner correctly identified C/axis 1 through last axis and preserved N/axis 0 at H0.
- Assessment and hints: `TENSOR-MODEL.explain=2`, `locate=1`; `PY-DATAMODEL.explain` remains 1 with new evidence. Core Tensor reasoning passed H0; direct callee was corrected H1; evidence boundary was supplied H2 and requires delayed retrieval.
- Review dates: 2026-09-03, 2026-09-05, 2026-09-09, 2026-09-16, 2026-10-02, adapted after each retrieval.
- Next action: On 2026-09-03, complete due H0 reviews, then begin Foundation 0.3 on the inference panorama.

## 2026-09-13 — MiniTorch assessment policy transition

- Revision: PyTorch reference remains `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`).
- MiniTorch revision/diff: repository not initialized; learner will author the M0 architecture/build plan first.
- Milestone/increment: M0.1 next — PyTorch→MiniTorch architecture and directory mapping.
- Outcome: Learner accepted an independent C++/CUDA MiniTorch with `minitorch` Python package, PyTorch-like engineering structure, runnable minimal coverage across major subsystems, project-driven assessment, expanded inference scope, and reduced training priority. Inference requirements now explicitly include CNN/Transformer/KV cache, CUDA memory/streams, mixed precision, compiler, inference DP and row/column TP.
- Learner artifact: accepted requirements recorded in `projects/MINITORCH_SPEC.md` and `projects/INFERENCE_SCOPE.md`; no mastery evidence awarded for requirements decisions.
- Source/runtime evidence: source checkout pin revalidated; inference ownership anchors for CUDA allocator/stream/event/graphs, modes/autocast, ProcessGroup/DDP and DeviceMesh/DTensor/tensor parallel observed at the pinned checkout; no MiniTorch build/runtime work performed.
- Syntax clinic: none.
- Assessment and hints: standalone knowledge quizzes retired prospectively; existing evidence and mistakes preserved and mapped to future project increments.
- Review dates: historical dates preserved; reviews activate inside their mapped milestones.
- Next action: learner authors the M0.1 architecture/directory mapping before repository initialization.
