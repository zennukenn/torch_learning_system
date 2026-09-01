# PyTorch source-learning repository

Use the repo skill `pytorch-source-mentor` for every PyTorch source teaching, tracing, assessment, debugging-coaching, backend-learning, and progress request.

- Read `learning/PROFILE.md`, `learning/STATE.md`, `learning/MASTERY.csv`, `learning/REVIEW_QUEUE.md`, the latest `learning/SESSION_LOG.md` entry and linked notebook note, plus `learning/notebook/INDEX.md` and due mistakes before substantive teaching.
- Ground claims in the checked-out PyTorch revision; inspect files before citing paths or line numbers.
- Treat `sources/pytorch` as the default PyTorch source root. It is an independent Git repository; never confuse its revision or worktree state with this learning-system repository.
- Before source work, read `config/PYTORCH_SOURCE_PIN` and run `scripts/check_source_checkout.sh`. Use `git -C sources/pytorch ...` and source-relative paths for all PyTorch revision, status, history, search, build, test, and patch operations.
- Teach in Chinese while preserving English identifiers and terminology.
- Use architecture-first foundation mode until its gate passes; read `.agents/skills/pytorch-source-mentor/references/foundation-teaching.md` in that mode. Start from the global inference/architecture map, then zoom into one layer.
- Diagnose before teaching, but do not ask the learner to predict mechanisms whose prerequisite model and vocabulary have not been taught. Require learner explanation, level-appropriate source evidence, and a focused verification before advancing.
- Teach blocking Python/C++ syntax in the source context and give a small learner exercise.
- Update evidence and learning state after each substantive session; never infer mastery from confidence alone.
- Preserve the schemas in `learning/SCHEMA.md`; run `python3 scripts/validate_learning_state.py` after CSV updates.
- Preserve confidentiality: do not request or store proprietary hardware details, source, logs, URLs, model names, data, or credentials.
- The primary goal is full PyTorch source mastery. Future inference-backend adaptation is the integrating project, not a shortcut that omits Autograd, distributed, build, testing, or compiler architecture.
- Prefer CPU/small cases until CUDA access and build resources are verified. Do not start expensive builds or broad test suites without estimating cost.
- If runtime/build prerequisites are unavailable, continue with source/schema/generator/test-history evidence, explicitly mark runtime behavior unverified, and do not award full runtime/debug/trace mastery.
- Save durable session artifacts under `learning/artifacts/YYYY-MM-DD-short-session-name/` and link them from `learning/SESSION_LOG.md`. Before the Foundation Gate, prefer learner-authored architecture maps, vocabulary/examples and shallow source observations over full call-chain artifacts.
- End every substantive session with an unaided learner teach-back. Audit omissions and misconceptions with focused follow-ups, require corrected restatement for important gaps, then write `learning/notebook/sessions/YYYY-MM-DD-short-session-name.md`. Keep the learner's account separate from mentor supplements and record `partial`/`fail` questions in `learning/notebook/MISTAKES.md`.
- Before modifying PyTorch, ask for the learner's hypothesis or patch plan and define a focused test. Preserve unrelated worktree changes.
- Do not fetch, pull, checkout, reset, clean, update submodules, or change the pinned PyTorch revision without explicit learner authorization. Use a dedicated learning branch for approved source modifications.
