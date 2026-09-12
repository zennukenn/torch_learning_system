# Session protocol

Use one of two project modes for a 90–120 minute session. The learner's demonstrated prerequisites, not elapsed weeks, select the mode. In both modes, the current MiniTorch increment is the assessment unit; isolated knowledge exams are not used.

## Mode selection

- Use **foundation project mode** until the Foundation Gate in `curriculum/ROADMAP.md` is met, or whenever the learner reports overload and cannot explain the current map. It advances MiniTorch M0 through small architecture/build/binding increments.
- Use **implementation/trace mode** after the gate for Tensor, operator, runtime, compiler, debugging, and modification increments.
- An advanced topic seen during foundation mode is a preview. Preserve any evidence, but do not make it the next review target before its prerequisites.

Read [foundation-teaching.md](foundation-teaching.md) whenever foundation mode applies.

## Rules shared by both modes

1. Select exactly one session-sized increment from `projects/ROADMAP.md` and create its contract with `templates/MINITORCH_MILESTONE.md`.
2. Teach the prerequisite before asking for design or code. Inspect at least one corresponding location in the pinned PyTorch checkout.
3. Require the learner's design, hypothesis or patch plan before decisive implementation.
4. The learner writes decisive logic. Mentor scaffolding must be minimal and labeled.
5. Verify with the relevant build, native, Python, boundary/error, parity, integration or packaging tests.
6. Use a real failure when one occurs; otherwise use a small seeded defect only after the base behavior works.
7. Close with an unassisted defense of the learner's diff/configuration and schedule a delayed extension or repair.

## Foundation mode

Target approximately 60% explanation, 25% practice, and 15% source observation.

### 1. Resume and orient (5–10 min)

- Read durable state and the last session entry.
- Run only due reviews whose prerequisites have already been taught; defer over-level reviews explicitly.
- Ask at most three short questions only to diagnose prerequisites for the current M0 increment or retrieve an older implemented behavior. Accept “不知道” without escalating into hidden internals.
- Point to the learner's current position on the global architecture map.

### 2. Establish one concept outcome (5 min)

State one observable learner outcome, such as: “Explain in plain language what a tensor, operator, model, and device each represent, then place them in one inference example.”

### 3. Explain from panorama to detail (40–60 min)

- Start with a concrete inference story and a simple diagram or analogy.
- Introduce roughly five to seven defined terms.
- For each term, cover what it is, why it exists, what enters/leaves it, and where it sits in the map.
- Explicitly list details postponed to later phases.
- Pause for short comprehension checks about material already explained; do not ask the learner to guess codegen, dispatch, or native internals.

### 4. Guided MiniTorch work (20–30 min)

Use labeling, directory mapping, a tiny Python/C++ example, build configuration or learner explanation. Move from recognition to one small learner-authored M0 artifact or code/config change. Give a reduced language/tooling example before asking for a project change.

### 5. Source observation (10–15 min)

Inspect one or two readable anchors that correspond directly to the taught map. The goal is “this concept has a real home,” not an end-to-end trace. Record one focused build/test verification and its limitation in an artifact based on `templates/MINITORCH_MILESTONE.md`; use `FOUNDATION_MAP.md` as a supporting learner diagram where useful.

### 6. Learner teach-back and gap audit (10–15 min)

Ask the learner, without notes, to explain:

1. today's concept map in their own words;
2. the M0 artifact/config/code they authored and its build or import path;
3. one inspected source anchor and the relevant correspondence;
4. one language or engineering construct used in the change;
5. what remains unclear.

Audit `correct`, `missing`, `incorrect`, and `uncertain`. Ask at most three focused follow-ups. After a material correction, require a short corrected restatement. Mentor-supplied material is not mastery evidence.

### 7. Notebook and close (5–10 min)

Write the completed note and evidence only after teach-back. Update notebook index, mistakes, evidence/questions, mastery, review queue, error log, session log, and state; run the validator. Schedule reviews around +1, +3, +7, +14, and +30 days, but defer prompts that depend on untaught layers.

## Implementation/trace mode

### 1. Resume and diagnose (10–15 min)

- Run only due reviews that can be expressed as a current code explanation, extension or repair, and diagnose the earliest relevant prerequisite.
- Ask only the conceptual/source/call-order questions required for the selected increment.
- Record the learner's initial answer before feedback.

### 2. Establish the implementation contract (5 min)

State one observable MiniTorch behavior. Define the supported subset, invariants, errors, likely files and acceptance matrix before coding.

### 3. Guided source comparison and implementation (35–45 min)

Have the learner design the next MiniTorch layer using the architecture model already learned, then inspect the current PyTorch checkout together:

`user API → Python wrapper/binding → operator schema/codegen → dispatcher → backend/fallback → kernel → result`

Add Autograd, modes/subclasses, compiler, runtime, or distributed branches only when relevant. The learner writes the decisive implementation. Maintain `templates/MINITORCH_MILESTONE.md` and use `CALL_CHAIN.md` when a vertical trace is part of the increment.

### 4. Syntax clinic (15–20 min)

Select at most two blocking constructs from the inspected source. For each, parse the minimum snippet, explain semantics and PyTorch purpose, reduce it to a standalone example, and ask the learner to predict or modify it.

### 5. Evidence lab (20–30 min)

Run the predefined acceptance matrix, beginning with the narrowest relevant test. Use a real failure or focused seeded defect for hypothesis-driven debugging. Require an expected result first and compare it with the actual result and limitations.

### 6. Learner teach-back and gap audit (15–20 min)

Ask for the implemented contract, important build/runtime path, MiniTorch diff, inspected PyTorch anchors, one syntax/engineering construct, verification result, simplification and remaining uncertainty. Preserve the original wording, audit gaps, ask at most three follow-ups, and require corrected restatement for material errors.

### 7. Notebook and close (5–10 min)

Follow the same evidence and state update rules as foundation mode. If the learner cannot complete teach-back, keep the session pending and do not advance the roadmap.

## Hint levels

- H0: restate the goal or ask a diagnostic question.
- H1: point to a subsystem, map region, or search term.
- H2: point to a symbol/file and explain part of the reasoning.
- H3: show the decisive path or complete solution.

Evidence produced at H2/H3 cannot demonstrate independent mastery until later H0/H1 retrieval succeeds.
