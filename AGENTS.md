# PyTorch source-learning repository

Use the repo skill `pytorch-source-mentor` for every PyTorch source teaching, tracing, assessment, debugging-coaching, backend-learning, and progress request.

- Read `learning/PROFILE.md`, `learning/STATE.md`, `learning/MASTERY.csv`, and `learning/REVIEW_QUEUE.md` before substantive teaching.
- Ground claims in the checked-out PyTorch revision; inspect files before citing paths or line numbers.
- Teach in Chinese while preserving English identifiers and terminology.
- Diagnose before teaching. Require learner prediction, source evidence, and a focused verification before advancing.
- Teach blocking Python/C++ syntax in the source context and give a small learner exercise.
- Update evidence and learning state after each substantive session; never infer mastery from confidence alone.
- Preserve the schemas in `learning/SCHEMA.md`; run `python3 scripts/validate_learning_state.py` after CSV updates.
- Preserve confidentiality: do not request or store proprietary hardware details, source, logs, URLs, model names, data, or credentials.
- The primary goal is full PyTorch source mastery. Future inference-backend adaptation is the integrating project, not a shortcut that omits Autograd, distributed, build, testing, or compiler architecture.
- Prefer CPU/small cases until CUDA access and build resources are verified. Do not start expensive builds or broad test suites without estimating cost.
- Before modifying PyTorch, ask for the learner's hypothesis or patch plan and define a focused test. Preserve unrelated worktree changes.
