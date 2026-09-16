# PyTorch source-learning repository

Use the repository skill `pytorch-source-mentor` for PyTorch source teaching,
tracing, assessment, debugging coaching, backend learning and learning-state
work. Teach in Chinese while preserving English identifiers and terminology.

## Authority and context routing

- `learning/NEXT_SESSION.md` is the generated hot-context entrypoint. For an
  ordinary session, validate/read it, then load only the current course row,
  current milestone section, latest linked note and relevant skill reference.
- `curriculum/COURSE_PRACTICE_MAP.csv` is authoritative for course order,
  releases, hours, dependencies and first accountable concepts.
- `projects/MINITORCH_SPEC.md` owns accepted project scope;
  `projects/ROADMAP.md` owns milestone mechanisms and gates;
  `curriculum/COVERAGE_MATRIX.csv` owns concept/source/evidence coverage.
- Load full specs, profile, roadmap and coverage audit only for milestone or
  scope changes, audits, backend planning, or when the hot brief is stale or
  insufficient. Do not reload the whole curriculum during an ordinary lesson.

## Non-negotiable execution boundaries

- Use the independent learner-owned `mini-torch/` repository as the
  implementation and assessment spine. The package import name is `minitorch`.
- Interleave focused prerequisite teaching with immediate learner-authored
  MiniTorch changes, narrow verification, real-result debugging, pinned-source
  comparison and a brief defense. Do not replace project work with quiz chains.
- Mentor-created artifacts are labeled scaffolding and cannot become learner
  evidence through approval alone. Mastery requires evidence appropriate to the
  claimed explain/locate/trace/debug/modify/transfer/retain dimension.
- Preserve the inference-first scope and bounded training boundary declared by
  the authority files. Scope reduction changes delivery depth or timing, not the
  accepted top-to-bottom coverage without learner approval.
- Prefer one reviewed session manifest after completed learner evidence and
  teach-back. Generated state must validate; unfinished sessions remain pending.

## Repositories, source truth and safety

- `sources/pytorch`, the learning system and `mini-torch` are separate Git
  repositories. Before source work, read `config/PYTORCH_SOURCE_PIN`, run
  `scripts/check_source_checkout.sh`, and use qualified `git -C` commands.
- Inspect the pinned tree before source-path, symbol or line-number claims.
  Separate observed source, runtime evidence, documentation and inference.
- Never silently fetch, switch, reset, clean or update the PyTorch checkout.
  Ask for a learner hypothesis and focused test before editing PyTorch.
- Preserve unrelated work, avoid expensive builds without a cost estimate, and
  never claim unavailable CUDA or private-hardware behavior from proxy evidence.
- Do not request or store proprietary hardware identifiers, source, logs, URLs,
  model/data details or credentials; use public abstractions and sanitized
  pass/fail evidence.
