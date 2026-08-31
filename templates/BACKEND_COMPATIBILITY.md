# `VENDOR_DEVICE` inference compatibility matrix

- PyTorch tag/commit:
- Prototype revision:
- Validation class: design / contract test / CPU proxy / CUDA proxy / real hardware
- Representative model/workload:

| Feature | Public behavior | Owning PyTorch subsystem/hook | Eager | Compile | Export/serialization | Focused test | Model evidence | Fallback | Limitation |
|---|---|---|---|---|---|---|---|---|---|
| Tensor creation/move | | | | | | | | | |
| dtype/layout/view | | | | | | | | | |
| allocation/lifetime | | | | | | | | | |
| stream/event/sync | | | | | | | | | |
| RNG | | | | | | | | | |
| operator families | | | | | | | | | |
| dynamic shapes | | | | | | | | | |
| graph partition | | | | | | | | | |
| profiler/errors | | | | | | | | | |
| concurrency | | | | | | | | | |
| distributed boundary | | | | | | | | | |

## Performance protocol

- Inputs/dtypes/layouts:
- Warmup:
- Synchronization:
- Measurement method:
- Reference baseline:
- Memory metric:
- Variance and repetitions:
- Result and limitation:

## Upgrade plan

- Supported PyTorch versions:
- ABI/API assumptions:
- Upstream change monitoring:
- Cross-repository CI:
- Known unsupported behavior:
