# Official sources and version policy

Accessed 2026-09-01. These links seed the work; the Agent must re-check changing facts and prefer the checked-out source for implementation details.

## Version and development

- [PyTorch releases](https://github.com/pytorch/pytorch/releases): observed latest stable release `v2.13.0` on 2026-09-01.
- [Published version metadata](https://github.com/pytorch/pytorch.github.io/blob/site/published_versions.json): reported `latest_stable` as `2.13.0` when checked.
- [PyTorch source repository and build instructions](https://github.com/pytorch/pytorch): clone, dependency and build entry points.
- [PyTorch CONTRIBUTING.md](https://github.com/pytorch/pytorch/blob/main/CONTRIBUTING.md): editable development, generated files, focused tests, build/debug tips and C++ development constraints.
- [PyTorch RELEASE.md](https://github.com/pytorch/pytorch/blob/main/RELEASE.md): release compatibility matrix; for 2.13 it records Python `>=3.10`, C++20, and the published CUDA/ROCm combinations.

## Backend and compiler integration

- [Accelerator Integration](https://docs.pytorch.org/docs/main/accelerator/index.html): current top-level accelerator integration documentation.
- [Facilitating New Backend Integration by PrivateUse1](https://docs.pytorch.org/tutorials/advanced/privateuseone.html): out-of-tree `PrivateUse1` mechanisms and registration topics.
- [Extending dispatcher for a new backend in C++](https://docs.pytorch.org/tutorials/advanced/extend_dispatcher.html): dispatcher-side backend extension concepts.
- [`rename_privateuse1_backend`](https://docs.pytorch.org/docs/main/generated/torch.utils.backend_registration.rename_privateuse1_backend.html): current public API requirements and backend module note.
- [`torch.compile` custom backends](https://docs.pytorch.org/docs/main/user_guide/torch_compiler/torch.compiler_custom_backends.html): backend callable contract and registration.
- [Out-of-tree accelerator CI integration](https://docs.pytorch.org/docs/stable/accelerator/ci.html): compatibility and cross-repository CI considerations.

## Source priority

1. Exact checked-out tag/commit and its tests/comments.
2. Documentation built for that same stable version.
3. Current official `main` documentation, clearly marked as newer or unstable relative to the checkout.
4. PyTorch issues/PRs only for history or unresolved behavior, never as a substitute for verifying current code.

For every architecture claim, distinguish public contract, current implementation, generated artifact and inference about design intent.

## Agent system sources

- [Official OpenAI documentation: AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md): repository instruction discovery and precedence.
- [Official OpenAI documentation: Build skills](https://learn.chatgpt.com/docs/build-skills): repo skill location, `SKILL.md` structure and explicit/implicit invocation.
