# Current learning state

- Status: entry baseline recalibrated; architecture-first foundation curriculum selected
- Current phase: Phase 0 — Foundation 0.1, PyTorch purpose and inference panorama
- Current week: 1 (mastery-paced; may extend without skipping the gate)
- Target stable tag: `v2.13.0`, verified against the official remote on 2026-09-01
- Source root: `sources/pytorch` (independent Git repository; ignored by the learning-system repository)
- Source checkout: complete full-history clone with 78 recursive submodule entries verified
- Commit: `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`, detached HEAD)
- Last session: 2026-09-02 — first `torch.add` source trace; source/codegen evidence only, independent reconstruction not yet demonstrated
- Next action: run a 90–120 minute Foundation 0.1 lesson on Tensor/operator/Module-forward/device/training-inference and the high-level inference flow, using 60% explanation, 25% practice and 15% shallow source observation
- Active blockers: WSL RAM 7.6 GiB; GPU access blocked; CMake/Ninja/GDB missing; `torch` not installed
- Confidentiality: only public PyTorch facts and abstract `VENDOR_DEVICE` requirements may be stored

## Earliest unverified prerequisites

1. Basic PyTorch vocabulary: Tensor, operator, Module/forward, device, training and inference.
2. Global inference and architecture map before subsystem internals.
3. Python import/class/function/method execution model.
4. C++ source/header, compile/link and pointer/reference model.
5. Environment, debugger and source-build workflow.

## Next-session contract

Use architecture-first foundation mode until the Foundation Gate passes. Start each session by placing the topic on the same global map, teach prerequisites in detailed plain Chinese, then ask questions only about material already explained. Keep source observation to about 15% and within learned layers; do not resume the deep `torch.add` schema/codegen/dispatcher trace as an active review yet. Before closing, require an unaided concept-map teach-back, audit gaps, and write evidence only from demonstrated learning.
