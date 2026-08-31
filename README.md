# PyTorch Source Learning Agent System

这是一个面向 20 周、每周约 20 小时的源码学习系统。第一目标是全面、深入、可验证地掌握 PyTorch 源码；第二目标是为未来的保密推理硬件适配建立可迁移能力。

系统不是静态教程。它通过仓库级 `AGENTS.md`、Codex skill、ChatGPT 总提示词、课程路线、项目关卡和持久化学习状态协同工作。

## 目录角色

- `AGENTS.md`：在学习系统工作区中对 Codex 持续生效的顶层约束。
- `.agents/skills/pytorch-source-mentor/`：Codex 的教学、源码取证、评估与 backend 实验工作流。
- `prompts/CHATGPT_SYSTEM_PROMPT.md`：ChatGPT Project 或新对话的总提示词。
- `prompts/QUICK_PROMPTS.md`：日常会话入口，不重复总提示词。
- `curriculum/ROADMAP.md`：20 周课程和阶段验收。
- `curriculum/KNOWLEDGE_GRAPH.md`：知识依赖与源码锚点。
- `projects/ROADMAP.md`：每个大阶段的源码修改项目。
- `learning/`：学习者档案、证据、掌握度、复习队列与会话记录。
- `scripts/validate_learning_state.py`：检查 CSV schema、ID、分数范围和必需状态文件。
- `templates/`：调用链、语法卡、单次学习和周复盘模板。
- `environment/REPORT.md`：2026-09-01 的本机体检和环境关卡。
- `sources/pytorch/`：被外层 `.gitignore` 忽略的 PyTorch 官方源码；它始终是独立 Git 仓库。

## 在 Codex 中使用

始终在 VS Code / WSL 中打开本目录 `/home/quanyx/pytorch-learning-system`，不要只打开 `sources/pytorch` 子目录。这样 Codex 能发现仓库级 Skill，同时可以读取和调试源码。

开始会话时可以说：

```text
使用 $pytorch-source-mentor，读取环境报告和学习状态。先执行 Phase 0 环境诊断，不安装或修改系统软件，给我第一个 90–120 分钟学习会话。
```

PyTorch 源码固定放在 `sources/pytorch`。不要把学习系统文件合并到上游源码，也不要把源码提交到外层学习系统仓库。检查双仓库状态：

```bash
bash scripts/check_source_checkout.sh
```

## 在 ChatGPT 中使用

将 `prompts/CHATGPT_SYSTEM_PROMPT.md` 放入 ChatGPT Project instructions，并上传或同步本系统的 `curriculum/`、`projects/`、`learning/` 和 `templates/`。ChatGPT 无法直接检查本地仓库时，必须由学习者提供具体 revision、源码片段和命令输出；它不得凭记忆伪造路径或调用链。

## 第一次启动的完成条件

1. 记录目标 PyTorch tag 和 commit；当前基线是 `v2.13.0`，每次正式开始前重新核验最新 stable。
2. 完成环境关卡，尤其是 WSL 内存、GPU 可访问性、构建工具和隔离 Python 环境。
3. 完成 60–90 分钟基线诊断，更新 `learning/MASTERY.csv`。
4. 运行第一条完整 vertical slice：一个 Python tensor 操作从 API 到 CPU kernel 的可验证调用链。

源码存在不代表构建环境已经就绪。构建、安装依赖或修改 WSL/Windows 设置必须经过单独的环境关卡。

可随时运行完整性检查：

```bash
python3 scripts/validate_learning_state.py
```
