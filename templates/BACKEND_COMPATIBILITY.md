# `VENDOR_DEVICE` inference compatibility matrix

- PyTorch tag/commit:
- MiniTorch PrivateUse revision:
- Native PyTorch PrivateUse1 package revision:
- Public adapter ABI version/size:
- Validation level: design / contract-ready mock / CPU proxy / CUDA proxy / real device-smoke / real representative-model
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

## Adapter and capability contract

- Route: MiniTorch PrivateUse / native PyTorch PrivateUse1
- Plugin/autoload mechanism:
- ABI negotiation result:
- Mandatory runtime functions:
- Optional capabilities reported:
- Kernel/fallback classification:
- Mock/fault-injection result:
- Private hardware command bundle:
- Sanitized real-hardware result or `unverified`:

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
