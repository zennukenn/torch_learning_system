# Call chain — API/operator

- Exact revision:
- Minimal input program:
- Tensor metadata: device, dtype, layout, shape/stride, grad/compile mode
- Question being answered:

| Layer | Symbol/path | What happens | Evidence | Observed/Documented/Inferred |
|---|---|---|---|---|
| Public Python API | | | | |
| Override/mode (if any) | | | | |
| Binding/generated wrapper | | | | |
| Schema/overload | | | | |
| DispatchKeySet/selection | | | | |
| Fallback/redispatch | | | | |
| ATen/native/kernel | | | | |
| Tensor/storage/runtime effect | | | | |
| Result | | | | |

## Optional branches

- Autograd:
- Dynamo/FX/export/AOT/Inductor:
- allocator/device guard/stream/event:
- distributed:

## Verification

- Prediction:
- Command/test/debugger setup:
- Actual result:
- Remaining uncertainty:
- Learner's no-notes reconstruction:
