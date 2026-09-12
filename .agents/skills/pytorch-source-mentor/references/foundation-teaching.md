# Architecture-first foundation teaching

Use this mode when the learner cannot yet explain basic PyTorch vocabulary, asks for a global architecture first, or shows overload during a source trace. The purpose is to build prerequisites for deep source work and MiniTorch implementation, not to lower the final standard.

## Progression

Teach by repeated zoom levels:

1. **User view:** tensor, operator, model/`Module`, `forward`, device, training, inference.
2. **Execution panorama:** Python frontend, tensor/operator core, eager execution, optional Autograd, runtime/hardware, and the compiler path.
3. **Repository map:** connect each already-known layer to one or two top-level directories.
4. **Language/runtime foundations:** Python import/class/call flow; C++ source/header, compile, link, library, pointer/reference and lifetime.
5. **Shallow source observation:** inspect a small readable Python path or one declaration without crossing unknown layers.
6. **MiniTorch M0:** turn the learned map into one small repository/build/binding increment without asking the learner to guess untaught C++ or tooling.
7. **Vertical source trace and deeper implementation:** begin only after the Foundation Gate in `curriculum/ROADMAP.md` is met.

Each zoom starts from the same global map. State where the current concept sits, what enters it, what leaves it, and which details are deliberately postponed.

## Session balance

For the current learner, target approximately:

- 60% mentor explanation using a concrete example, analogy, and simple diagram;
- 25% learner practice such as sorting, labeling, explaining, or modifying a tiny example;
- 15% source observation limited to the concepts already taught.

Adjust timing without changing the order. Introduce roughly five to seven new terms in one session, define each in plain Chinese, and maintain a short vocabulary recap. Do not combine a new architecture layer, unfamiliar schema notation, code generation, dispatcher internals, and C++ syntax in the same beginner session.

## Questions and evidence

- A diagnostic may ask what the learner already knows, but “不知道” is a valid baseline rather than a cue to reveal a deep solution path.
- Teach the prerequisite model before asking a prediction about it. Predictions test a model the learner has just received; they do not require guessing undisclosed internals.
- Prefer classification and causal questions before source-location questions: “Which layer owns this?” before “Which file implements this?”
- In foundation mode, one inspected source anchor and a small verification are enough. Do not require an end-to-end call chain.
- Use M0 architecture, packaging, CMake, pybind11 and import work as the assessment medium. Short oral checks must explain learner-produced design/config/code rather than form a separate quiz.
- Teach-back asks for the concept map, one concrete example, one source observation, and current uncertainty. Do not require two native anchors or generated/runtime evidence unless those were the declared outcome.
- Architecture diagrams and mentor explanations do not by themselves prove mastery. Award `explain` evidence only from the learner's own restatement or application.

## Overload response

When the learner cannot reconstruct the lesson after explanation:

1. stop adding layers;
2. identify the earliest missing term or causal link;
3. return to a smaller example and ask for a corrected restatement;
4. reschedule advanced reviews until their prerequisites have been taught;
5. record the advanced material as a preview, not as the learner's active next step.
