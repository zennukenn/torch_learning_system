# Quick prompts

日常不需要选择复杂模板。Repository mode 已由 Skill 路由；通常只说：

```text
使用 $pytorch-source-mentor，继续当前课程。
```

如果 Skill 列表不可见：

```text
读取 .agents/skills/pytorch-source-mentor/SKILL.md，验证并读取 learning/NEXT_SESSION.md，然后继续唯一下一步。
```

仅在明确切换任务时使用下面入口。

## 源码追踪

```text
使用 $pytorch-source-mentor，在当前 pinned revision 中追踪 <API/op>。先检查当前 prerequisites，再用源码和最小 runtime evidence 验证一条 vertical slice。
```

## Debug

```text
使用 $pytorch-source-mentor 调试 <reproduction>。先记录我的 hypothesis，再用最小可证伪命令定位；不要直接替我完成决定性修复。
```

## Milestone 验收

```text
使用 $pytorch-source-mentor 验收当前 MiniTorch increment：检查 learner diff、focused tests、一次 bounded failure repair、pinned-source 对照和简短 code defense。
```

## Scope/系统审计

```text
使用 $pytorch-source-mentor 执行范围和系统审计。加载冷 context，检查覆盖、时间到价值、token/记录成本、当前 blocker 和唯一下一步；不要把审计记作 mastery。
```

## PrivateUse/backend

```text
使用 $pytorch-source-mentor 进入当前 PrivateUse P0–P5 gate。严格区分 MiniTorch C-ABI route、native PyTorch PrivateUse1 route 和真实硬件证据。
```

## 记录完成会话

```text
我已完成 unaided defense。使用 reviewed manifest dry-run、校验并更新学习状态，同时重新生成 learning/NEXT_SESSION.md。
```
