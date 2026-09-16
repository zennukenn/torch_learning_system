# Learning-system maturity audit — 2026-09-15

> Historical baseline. Superseded for current product/runtime decisions by
> `2026-09-16-product-optimization-acceptance.md`; retained to preserve the
> evidence trail that motivated the hot-context and release redesign.

## Verdict

The system is **ready for project-integrated use** and its declared curriculum
is structurally mature: all 41 mastery concepts map to pinned PyTorch source
anchors, evidence dimensions, one of 13 ordered course blocks, an immediate
learner-owned MiniTorch action and runnable gate evidence.

This verdict applies to the curriculum and mentor-control system. It does not
claim that the learner has completed the curriculum, that the current
`mini-torch/` project passes M0a, or that private hardware works. Educational
effectiveness must continue to be checked from real sessions and adjusted when
the worktree evidence exposes a weakness.

## Requirement traceability

| Requirement | Implemented control | Verification |
|---|---|---|
| Teach knowledge and immediately build MiniTorch | `project-teaching-loop.md` and interleaved `session-protocol.md` require a repository action after each 10–20 minute teaching block | completed manifests require nonempty structured `practice_cycles`; negative health test rejects their absence |
| Learner authors even early repository artifacts | Skill/spec/roadmap explicitly include maps README ADR ignore rules config source and tests in the authorship boundary | completed manifests require `authorship` and worktree evidence; current premature drafts are labeled mentor work |
| Assess from the actual project rather than oral quizzes | Diff/build/test/debug/source comparison precede one compact defense; questions are optional | example manifest dry run succeeds with zero questions; partial project prompts still enter mistakes correctly |
| Preserve architecture-first beginner support | Foundation mode keeps a stable inference map reduced examples and shallow source observations | Foundation protocol interleaves rather than removes explanation and syntax teaching |
| Cover inference from model API to hardware | `COURSE_PRACTICE_PLAN.md`, `INFERENCE_SCOPE.md`, M0–M9 and M2.5 | 28 I0 inference/backend concepts plus F0/I1/T1 supporting concepts validate against the coverage matrix |
| Retain essential non-inference architecture | bounded Autograd/SGD/MLP/gradient-sync plus distributed build testing and compiler architecture remain required | T1/I0 gates remain in M5/M6 and the coverage validator |
| Ground claims in the chosen PyTorch tree | exact source pin separate repository commands and source-symbol verification | checkout is exact `cf30153c4c131c8164ee7798e5022d810682e2cb` / `v2.13.0`; full history and 78 recursive submodules pass |
| Avoid false backend claims | dual mock/proxy routes and three evidence levels | P0–P5 specification distinguishes contract-ready device-smoke and representative-model results |

## Pedagogical quality review

### Constructive alignment

Learning outcomes, activities and assessment now use the same artifact. For
example, compile/link is taught immediately before the learner authors a CMake
target; the build result and later diagnosis assess that same knowledge. There
is no separate trivia exam standing in for the project behavior.

### Cognitive load and sequencing

- Foundation sessions retain one stable global map and introduce only the terms
  required for the next repository action.
- M0a/M0b establish Git/build/import/test success before Tensor and operator internals; M0c revisits the now-real native boundary as a debugging clinic before CUDA.
- M1 establishes ownership and numerical invariants before M2 operators.
- M2.5 produces an early top-to-bottom CPU inference model before CUDA.
- CUDA precedes CUDA model variants so asynchronous failures are not mixed with
  unknown eager semantics.
- Distributed and compiler work reuse already working models and kernels.
- PrivateUse integrates already verified eager runtime compiler and packaging
  contracts rather than serving as a shortcut.

### Authentic and formative assessment

Opening diagnostics only tune explanation depth. The primary evidence is
learner-authored work plus focused execution and hypothesis-driven debugging.
Scores remain dimension-specific; mentor code and test output alone cannot
raise them. Delayed extension/repair tests transfer and retention without
replaying the original solution.

### Feedback control

The prior failure mode was reproduced conceptually: a partial answer could lead
to repeated oral correction even though no MiniTorch artifact existed. The new
stop rule ends the oral loop after two attempts and converts the gap into a
file edit, test, source observation or delayed repair. Session records now
preserve practice cycles and provenance so this drift is auditable.

## PyTorch and inference coverage review

