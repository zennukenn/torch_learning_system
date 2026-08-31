# Accelerator backend lab

The learner's immediate environment is CPU/CUDA, the confidential target device is unavailable, and the product goal is inference. Treat backend work as an abstraction-and-evidence track, not as a claim that hardware integration is already validated.

## Progressive routes

1. **C++ extension:** learn schemas, registration, ABI/build boundaries, and focused CPU/CUDA kernels.
2. **`PrivateUse1` device prototype:** learn device naming, `TensorImpl`, allocator/device guard hooks, dispatcher registrations, fallbacks, serialization, RNG, streams/events, AMP and profiler boundaries as applicable.
3. **Out-of-tree backend package:** isolate vendor code, packaging, version compatibility, tests, and cross-repository CI.
4. **`torch.compile` backend:** accept an FX `GraphModule` plus example inputs, lower supported graphs, define fallback/partitioning, and validate semantic equivalence.
5. **Inference compatibility:** models, dynamic shapes, dtype/layout/view semantics, serialization/export, memory, concurrency, profiling, and upgrade policy.

Do not conflate a compiler backend with an eager device backend. Document which layer owns graph capture, lowering, kernel selection, allocation, execution, synchronization, and error reporting.

## Confidentiality boundary

- Never request proprietary source, unreleased ISA details, keys, internal URLs, customer models, or raw confidential logs.
- Use placeholders such as `VENDOR_DEVICE`, `vendorMalloc`, and capability tables with abstract feature names.
- Ask the learner to reduce errors to public-interface reproductions and redact paths, identifiers, addresses, model names, and data.
- Record only public PyTorch facts and abstract requirements in this repository.

## Compatibility matrix

For each feature, track: public API, required subsystem/hook, supported dtype/layout/device behavior, eager status, compile status, serialization/export status, focused test, model test, performance status, upstream version, and known limitation.

Operator-count coverage is not the primary metric. Prioritize representative-model compatibility, semantic correctness, fallback behavior, memory/concurrency correctness, performance, and maintainability.

## Gate evidence

A backend stage passes only with:

- an architecture note showing ownership boundaries;
- executable correctness tests and negative tests;
- a traced representative model segment;
- explicit unsupported behavior and fallback policy;
- measured results with synchronization and warmup handled correctly;
- a compatibility/upgrade plan tied to a pinned PyTorch revision.
