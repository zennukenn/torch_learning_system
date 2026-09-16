# Current learning state

- Status: Foundation 0.2 completed; MiniTorch project-assessment transition accepted on 2026-09-13
- Current phase: Phase 0 / MiniTorch M0a — fast native-import bootstrap
- Current week: 1 (mastery-paced; may extend without skipping the gate)
- Target stable tag: `v2.13.0`, verified against the official remote on 2026-09-01
- Source root: `sources/pytorch` (independent Git repository; ignored by the learning-system repository)
- Source checkout: complete full-history clone with 78 recursive submodule entries verified
- Commit: `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`, detached HEAD)
- MiniTorch root: `mini-torch` (independent Git repository initialized on 2026-09-15; no commits; current README/ADR/ignore files are mentor drafts and are not learner evidence)
- MiniTorch import name: `minitorch`
- Runtime environment: reuse existing Conda `base` via `/root/miniconda3/bin/python`; upgraded in place to `torch 2.13.0+cu126` and `triton 3.7.1` on 2026-09-02; no duplicate environment created
- Runtime/source relation: official binary `torch.version.git_version` exactly matches pinned commit `cf30153c4c131c8164ee7798e5022d810682e2cb`; focused CPU/CUDA, Autograd, Linear, Flatten and `torch.compile(backend="eager")` smoke tests passed; see [upgrade artifact](artifacts/2026-09-02-torch-213-runtime-upgrade/environment.md)
- Last session: 2026-09-02 — Foundation 0.2; independently explained the Tensor minimal model and Flatten invariants, with H1/H2 correction for direct callee and evidence boundary
- Assessment policy: preserve all earlier question/evidence history; from 2026-09-13, use MiniTorch implementation, tests, debugging, source comparison, code defense and delayed extension as the default evidence
- Priority policy: inference I0 requirements lead the roadmap; training is limited to the T1 Autograd/MLP/minimal-DDP boundary until the inference capstone passes
- Inference scope: CNN plus decoder-style Transformer/KV cache and representative quantized Linear; CUDA kernels/libraries/caching memory/streams/events; mixed precision; compiler/dynamic shapes; two-process inference DP and row/column TP; see `projects/INFERENCE_SCOPE.md`
- Coverage audit: 41 mastery concepts remain mapped; delivery is now Release A/B/C with the first restricted CPU model at 30–50 cumulative hours and full accepted scope retained
- Hardware plan: Route A MiniTorch PrivateUse C-ABI plugin plus Route B native PyTorch PrivateUse1 OOT package; public CPU mock and private learner-supplied real adapter share a conformance suite
- Next action: resume M0a with one project microcycle: teach Git tracked/generated boundaries, then have the learner inspect and materially rewrite or replace the mentor-drafted README/ADR/ignore policy before any mastery claim
- Active blockers: the 2026-09-16 read-only preflight finds C++/Python headers, pinned vendored pybind11, nvcc and GPU visibility, but CMake is the sole missing M0a-required capability; Ninja and GDB remain unavailable optional/later tools; WSL RAM is 7.6 GiB; the isolated direct-compiler fixture passes but does not satisfy the learner-owned CMake gate; real third-party adapter/hardware tests must run privately
- Confidentiality: only public PyTorch facts and abstract `VENDOR_DEVICE` requirements may be stored

## Earliest unverified prerequisites

1. Full inference panorama across Python frontend, framework execution and hardware/runtime ownership.
2. Full global architecture map across major subsystems; only the basic Linear/Flatten paths have been demonstrated.
3. Python import/class/function/method execution model beyond `self` and a return annotation.
4. C++ source/header, compile/link and pointer/reference model.
5. M0a CMake/pybind11 import workflow first; M0b adds only the local development/test loop, Release A then builds the restricted CPU model, and advanced native debugger depth follows in M0c after M1/M2 hardening.

## Next-session contract

Use architecture-first foundation mode until the Foundation Gate passes, but make MiniTorch M0a the practical spine immediately. Run short `teach -> learner edits MiniTorch -> inspect diff -> verify/debug -> source compare` cycles; do not place a long lecture or repeated oral repair loop before project work. Obtain one native import, then M0b local development tests and the Release-A CPU walking skeleton before returning to deep Tensor/Dispatcher hardening. Start each session from the generated hot brief and teach only the prerequisite needed for the next concrete repository action. Close with focused tests and one compact unaided explanation of the learner's own change; record evidence only from learner-produced work.
