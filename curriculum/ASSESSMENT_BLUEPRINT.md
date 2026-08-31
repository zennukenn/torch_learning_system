# Assessment blueprint

## Baseline diagnostic (60–90 min)

Do this before Week 1 teaching. It is evidence collection, not a pass/fail exam.

1. Python reading: decorator/context manager, attribute lookup and a tiny tensor-wrapper example.
2. C++ reading: references/pointers, RAII, smart pointer, template/macro, compile/link question.
3. Tensor/deep-learning: shape/stride/view, dtype/device, computation graph and inference/training boundary.
4. Systems/debug: process/thread, virtual memory, dynamic library, stack trace and hypothesis formation.
5. Source navigation: with no supplied path, find a public API, relevant test, schema/registration and implementation candidate.
6. Transfer: predict how a new device or compiler backend might intercept the same operation, clearly marking uncertainty.

Use small runnable tasks when possible. Self-ratings initialize no mastery scores.

## Weekly retrieval

- One concept from the previous week.
- One concept at least 3 weeks old.
- One syntax-reading item taken from the current source, not a generic quiz.
- One source-location or call-order prediction.
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
