# Project-driven assessment blueprint

From 2026-09-13, MiniTorch implementation is the default assessment medium. Earlier question, mistake and mastery records remain historical evidence. Do not generate standalone knowledge exams or trivia review sets after the transition.

Questions still have a narrow role: diagnose a prerequisite before implementation, ask the learner to defend code they wrote, or retrieve a mechanism through a delayed extension/repair. Every new row in `QUESTION_HISTORY.csv` must name the associated MiniTorch milestone, diff, failure or source-comparison task in its conditions.

## Assessment unit

Assess one session-sized MiniTorch increment, not an entire subsystem at once. Define its contract before coding:

- observable API or build behavior;
- supported and explicitly unsupported inputs;
- invariants and ownership/state expectations;
- expected error behavior;
- files or targets likely to change;
- focused acceptance commands and expected results;
- one or two current PyTorch source anchors to inspect;
- concepts deliberately postponed.

Use `templates/MINITORCH_MILESTONE.md`. The learner submits the decisive design and implementation. Mentor-authored scaffolding and tests must be distinguished from learner-authored logic.

## Evidence ladder

An increment moves through the following evidence. Earlier rungs can guide learning but do not substitute for later ones.

1. **Design:** the learner places the change in the architecture and predicts build/call/ownership behavior.
2. **Implement:** the learner writes the decisive code and can identify their diff.
3. **Verify:** build plus relevant unit, integration, boundary, error and oracle-parity tests pass.
4. **Debug:** the learner forms and tests a hypothesis for a real or seeded failure instead of applying an unexplained fix.
5. **Compare:** the learner inspects the pinned PyTorch source and explains one real correspondence and one MiniTorch simplification.
6. **Defend:** without notes, the learner explains contract, path, invariants, evidence, tradeoff and limitation.
7. **Transfer/retain:** after a delay, the learner adds a small variant or repairs a related defect without replaying the original solution.

Passing an existing test suite alone does not demonstrate authorship, understanding, debugging or retention.

## Test matrix

Choose only relevant layers for a given increment, but never treat one happy-path test as completion.

| Layer | What it proves | Typical examples |
|---|---|---|
| Configure/build | dependency discovery and target graph | clean CMake configure, CPU-only option, CUDA-conditional configure |
| Native unit | local C++ invariant | ownership, registration lifetime, shape/stride, kernel result |
| Python API | binding and frontend contract | import, dtype/device conversion, Module call |
| Boundary/error | explicit unsupported behavior | invalid shape, dtype/device mismatch, missing kernel |
| Oracle parity | supported semantic agreement | NumPy or official PyTorch result/tolerance |
| Integration | cross-layer execution | Python → binding → dispatcher → kernel |
| Packaging | isolated consumer behavior | wheel install in a clean environment |
| Performance | measurement correctness and trend | warmup, synchronization, input specification, baseline |
| Memory/runtime | allocation, reuse and asynchronous lifetime | allocated/reserved counters, fragmentation/OOM, stream/event dependency |
| Distributed | shard/replica and collective correctness | per-rank shapes, reconstruction, timeout/failure, unsharded oracle |

Tests should expose a contract, not surprise the learner with untaught behavior. A small unseen variant is reserved for transfer only after the base mechanism has been taught and implemented.

## Code defense

At the end of a substantive increment, stop teaching and ask the learner to explain their own work without notes:

1. What contract did this change implement, and what is unsupported?
2. What is the build or runtime call path through the changed files?
3. Who owns memory/state, and what invariant must remain true?
4. Which tests ran, what did each prove, and what remains unverified?
5. Where is the corresponding responsibility in the pinned PyTorch source?
6. What simplification did MiniTorch make, and what consequence follows?

Ask at most three focused follow-ups. Preserve the initial answer and hint level. A critical correction requires a short corrected restatement before closing.

## Mastery dimensions

- `explain`: defend purpose, contract, invariants and simplifications;
- `locate`: find the relevant MiniTorch and pinned PyTorch locations;
- `trace`: reconstruct the build or runtime path with evidence;
- `debug`: form and test hypotheses from a reproducible failure;
- `modify`: author a focused implementation with tests;
- `transfer`: extend the mechanism to a related unscripted case;
- `retain`: repeat an explanation, repair or extension after a delay.

Score each dimension independently from 0–4:

- 0: no evidence;
- 1: recognizes after substantial guidance;
- 2: partial result or completion with H2;
- 3: independently completes the studied case with H0/H1;
- 4: independently transfers, explains tradeoffs and survives delayed review.

Mentor-written code, copied solutions, self-confidence and test output without learner explanation cannot raise mastery.

## Milestone gate

A milestone passes only when:

- all required increments in `projects/ROADMAP.md` have learner-authored evidence;
- all I0 items assigned to the milestone by `projects/INFERENCE_SCOPE.md` are complete before any T2 training extension is credited;
- the milestone's positive, boundary, negative and relevant parity/integration tests pass;
- at least one real or seeded debugging task is completed;
- the learner can trace a representative vertical slice in MiniTorch and compare it with inspected PyTorch source;
- simplifications and unverified behavior are explicit;
- a delayed transfer or repair has passed at H0/H1.

If a gate fails, identify the earliest missing language, architecture, implementation or debugging prerequisite and schedule one repair increment.

## Weekly audit

Once per week:

- review MiniTorch commits/diffs and identify which decisive code the learner authored;
- check the ratio of implementation/debugging evidence to passive reading;
- run one delayed extension or repair tied to an older milestone;
- inspect test gaps and flaky/non-reproducible behavior;
- identify the earliest weak prerequisite;
- choose exactly one next milestone increment.

Do not add an unrelated old-style quiz merely to fill a review slot. Convert a due historical prompt into a current code explanation, test, source comparison or extension when prerequisites now exist; otherwise keep it deferred.

## Final assessment

The final assessment is a capstone maintenance exercise rather than a written exam:

- reconstruct the architecture from the learner's MiniTorch repository and reconcile it with pinned PyTorch;
- trace one unannounced eager operation and one unannounced compiled inference path;
- implement one bounded extension from contract to tests;
- diagnose and repair one seeded cross-layer failure without a supplied source location;
- build and install a wheel in a clean environment;
- run only the minimal MLP training/gradient-sync boundary, then CPU/CUDA CNN and Transformer/KV-cache inference, mixed precision, compiler, inference DP/TP, memory/stream and simulated-device demonstrations;
- defend correctness, latency, throughput, allocated/reserved memory, transfer/communication, compile/startup, fallback, packaging and version-upgrade limitations;
- repeat a related maintenance task after at least 14 days.
