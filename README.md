# PyTorch Source Learning Agent System

这是一个以 MiniTorch 独立实现为项目主线、每周约 20 小时、按 mastery gate 推进的源码学习系统。第一目标是全面、深入、可验证地掌握 PyTorch、C++、CUDA 和相关工程知识；第二目标是为未来的保密推理硬件适配建立可迁移能力。原 20 周只作历史参考，完整容量估计为 547–875 focused hours，通常对应 9–18 个自然月；Release A 先在累计 30–50 小时内交付受限但真实的 CPU inference，后续 releases 保留全部既定深度。

系统不是静态教程。它通过仓库级 `AGENTS.md`、Codex skill、ChatGPT 总提示词、课程路线、项目关卡和持久化学习状态协同工作。

## 目录角色

- `AGENTS.md`：在学习系统工作区中对 Codex 持续生效的顶层约束。
- `.agents/skills/pytorch-source-mentor/`：Codex 的教学、源码取证、评估与 backend 实验工作流。
- `prompts/CHATGPT_SYSTEM_PROMPT.md`：ChatGPT Project 或新对话的薄适配提示词，详细规则仍由 Skill 和仓库权威文件提供。
- `prompts/QUICK_PROMPTS.md`：日常会话入口，不重复总提示词。
- `curriculum/ROADMAP.md`：PyTorch 源码课程、architecture-first sequence 与 MiniTorch phase 对齐。
- `curriculum/COURSE_PRACTICE_PLAN.md` 与 `COURSE_PRACTICE_MAP.csv`：从 Python/model 到 kernel/runtime/hardware 的 inference 课程索引，以及每个知识点必须紧接的 learner-authored MiniTorch 行动和可运行证据。
- `curriculum/ASSESSMENT_BLUEPRINT.md`：以实现、测试、调试、code defense 和延迟扩展为核心的考核规则。
- `curriculum/COVERAGE_AUDIT.md` 与 `COVERAGE_MATRIX.csv`：全面知识/路径审计和每个 mastery concept 的 milestone、source anchor、evidence 映射。
- `curriculum/KNOWLEDGE_GRAPH.md`：知识依赖与源码锚点。
- `projects/MINITORCH_SPEC.md`：已确认的 MiniTorch 范围、依赖、目录、最终案例和作者边界。
- `projects/INFERENCE_SCOPE.md`：inference-first 必修矩阵，覆盖 CNN/Transformer、显存/stream、mixed precision、DP/TP、compiler 与性能证据；同时定义训练降级边界。
- `projects/PRIVATEUSE_BACKEND_SPEC.md`：MiniTorch PrivateUse C-ABI plugin 与原生 PyTorch PrivateUse1 OOT package 的双路线、mock 和真实硬件验收门。
- `projects/ROADMAP.md`：M0a/M0b/M0c、M1–M9 和早期 M2.5 CPU 模型闭环，包含 C/R/S 深度、容量估计与质量门。
- `learning/NEXT_SESSION.md`：从正式状态生成的紧凑 hot context；普通会话不再加载整套课程。
- `learning/`：学习者档案、证据、掌握度、复习队列与会话记录。
- `learning/notebook/`：每次课的闭卷复述、查漏补缺、整理笔记和长期错题本。
- `learning/artifacts/`：每次会话的调用链、语法卡、实验或项目产物。
- `config/PYTORCH_SOURCE_PIN`：唯一的 PyTorch baseline tag/commit 固定点；学习分支可在它之上产生新 commit。
- `scripts/validate_learning_state.py`：检查 CSV schema、跨表引用、枚举、日期、revision 和分数。
- `scripts/system_health_check.py`：在临时独立 Git 仓库编译并导入一个真实 pybind11 native module，再模拟 M0 项目证据、code defense、错误拒绝与清理，不污染真实学习记录。
- `scripts/validate_curriculum_coverage.py`：检查每个 mastery concept 都有有效 priority、已声明 milestone、真实 PyTorch path、具名 source symbol 和足够的 evidence dimensions。
- `scripts/record_learning_session.py`：用一个 JSON session manifest 在临时副本中生成并校验 evidence、question、mastery、review、note、index 和 session log，再选择性写回。
- `scripts/build_next_session.py`：从 profile/state/mastery/review/course map 生成下一节所需的紧凑 hot context。
- `scripts/sync_course_plan.py`：从唯一的 course CSV 生成公开课程表、容量表和 release 表，防止多文档漂移。
- `scripts/preflight.py`：只读检查 M0a 构建依赖、可选 debugger/CUDA 工具与本机资源，不自动安装或修改环境。
- `templates/`：基础架构图、调用链、语法卡、session manifest、单次学习、四周范围审查和周复盘模板。
- `audits/2026-09-16-product-optimization-acceptance.md`：hot/cold context、三阶段 release、单一课程权威、token 降幅和完整验收；2026-09-15 报告保留为历史基线。
- `environment/REPORT.md`：2026-09-01 的本机体检和环境关卡。
- `sources/pytorch/`：被外层 `.gitignore` 忽略的 PyTorch 官方源码；它始终是独立 Git 仓库。
- `mini-torch/`：被外层 `.gitignore` 忽略、由学习者逐步实现的独立 Git 仓库；Python 包名为 `minitorch`。

## 在 Codex 中使用

