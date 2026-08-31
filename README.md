# PyTorch Source Learning Agent System

这是一个面向 20 周、每周约 20 小时的源码学习系统。第一目标是全面、深入、可验证地掌握 PyTorch 源码；第二目标是为未来的保密推理硬件适配建立可迁移能力。

系统不是静态教程。它通过仓库级 `AGENTS.md`、Codex skill、ChatGPT 总提示词、课程路线、项目关卡和持久化学习状态协同工作。

## 目录角色

- `AGENTS.md`：放入 PyTorch 源码仓库后，对 Codex 持续生效的顶层约束。
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

## 在 Codex 中使用

当 PyTorch 仓库尚未克隆时，先在本系统目录启动 Codex 并说：

```text
使用 $pytorch-source-mentor，读取环境报告和学习状态。先执行 Phase 0 环境诊断，不安装或修改系统软件，给我第一个 90–120 分钟学习会话。
```

克隆源码后，将本目录内容合并到源码仓库根目录，保留 PyTorch 原有文件和用户改动。之后从源码仓库启动 Codex。不要在未审阅差异时覆盖上游同名 `AGENTS.md`。

## 在 ChatGPT 中使用

将 `prompts/CHATGPT_SYSTEM_PROMPT.md` 放入 ChatGPT Project instructions，并上传或同步本系统的 `curriculum/`、`projects/`、`learning/` 和 `templates/`。ChatGPT 无法直接检查本地仓库时，必须由学习者提供具体 revision、源码片段和命令输出；它不得凭记忆伪造路径或调用链。

## 第一次启动的完成条件

1. 记录目标 PyTorch tag 和 commit；当前基线是 `v2.13.0`，每次正式开始前重新核验最新 stable。
2. 完成环境关卡，尤其是 WSL 内存、GPU 可访问性、构建工具和隔离 Python 环境。
3. 完成 60–90 分钟基线诊断，更新 `learning/MASTERY.csv`。
4. 运行第一条完整 vertical slice：一个 Python tensor 操作从 API 到 CPU kernel 的可验证调用链。

此目录当前只创建学习系统，没有克隆 PyTorch、安装依赖或更改 WSL/Windows 设置。

可随时运行完整性检查：

```bash
python3 scripts/validate_learning_state.py
```
