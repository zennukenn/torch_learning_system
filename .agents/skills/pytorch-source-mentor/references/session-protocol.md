# Session protocol

Use this protocol for a 90–120 minute session. Adjust timing to the task; keep the evidence gates.

## 1. Resume and diagnose (10–15 min)

- Read durable state and the last session entry.
- Run due spaced-repetition prompts before new material.
- Ask one conceptual recall, one source-location or call-order prediction, and—when appropriate—one syntax reading question.
- Record the learner's initial answer before feedback.

## 2. Establish the source question (5 min)

State one observable question, for example: “For `torch.add(x, y)` on CPU, which mechanism selects the concrete kernel in this revision?” Define success as an explanation plus source and runtime evidence.

## 3. Guided source trace (35–45 min)

Have the learner predict the next layer, then search and inspect together. Prefer this vertical scaffold:

`user API → Python wrapper/binding → operator schema/codegen → dispatcher → backend/fallback → kernel → result`

Add these branches only when relevant:

- `Autograd` keys and generated variable wrappers;
- `__torch_function__`, `__torch_dispatch__`, modes, or subclasses;
- `TorchDynamo → FX → AOTAutograd/export → backend/Inductor`;
- device guard, allocator, stream, event, generator, or distributed layer.

Maintain a trace note using `templates/CALL_CHAIN.md`.

## 4. Syntax clinic (15–20 min)

Select at most two blocking constructs found in the real code. For each:

1. quote only the smallest relevant snippet;
2. parse tokens and types;
3. explain lifetime, dispatch, binding, or compile-time consequences;
4. reduce it to a standalone example;
5. ask the learner to predict or modify it.

Candidates include Python descriptors/decorators/context managers/metaclasses and C++ templates, RAII, intrusive pointers, move semantics, macros, lambdas, `constexpr`, type erasure, and pybind-style bindings.

## 5. Evidence lab (20–30 min)

Use one focused experiment: dispatcher table query, breakpoint, stack trace, logging, a tiny extension, a focused unit test, or a reversible learning patch. Require an expected result before execution and compare actual versus expected afterward.

## 6. Learner teach-back (10–15 min)

Stop teaching and ask the learner to close notes and explain, in their own words:

1. the question and main conclusion from today;
2. the important mechanism or vertical call chain;
3. at least two source anchors and what each proves;
4. one Python or C++ construct encountered and its semantics;
5. what remains uncertain or unverified.

Do not pre-fill the recap or turn the prompt into a summary. Preserve the learner's original wording faithfully enough to assess it. If the learner cannot continue, mark the session pending teach-back; do not append completed-session evidence or advance the roadmap.

## 7. Gap audit and corrected retrieval (5–10 min)

- Compare the teach-back with the observable outcome, inspected source, prediction versus result, syntax clinic, and stated limitations.
- Separate findings into `correct`, `missing`, `incorrect`, and `uncertain`. Ask at most three focused follow-ups before explaining the gaps.
- After a material correction, ask the learner to restate the corrected point. Record the hint level and distinguish the initial answer, corrected learner answer, and mentor supplement.
- Grade only what the learner demonstrated. Mentor-supplied content is useful notebook material but not mastery evidence.

## 8. Notebook and close (5–10 min)

- Create one note from `templates/LEARNING_NOTE.md` at `learning/notebook/sessions/YYYY-MM-DD-short-session-name.md`.
- Preserve the learner teach-back, gap audit, corrected answers, verified source map, syntax takeaway, unresolved items, evidence IDs, review dates, and exactly one next action.
- Update `learning/notebook/INDEX.md`. For every question graded `partial` or `fail`, append a concise row to `learning/notebook/MISTAKES.md`; retain resolved mistakes and link their later retrieval evidence.
- Append evidence/questions with the note path, then update mastery, review queue, error log, session log, and state. Run the validator.
- Schedule reviews at roughly +1, +3, +7, +14, and +30 days, adapting to performance.

## Hint levels

- H0: restate the goal or ask a diagnostic question.
- H1: point to a subsystem or search term.
- H2: point to a symbol/file and explain part of the reasoning.
- H3: show the solution path or decisive code.

Evidence produced at H2/H3 cannot demonstrate independent mastery until later retrieval succeeds at H0/H1.
