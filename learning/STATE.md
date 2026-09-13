# Current learning state

- Status: Foundation 0.2 completed; MiniTorch project-assessment transition accepted on 2026-09-13
- Current phase: Phase 0 / MiniTorch M0 — architecture, repository and build/import bootstrap
- Current week: 1 (mastery-paced; may extend without skipping the gate)
- Target stable tag: `v2.13.0`, verified against the official remote on 2026-09-01
- Source root: `sources/pytorch` (independent Git repository; ignored by the learning-system repository)
- Source checkout: complete full-history clone with 78 recursive submodule entries verified
- Commit: `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`, detached HEAD)
- MiniTorch root: `mini-torch` (planned independent Git repository; not initialized yet)
- MiniTorch import name: `minitorch`
- Runtime environment: reuse existing Conda `base` via `/root/miniconda3/bin/python`; upgraded in place to `torch 2.13.0+cu126` and `triton 3.7.1` on 2026-09-02; no duplicate environment created
- Runtime/source relation: official binary `torch.version.git_version` exactly matches pinned commit `cf30153c4c131c8164ee7798e5022d810682e2cb`; focused CPU/CUDA, Autograd, Linear, Flatten and `torch.compile(backend="eager")` smoke tests passed; see [upgrade artifact](artifacts/2026-09-02-torch-213-runtime-upgrade/environment.md)
- Last session: 2026-09-02 — Foundation 0.2; independently explained the Tensor minimal model and Flatten invariants, with H1/H2 correction for direct callee and evidence boundary
- Assessment policy: preserve all earlier question/evidence history; from 2026-09-13, use MiniTorch implementation, tests, debugging, source comparison, code defense and delayed extension as the default evidence
- Priority policy: inference I0 requirements lead the roadmap; training is limited to the T1 Autograd/MLP/minimal-DDP boundary until the inference capstone passes
- Inference scope: CNN plus decoder-style Transformer/KV cache and representative quantized Linear; CUDA kernels/libraries/caching memory/streams/events; mixed precision; compiler/dynamic shapes; two-process inference DP and row/column TP; see `projects/INFERENCE_SCOPE.md`
- Coverage audit: 41 mastery concepts mapped through `curriculum/COVERAGE_MATRIX.csv`; CPU/numerics/debug/custom-op/quantization/AOT gaps and dual PrivateUse routes added on 2026-09-13
- Hardware plan: Route A MiniTorch PrivateUse C-ABI plugin plus Route B native PyTorch PrivateUse1 OOT package; public CPU mock and private learner-supplied real adapter share a conformance suite
- Next action: start MiniTorch M0 by having the learner author the architecture/directory mapping and build plan before initializing the independent repository
- Active blockers: the official wheel is not built from local checkout changes; WSL RAM is 7.6 GiB; CMake/Ninja/GDB and Python `pybind11` package are unavailable; real third-party adapter/hardware tests must run privately, so no real-hardware claim exists yet
- Confidentiality: only public PyTorch facts and abstract `VENDOR_DEVICE` requirements may be stored

## Earliest unverified prerequisites

1. Full inference panorama across Python frontend, framework execution and hardware/runtime ownership.
2. Full global architecture map across major subsystems; only the basic Linear/Flatten paths have been demonstrated.
3. Python import/class/function/method execution model beyond `self` and a return annotation.
4. C++ source/header, compile/link and pointer/reference model.
5. Environment, debugger and source-build workflow, including CMake, pybind11, `pyproject.toml`, wheel and isolated environments.

## Next-session contract

Use architecture-first foundation mode until the Foundation Gate passes, but make MiniTorch M0 the practical spine immediately. Start each session from the global map, teach only the prerequisites needed for the current project increment, inspect the corresponding PyTorch source anchor, then let the learner produce the decisive design or code. Do not resume deep schema/codegen/dispatcher work until prerequisites and earlier MiniTorch layers exist. Close with focused tests and an unaided explanation of the learner's own change; record evidence only from learner-produced work.
