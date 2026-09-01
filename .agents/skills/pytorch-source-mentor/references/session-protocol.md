# Session protocol

Use one of two modes for a 90–120 minute session. The learner's demonstrated prerequisites, not elapsed weeks, select the mode.

## Mode selection

- Use **foundation mode** until the Foundation Gate in `curriculum/ROADMAP.md` is met, or whenever the learner reports overload and cannot explain the current map.
- Use **source-trace mode** after the gate for operator, runtime, compiler, debugging, and modification sessions.
- An advanced topic seen during foundation mode is a preview. Preserve any evidence, but do not make it the next review target before its prerequisites.

Read [foundation-teaching.md](foundation-teaching.md) whenever foundation mode applies.

## Foundation mode

Target approximately 60% explanation, 25% practice, and 15% source observation.

### 1. Resume and orient (5–10 min)

- Read durable state and the last session entry.
- Run only due reviews whose prerequisites have already been taught; defer over-level reviews explicitly.
- Ask one to three short baseline or recall questions. Accept “不知道” without escalating into hidden internals.
- Point to the learner's current position on the global architecture map.

### 2. Establish one concept outcome (5 min)

State one observable learner outcome, such as: “Explain in plain language what a tensor, operator, model, and device each represent, then place them in one inference example.”

### 3. Explain from panorama to detail (40–60 min)

- Start with a concrete inference story and a simple diagram or analogy.
- Introduce roughly five to seven defined terms.
- For each term, cover what it is, why it exists, what enters/leaves it, and where it sits in the map.
- Explicitly list details postponed to later phases.
- Pause for short comprehension checks about material already explained; do not ask the learner to guess codegen, dispatch, or native internals.

### 4. Guided practice (20–30 min)

Use labeling, ordering, comparison, a tiny Python example, or learner explanation. Move from recognition to a small causal explanation. Give a reduced language example before any syntax exercise.

### 5. Source observation (10–15 min)

Inspect one or two readable anchors that correspond directly to the taught map. The goal is “this concept has a real home,” not an end-to-end trace. Record one focused verification and its limitation in an artifact based on `templates/FOUNDATION_MAP.md`.

### 6. Learner teach-back and gap audit (10–15 min)

Ask the learner, without notes, to explain:

1. today's concept map in their own words;
2. one concrete example and the order of events;
3. one inspected source anchor and what it contains;
4. one language term if it was part of the outcome;
5. what remains unclear.

Audit `correct`, `missing`, `incorrect`, and `uncertain`. Ask at most three focused follow-ups. After a material correction, require a short corrected restatement. Mentor-supplied material is not mastery evidence.

### 7. Notebook and close (5–10 min)

Write the completed note and evidence only after teach-back. Update notebook index, mistakes, evidence/questions, mastery, review queue, error log, session log, and state; run the validator. Schedule reviews around +1, +3, +7, +14, and +30 days, but defer prompts that depend on untaught layers.

## Source-trace mode

### 1. Resume and diagnose (10–15 min)

- Run due reviews and diagnose the earliest relevant prerequisite.
- Ask one conceptual recall, one source-location or call-order prediction, and when appropriate one syntax-reading question.
- Record the learner's initial answer before feedback.

### 2. Establish the source question (5 min)

State one observable source question and define success as an explanation plus source and focused verification evidence.

### 3. Guided source trace (35–45 min)

Have the learner predict the next layer using the architecture model already learned, then inspect the current checkout together:

`user API → Python wrapper/binding → operator schema/codegen → dispatcher → backend/fallback → kernel → result`

Add Autograd, modes/subclasses, compiler, runtime, or distributed branches only when relevant. Maintain `templates/CALL_CHAIN.md`.

### 4. Syntax clinic (15–20 min)

Select at most two blocking constructs from the inspected source. For each, parse the minimum snippet, explain semantics and PyTorch purpose, reduce it to a standalone example, and ask the learner to predict or modify it.

### 5. Evidence lab (20–30 min)

Use one focused dispatcher query, test, stack trace, log, debugger breakpoint, extension, or reversible learning patch. Require an expected result first and compare it with the actual result and limitations.

### 6. Learner teach-back and gap audit (15–20 min)

Ask for the question/conclusion, important call chain, two source anchors, one syntax construct, verification result, and remaining uncertainty. Preserve the original wording, audit gaps, ask at most three follow-ups, and require corrected restatement for material errors.

### 7. Notebook and close (5–10 min)

Follow the same evidence and state update rules as foundation mode. If the learner cannot complete teach-back, keep the session pending and do not advance the roadmap.

## Hint levels

- H0: restate the goal or ask a diagnostic question.
- H1: point to a subsystem, map region, or search term.
- H2: point to a symbol/file and explain part of the reasoning.
- H3: show the decisive path or complete solution.

Evidence produced at H2/H3 cannot demonstrate independent mastery until later H0/H1 retrieval succeeds.