始终在 VS Code / WSL 中打开本目录 `/home/quanyx/pytorch-learning-system`，不要只打开 `sources/pytorch` 子目录。这样 Codex 能发现仓库级 Skill，同时可以读取和调试源码。

每次从 WSL 启动：

```bash
cd /home/quanyx/pytorch-learning-system
code .
```

开始下一次会话时可以说：

```text
使用 $pytorch-source-mentor，继续当前课程。
```

每次课不是“先讲完再实践”：每个 10–20 分钟 prerequisite block 后，你会立即修改一个真实 MiniTorch 文件/config/test，Agent 检查 diff、运行 focused test，并围绕真实结果教学和调试。结束时只做一次与该 diff 绑定的简短 code defense。只有 learner-authored 项目证据才会更新 mastery；AI 自动补充的文字、草稿、脚手架或测试输出不会被当成你的掌握证据。

从 2026-09-13 起不再生成脱离项目的知识试卷。短问题只用于当前实现的 prerequisite 诊断、code review/defense 或延迟扩展与修复。旧问答、错题和证据保留为历史，不回写成新制度下的成绩。

如果 `$pytorch-source-mentor` 暂时没有出现在列表中：

1. 确认 VS Code 打开的根目录正是 `/home/quanyx/pytorch-learning-system`，而不是 `/home/quanyx` 或 `sources/pytorch`。
2. 执行 `Developer: Reload Window`，再创建一个新的 Codex chat。
3. 仍未显示时，直接说“读取并严格遵循 `.agents/skills/pytorch-source-mentor/SKILL.md`”，功能不会依赖 `$` 补全才能工作。

Codex 从当前工作目录到 repository root 的 `.agents/skills` 中发现 skills；可参考 [Build skills](https://learn.chatgpt.com/docs/build-skills) 和 [Codex IDE extension](https://learn.chatgpt.com/zh-Hans/docs/codex/ide)。

PyTorch 源码固定放在 `sources/pytorch`，MiniTorch 固定放在 `mini-torch`。不要把学习系统文件合并到任一独立仓库。检查 PyTorch 状态：

```bash
bash scripts/check_source_checkout.sh
```

在另一台机器首次克隆本学习系统后，显式执行下面的命令拉取固定版本源码（约占用数 GB，耗时取决于网络）：

```bash
bash scripts/checkout_pytorch_source.sh
```

脚本只会创建缺失的 `sources/pytorch`，不会覆盖已有 checkout；完成后会核对 full history、tag、commit 和 recursive submodules。

## 在 ChatGPT 中使用

将 `prompts/CHATGPT_SYSTEM_PROMPT.md` 放入 ChatGPT Project instructions，并上传或同步本系统的 `config/`、`curriculum/`、`environment/`、`projects/`、`learning/` 和 `templates/`。ChatGPT 无法直接检查本地仓库时，必须由学习者提供具体 revision、源码片段和命令输出；它不得凭记忆伪造路径或调用链。

## MiniTorch 第一次启动的完成条件

1. `config/PYTORCH_SOURCE_PIN` 与本地 checkout 基线完全匹配。当前基线是 `v2.13.0`；学习 patch 必须位于它的 descendant branch，并把实际 HEAD 写入证据。是否出现新 stable 只需在阶段边界定期检查，不在学习会话中自动切换。迁移版本必须单独评估并得到你的明确同意。
2. 完成环境关卡，尤其是 WSL 内存、GPU 可访问性、构建工具和隔离 Python 环境。
3. 学习者完成 PyTorch→MiniTorch 目录/职责映射，并初始化 `mini-torch/` 独立 Git 仓库。
4. M0a 先从干净 build directory 完成 `CMake → C++ library → pybind11 → minitorch._C → import minitorch`，获得第一条 native success。
5. M0b 完成 `pyproject.toml`、local editable development、pytest 和 CTest；随后以显式受限的 contiguous-FP32/manual-op walking skeleton 在累计 30–50 小时内运行首个 CPU model。
6. M1/M2 移除 walking-skeleton debt；M0c 的 exception/GIL/ABI/RPATH/debugging 在进入 CUDA M3 前完成。Release-grade wheel、CI 和 upgrade matrix 属于 M9，不与 M0b 重复。
7. 学习者无笔记解释自己编写的配置、compile/link、extension import path、测试证据和简化边界。

源码存在不代表构建环境已经就绪。构建、安装依赖或修改 WSL/Windows 设置必须经过单独的环境关卡。

可随时运行完整性检查：

```bash
python3 scripts/system_health_check.py
```

开始 M0a 前可先运行无副作用环境检查：

```bash
python3 scripts/preflight.py
```

单独检查知识与路径覆盖：

```bash
python3 scripts/validate_curriculum_coverage.py
```

只检查正式学习记录时运行 `python3 scripts/validate_learning_state.py`。检查 hot context 是否仍与正式状态一致时运行 `python3 scripts/build_next_session.py --check`。系统自检生成的模拟 learner/evidence/question/artifact 全部位于 OS 临时目录，测试完成后自动删除。

完成真实项目会话后，从 `templates/SESSION_MANIFEST.example.json` 复制一份 manifest，将 `example_only` 改为 `false`，再运行 `python3 scripts/record_learning_session.py <manifest>` 预检；确认无误后加 `--apply`。示例文件不能直接写入，脚本也不会绕过 learner teach-back、证据要求或最终状态校验。
