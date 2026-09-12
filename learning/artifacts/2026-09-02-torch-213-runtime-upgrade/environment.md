# PyTorch 2.13 runtime upgrade

- Date: 2026-09-02
- Environment: existing Conda `base` at `/root/miniconda3`; no duplicate environment created
- Platform checked: CPython 3.10, Linux x86_64
- Source pin: `v2.13.0` / `cf30153c4c131c8164ee7798e5022d810682e2cb`

## Pre-upgrade audit

- Existing runtime: `torch 2.7.1+cu126`, `triton 3.3.1`.
- No installed `torchvision`, `torchaudio`, `torchdata`, `torchtext`, `xformers`, or package declaring a dependency on torch was found in this environment.
- `pip check`: passed.
- Available disk space: approximately 882 GiB.
- Official CUDA 12.6 index contained a CPython 3.10 Linux x86_64 `torch 2.13.0+cu126` wheel.
- Wheel metadata required Python `>=3.10`, matching the environment.

## Upgrade

```text
/root/miniconda3/bin/python -m pip install --upgrade torch==2.13.0 \
  --index-url https://download.pytorch.org/whl/cu126
```

Installed result:

- `torch 2.13.0+cu126`
- `triton 3.7.1`
- CUDA 12.6 wheel dependency set resolved successfully
- `pip check`: passed

## Focused verification

- Import and exact version: passed.
- `torch.version.git_version == cf30153c4c131c8164ee7798e5022d810682e2cb`: passed.
- CPU Tensor/`nn.Flatten`: passed.
- CPU Autograd: passed.
- CPU `nn.Linear`: passed.
- `torch.compile(backend="eager")`: passed.
- CUDA tensor creation, matrix multiplication and synchronization: passed.
- CUDA default `nn.Flatten()` and `nn.Flatten(0)`: passed.
- Learning-system health check: passed.

## Evidence boundary

The installed official binary reports the same Git revision as the pinned checkout, so focused unmodified runtime behavior can be compared with that source revision. It is not built from the local checkout: future local source edits will not affect this binary. A local source build and native debugger workflow remain separate prerequisites.

## Official sources checked

- `https://download.pytorch.org/whl/cu126/torch/`
- `https://pytorch.org/get-started/previous-versions/`
- Accessed 2026-09-02.
