# Current learning state

- Status: Foundation 0.2 completed with learner teach-back; architecture-first foundation curriculum active
- Current phase: Phase 0 — Foundation 0.3 next, full inference panorama
- Current week: 1 (mastery-paced; may extend without skipping the gate)
- Target stable tag: `v2.13.0`, verified against the official remote on 2026-09-01
- Source root: `sources/pytorch` (independent Git repository; ignored by the learning-system repository)
- Source checkout: complete full-history clone with 78 recursive submodule entries verified
- Commit: `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`, detached HEAD)
- Runtime environment: reuse existing Conda `base` via `/root/miniconda3/bin/python`; `torch 2.7.1+cu126`; focused CPU and CUDA Tensor/Flatten smoke tests passed on 2026-09-02
- Runtime/source relation: the installed binary is not built from the pinned `v2.13.0` checkout; record its evidence as `binary:2.7.1+cu126` and do not use it to claim revision-specific runtime behavior
- Last session: 2026-09-02 — Foundation 0.2; independently explained the Tensor minimal model and Flatten invariants, with H1/H2 correction for direct callee and evidence boundary
- Next action: on 2026-09-03 complete due H0 reviews, then begin Foundation 0.3 on `input → model.forward → operators → device execution → output` and optional branches
- Active blockers: source-aligned `v2.13.0` runtime is unavailable; WSL RAM is 7.6 GiB; CMake/Ninja/GDB are missing, so no source build or native-debug claim is available
- Confidentiality: only public PyTorch facts and abstract `VENDOR_DEVICE` requirements may be stored

## Earliest unverified prerequisites

1. Full inference panorama across Python frontend, framework execution and hardware/runtime ownership.
2. Full global architecture map across major subsystems; only the basic Linear/Flatten paths have been demonstrated.
3. Python import/class/function/method execution model beyond `self` and a return annotation.
4. C++ source/header, compile/link and pointer/reference model.
5. Environment, debugger and source-build workflow.

## Next-session contract

Use architecture-first foundation mode until the Foundation Gate passes. Start each session by placing the topic on the same global map, teach prerequisites in detailed plain Chinese, then ask questions only about material already explained. Keep source observation to about 15% and within learned layers; do not resume the deep `torch.add` schema/codegen/dispatcher trace as an active review yet. Before closing, require an unaided concept-map teach-back, audit gaps, and write evidence only from demonstrated learning.
