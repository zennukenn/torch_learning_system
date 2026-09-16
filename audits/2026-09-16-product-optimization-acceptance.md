# Product optimization and acceptance audit — 2026-09-16

## Verdict

The learning system preserves its accepted PyTorch/source/backend coverage but
is now materially cheaper and clearer to operate. It is ready for ordinary
project-integrated sessions through a generated hot-context entrypoint. The
curriculum/system verdict does not claim that the learner has passed M0a or that
real private hardware works.

## Requirement preservation

- All 41 mastery concepts remain present and mapped to pinned-source anchors,
  milestone ownership, evidence dimensions and an immediate learner action.
- All 28 I0 inference/backend concepts remain required; the minimal T1
  Autograd/SGD/MLP/gradient-sync boundary is unchanged.
- CNN, decoder attention/KV cache, numerics, CPU/CUDA runtime and memory,
  mixed precision, quantization, distributed inference DP/TP, compiler/AOT,
  deployment, MiniTorch PrivateUse and native PyTorch `PrivateUse1` remain in
  scope.
- Learner authorship, project evidence, pinned-source comparison, real-result
  debugging, compact defense and delayed transfer/retention remain required.

The optimization changes delivery and context routing, not accepted mastery.

## Product and curriculum redesign

### Faster time to value

The previous sequence delayed the first model until approximately 135–220
focused hours. The canonical course map now defines three independently useful
releases:

| Release | Outcome | Courses | Increment | Cumulative |
|---|---|---|---:|---:|
| A | restricted but real CPU inference | C00–C02 | 30–50 h | 30–50 h |
| B | robust eager CPU/CUDA inference engine | C03–C07 | 217–340 h | 247–390 h |
| C | full source/backend mastery | C08–C12 | 300–485 h | 547–875 h |

Release A uses explicit contiguous-FP32 and manual-op restrictions. M1/M2 must
replace that debt and rerun the same model tests before CUDA. Basic pybind
module/ownership concepts are taught at first use; GIL, exception, ABI/RPATH,
debugger and sanitizer depth remains the later M0c clinic. M0b owns only the
local editable development loop; M9 owns release wheel, CI, ABI and upgrades.

### Single course authority

`curriculum/COURSE_PRACTICE_MAP.csv` now owns course ID/order, title,
milestone, release, priority, hour range, dependency, concepts, immediate action
and evidence. `scripts/sync_course_plan.py` renders the learner-facing course,
capacity and release tables. Validation rejects stale tables, broken dependency
chains and a Release A exceeding 50 focused hours.

### Hot/cold context

`scripts/build_next_session.py` generates `learning/NEXT_SESSION.md` from the
canonical learner/course state. The Skill and `AGENTS.md` route ordinary
sessions through that brief plus only the current course/milestone and relevant
reference. Full specs, history and audits are loaded only for decisions that
need them.

Measured with `o200k_base`:

| Context shape | Before | After | Reduction |
|---|---:|---:|---:|
| ordinary Foundation startup | about 32,005 tokens | 3,756 tokens | 88.3% |
| resume including foundation guide and latest full note | about 32,005 tokens | 6,518 tokens | 79.6% |

The after measurements include `AGENTS.md`, Skill, hot brief, project loop,
current course row and milestone; the resume measurement additionally includes
the foundation reference and latest completed note. Platform system prompts,
source excerpts and actual lesson content are excluded from both comparisons.

### Lower prompt and administration duplication

- `AGENTS.md` now contains repository-wide invariants and authority routing.
- `SKILL.md` contains runtime decisions and progressive-disclosure routing.
- Mode, source-evidence, assessment and backend detail remain in conditional
  references.
- The ChatGPT prompt is a thin repository/chat-only adapter; quick prompts are
  reduced to a small task switchboard.
- A reviewed session manifest remains the single normal write input. The
  recorder regenerates the hot brief in its isolated staged copy before state
  is accepted.

## Engineering controls

- `scripts/preflight.py` performs a non-mutating environment/capability report
  using the configured Conda Python by default.
- `tests/test_learning_system.py` tests course sequencing, time to first model,
  dependency chaining, generated-table drift, >50-hour rejection, hot-context
  freshness/rebuild, Skill size/routing and machine-readable preflight.
- `scripts/validate_learning_state.py` rejects a missing or stale hot brief.
- `scripts/validate_curriculum_coverage.py` derives course order from the
  canonical map instead of duplicating a hard-coded course/milestone table.
- `scripts/system_health_check.py` runs the focused tests and generated-output
  checks and labels its compiled extension as an isolated fixture rather than
  learner M0a evidence.

## Acceptance evidence

The following completed successfully from the learning-system root:

```text
python3 -m py_compile scripts/*.py tests/test_learning_system.py
python3 -m unittest -v tests/test_learning_system.py
  -> 9 focused product tests pass, including negative drift/time-budget cases

python3 .../skill-creator/scripts/quick_validate.py \
  .agents/skills/pytorch-source-mentor
  -> Skill is valid

python3 scripts/sync_course_plan.py --check
python3 scripts/build_next_session.py --check
  -> generated public tables and hot context are current

python3 scripts/validate_curriculum_coverage.py --verify-symbols
  -> 41 concepts; 13 courses; 28 I0; Release A 30–50 h; full 547–875 h

python3 scripts/validate_learning_state.py
  -> 41 mastery concepts; 12 evidence rows; 12 historical question rows

python3 scripts/record_learning_session.py \
  templates/SESSION_MANIFEST.example.json
  -> isolated dry-run passes with one evidence and zero questions

python3 scripts/system_health_check.py
  -> structure, generated artifacts, preflight, source pin/anchors, fixture
     native import, manifest lifecycle, negative rejection and cleanup pass

git diff --check
  -> pass
```

The health test confirms that synthetic session artifacts remain isolated and
the real learning records are unchanged.

## Repository and environment boundary

- The pinned PyTorch checkout remains exact at
  `cf30153c4c131c8164ee7798e5022d810682e2cb` / `v2.13.0`, detached and clean,
  with full history and 78 recursive submodule entries.
- `mini-torch/` remains an independent repository with no commit. Its current
  README/ADR/ignore artifacts are labeled mentor drafts and are not mastery.
- The 2026-09-16 preflight sees the configured Conda Python development
  headers, C++ compiler, pinned vendored pybind11, nvcc and GPU visibility.
  CMake is the only missing M0a-required capability; Ninja and GDB are
  unavailable optional/later tools. Nothing was installed automatically.
- The isolated direct-compiler fixture proves the host can compile/import a
  pybind extension; it does not satisfy the learner-authored CMake M0a gate.
- Private hardware remains unavailable here; mock/proxy evidence cannot support
  a real-device claim.

## Remaining product risks

- Full mastery is still a 547–875 hour commitment. Releases reduce motivational
  and planning risk but do not make the final objective small.
- Human versus mentor authorship cannot be proven from Git alone; diff history,
  debugging behavior, defense and delayed transfer remain combined evidence.
- The course-map generator removes one major drift source, but project specs
  still contain intentionally overlapping scope descriptions and require audit
  at milestone boundaries.
- Educational effectiveness must be judged from real learner sessions. Passing
  validators proves structural consistency, not learning outcomes.

## Next operational action

Resume C00/M0a from the generated hot brief. Teach tracked/generated boundaries,
then let the learner materially rewrite or replace the mentor-drafted
README/ADR/ignore policy. Resolve the CMake dependency only with explicit setup
authorization before attempting the learner-owned native gate.