| Layer | Required scope | Accountable courses |
|---|---|---|
| User/model layer | package/import Python data model Module/Parameter/buffer hooks state loading eval and batching | C00 C04 C05 C07 |
| Tensor semantics | allocation ownership Storage/Tensor metadata shape stride offset view alias mutation dtype device layout promotion broadcasting numerics RNG | C02 |
| Operator execution | schema overload codegen binding Dispatcher keys registration fallback redispatch composite/native behavior | C03 |
| CPU backend | scalar reference TensorIterator-like iteration threading vectorization external math libraries determinism and benchmarking | C03–C04 |
| CUDA backend/runtime | compilation launch geometry kernels libraries allocator cache fragmentation/OOM pinned transfers device guard streams events lifetime synchronization graphs precision | C06 |
| Representative models | Linear/ReLU model CNN decoder Transformer masking attention KV-cache dynamic batch/sequence and quantized Linear | C04 C07 |
| Inference state | `eval` `no_grad` inference mode autocast serialization safe loading and repeated-request isolation | C04 C07 |
| Autograd boundary | reverse mode saved values leaves version/in-place safety minimal SGD/MLP and gradient synchronization contrast | C08 |
| Runtime/observability | allocator/TLS/thread/RNG/profiler/error/serialization state | C06 C09 |
| Distributed inference | rendezvous ProcessGroup/Work collectives timeout/failure DeviceMesh placements DP row/column TP checkpoint and optional overlap | C09 |
| Compiler | IR capture graph break Fake/meta symbolic shapes guards functionalization decomposition lowering fusion cache dynamic shapes quantized/TP behavior export/AOT | C10 |
| Accelerator integration | MiniTorch versioned C ABI plugin and native PyTorch `PrivateUse1` package including memory streams ops fallback modes profiler Fake/Meta compiler compatibility | C11 |
| Deployment/performance | wheel clean install CI AOT versions upgrades correctness latency throughput memory transfer communication compile/startup | C12 |

No known major top-to-bottom inference responsibility is absent from the
declared Core/Representative/Survey scope. “Comprehensive” means every major
responsibility has a runnable reduced mechanism or an explicitly scoped source
study; it does not mean reproducing PyTorch's complete operator zoo or every
platform backend.

## Verification executed

All commands completed successfully from the learning-system root:

```text
python3 -m py_compile scripts/validate_curriculum_coverage.py \
  scripts/record_learning_session.py scripts/system_health_check.py \
  scripts/validate_learning_state.py

python3 scripts/validate_curriculum_coverage.py --verify-symbols
  -> 41 concepts; 13 project-integrated course blocks; 28 I0 concepts; pass

python3 scripts/validate_learning_state.py
  -> 41 mastery concepts; 12 evidence rows; 12 historical question rows; pass

python3 scripts/record_learning_session.py \
  templates/SESSION_MANIFEST.example.json
  -> dry run pass with 1 evidence and 0 questions

python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  .agents/skills/pytorch-source-mentor
  -> skill valid

python3 scripts/system_health_check.py
  -> source pin/history/submodules; independent MiniTorch repository boundary;
     source anchors; curriculum/practice mapping; isolated native import;
     manifest lifecycle; negative rejection; cleanup pass

git diff --check
  -> pass

changed/new Markdown local-link scan
  -> 14 local links across 24 files; pass
```

The health check also proves that invalid I0 evidence dimensions, a course with
no immediate learner action, a session with no practice cycle, missing learner
authorship, an unknown concept, missing mistake linkage and invalid notebook
evidence are rejected.

## Remaining operational constraints

- The real `mini-torch/` repository has no commit and has not passed M0a. Its
  current README/ADR/ignore files are explicitly mentor drafts, not mastery.
- CMake, Ninja, GDB and the Python `pybind11` package are unavailable in the
  learner environment. The isolated direct-compiler native smoke passes using
  pinned vendored headers, but it does not satisfy the learner's CMake gate.
- CUDA must be rechecked at the relevant M3 session before runtime mastery or
  performance claims.
- Private third-party hardware remains unavailable; only public mock/proxy
  contract evidence can be produced here.
- The curriculum is intentionally mastery-paced. Its 580–930 hour range and
  9–18 calendar-month estimate remain planning aids, not guarantees.

These are project and environment gates rather than defects in curriculum
coverage. The next real validation of teaching quality is C00/M0a performed with
the new microcycle and learner-authored repository changes.
