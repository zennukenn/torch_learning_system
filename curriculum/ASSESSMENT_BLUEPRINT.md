# Assessment blueprint

## Progressive baseline

Do not compress the entire baseline into a 60–90 minute source exam. Collect it at the layer where the learner has prerequisites; it is evidence collection, not a pass/fail event.

### Entry diagnostic (20–30 min)

1. Vocabulary: Tensor, operator, model/forward, device, training/inference.
2. Python familiarity: import, function/method, class/object, argument/return.
3. C++ familiarity: source/header, pointer/reference, compile/link.
4. Systems familiarity: process, CPU/GPU, library, stack trace.
5. Learning preference, session duration, work-driven schedule variability, and desired first-stage outcome.

Self-ratings initialize no mastery scores. “听说过” means teach from first principles; it is not permission to test internals.

### Foundation diagnostic

After the relevant lessons, assess the learner's global architecture explanation, a concrete inference ordering task, repository-layer mapping, a small Python reading task, and a reduced C++ compile/link exercise.

### Source-readiness diagnostic

Only after the Foundation Gate, ask the learner to locate a public API, test, schema/registration, and implementation candidate or to predict how a device/compiler backend intercepts an operation. This determines readiness for vertical traces; it is not part of the entry diagnostic.

## Weekly retrieval

- One concept from the previous week.
- One concept at least 3 weeks old.
- One syntax-reading item from a reduced example or current source at the learner's active layer.
- In foundation mode, one architecture ordering/ownership item; after the gate, one source-location or call-order prediction.
- Record original answers and hints before feedback; avoid repeating exact questions from `QUESTION_HISTORY.csv`.

## Phase gate

Each gate contains four parts:

1. closed-notes architecture explanation;
2. locate-and-trace task on a related but unpracticed API/operator;
3. debugging or modification task with focused tests;
4. project defense covering tradeoffs, limitations and evidence.

The roadmap's dimension thresholds are necessary but not sufficient: the project quality gate must also pass. If the learner fails, diagnose the earliest prerequisite and schedule a focused repair session.

## Final assessment

- Reconstruct the full architecture without notes, then reconcile it with source.
- Trace one unannounced eager operation and one unannounced compile/model path.
- Debug a seeded failure without a supplied source location.
- Read a nontrivial Python construct and a nontrivial C++ construct from the checkout.
- Defend the `VENDOR_DEVICE` blueprint, explicitly separating documented facts, proxy validation and unverified hardware assumptions.
- Repeat a sample after at least 14 days to demonstrate retention.
