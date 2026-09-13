# Dual PrivateUse backend specification

This project requires two related but separate backend routes. Both use only public abstractions and the placeholder name `VENDOR_DEVICE`. No proprietary runtime names, headers, model names, logs or hardware details belong in this repository.

All PyTorch anchors in this document were inspected in the pinned checkout `cf30153c4c131c8164ee7798e5022d810682e2cb` (`v2.13.0`) on 2026-09-13.

## Claims and validation boundary

The repository can prove that the backend architecture, public adapter ABI, CPU mock and contract suite work. It cannot prove that MiniTorch or native PyTorch runs correctly on the real third-party device until the learner supplies a private adapter shared library in the hardware environment and records sanitized pass/fail results.

The final claim has three levels:

1. **contract-ready:** public headers, loader, mock adapter and negative tests pass;
2. **device-smoke verified:** real adapter passes device, allocation, copy, stream/event and one operator test;
3. **model verified:** a representative inference slice passes eager and compile correctness, memory, concurrency and error tests on the real device.

Never promote level 1 proxy evidence to level 2 or 3.

## Route A — MiniTorch pluggable PrivateUse device

MiniTorch reserves a `PrivateUse` device kind and loads an out-of-tree plugin at runtime. The plugin registers runtime services and kernels through a versioned C ABI; vendor implementation remains outside the learning repository.

Architecture:

```text
minitorch Python API
  → MiniTorch schema/Dispatcher
    → PrivateUse dispatch key
      → out-of-tree kernel registration
        → public vendor adapter ABI
          → private vendor runtime and libraries

MiniTorch compiler
  → supported graph partition/lowering
    → adapter graph compile/execute capability, when provided
```

Required MiniTorch components:

- `DeviceType::PrivateUse`, backend rename and one-registration-per-process policy;
- plugin discovery/loading with explicit path or package entry point, ABI/version check and unload/lifetime policy;
- device count/current/set/exchange and `DeviceGuard` behavior;
- device and pinned-host allocators, copy directions and asynchronous copy;
- current/default stream, stream pools, events, query/wait/synchronize and allocator-stream lifetime recording;
- Tensor/Storage construction plus `empty`, `empty_strided`, copy/to and view metadata preservation;
- schema-based operator/kernel registration, backend fallback and explicit unsupported errors;
- inference autocast policy, RNG state, serialization location tags and profiler activities;
- distributed transport/process-group capability when the vendor provides it;
- compiler capability query, supported graph partition, lowering/execute and eager fallback policy;
- positive, boundary, failure-injection and concurrency contract tests.

### Public adapter ABI

Use a C ABI so the adapter can be built with the vendor toolchain without exposing C++ standard-library ABI across the boundary. The final header is learner-authored, but its contract must include:

- ABI version, struct size, feature flags and runtime version query;
- opaque device, stream, event, allocation and compiled-graph handles;
- thread-local last-error retrieval or explicit status plus error object;
- device enumeration, property query, current/set device and synchronize;
- device/pinned allocation and free with size/alignment/device information;
- synchronous and asynchronous H2D/D2H/D2D copies;
- stream create/destroy/query/synchronize and event create/destroy/record/query/wait;
- kernel registry or launch entry points for the supported primitive set;
- optional graph compile/destroy/execute interface;
- optional RNG, profiler activity and collective interfaces;
- capability queries for dtype, layout, op, graph, stream/event and distributed support.

The loader requests a known ABI version and rejects incompatible `abi_version`, insufficient `struct_size`, missing mandatory function pointers or contradictory capability flags. Plugins return status codes; exceptions do not cross the C ABI.

### Out-of-tree plugin package

The private package supplies a shared library such as `libminitorch_vendor_adapter.so` and, when useful, Python metadata/entry points. MiniTorch owns dispatch, Tensor semantics and fallback policy; the adapter owns calls into the vendor runtime. A CPU mock adapter with the same ABI is committed for CI and fault injection.

## Route B — native PyTorch `PrivateUse1` backend

Build a separate out-of-tree package that integrates the real pinned PyTorch. Use the checked-in `OpenReg` test backend as the primary reference rather than inventing a parallel mechanism:

- overview and four-DSO boundary: `test/cpp_extensions/open_registration_extension/torch_openreg/README.md`;
- Python rename/generated helpers: `torch/utils/backend_registration.py`;
- device guard contract: `c10/core/impl/DeviceGuardImplInterface.h`;
- backend hooks: `aten/src/ATen/detail/PrivateUse1HooksInterface.h`;
- storage factory and dispatch registration example: `test/cpp_extensions/open_registration_extension.cpp`;
- runtime allocator/guard/stream/event/generator/hooks: `test/cpp_extensions/open_registration_extension/torch_openreg/csrc/runtime/`;
- operators and fallback: `test/cpp_extensions/open_registration_extension/torch_openreg/csrc/aten/`;
- AMP: `test/cpp_extensions/open_registration_extension/torch_openreg/csrc/amp/`;
- distributed process group: `test/cpp_extensions/open_registration_extension/torch_openreg/csrc/distributed/c10d/`;
- device, storage, memory, stream, event, RNG, AMP, profiler, distributed and compile tests: `test/cpp_extensions/open_registration_extension/torch_openreg/tests/`.

Required native-PyTorch integration increments:

1. package/autoload entry point, `rename_privateuse1_backend` and backend Python module registration;
2. `C10_REGISTER_GUARD_IMPL`, `PrivateUse1HooksInterface`, device/pinned allocator and Storage/Tensor factories;
3. mandatory factory/copy operators, selected `TORCH_LIBRARY_IMPL(aten, PrivateUse1, ...)` kernels and explicit fallback policy;
4. `AutogradPrivateUse1` boundary, `AutocastPrivateUse1`, RNG/generator, serialization and profiler;
5. stream/event plus allocator lifetime behavior;
6. Meta/Fake support for the selected operators and a custom `torch.compile` backend for graph lowering;
7. optional PrivateUse process group and TP/DP model slice when the vendor communication capability exists;
8. wheel, autoload, version/ABI matrix and pinned-PyTorch upgrade tests.

The native backend is not implemented by editing PyTorch core. It stays out-of-tree unless a focused learning patch to PyTorch itself is separately authorized.

## Shared primitive and model scope

Avoid reproducing the full ATen surface. Both routes use the same versioned capability manifest and a mechanism-complete primitive subset:

- Tensor creation/allocation/copy/view/reshape/transpose/slice/cat;
- elementwise add/mul plus one unary activation;
- reduction, matmul/Linear;
- one CNN kernel path;
- Embedding, normalization, Softmax and a naive attention composition;
- only the extra primitives required by the final CNN and decoder-block inference tests.

Target approximately 20–30 schemas and 10–15 backend-native kernels. Composite implementations should supply higher-level APIs where they preserve semantics. Adding an operator requires a target-model need or a new mechanism, not a desire to increase coverage count.

## Fallback policy

Every operation is classified as:

- native kernel on `VENDOR_DEVICE`;
- graph-compiler supported;
- safe composite decomposition whose children are supported;
- explicit CPU fallback with synchronization/copy and performance warning;
- unsupported with deterministic error.

Silent CPU execution while reporting a vendor device is forbidden. Tests assert output device, allocation ownership and dispatch trace, not only numerical values.

## Hardware conformance suite

The same suite runs against the CPU mock and the private real adapter:

1. ABI negotiation and missing-function/capability rejection;
2. device enumeration/current guard and multi-thread current-device behavior;
3. allocation alignment, zero-size, OOM, double-free rejection and leak counters;
4. H2D/D2H/D2D copies, pinned non-blocking copy and invalid direction/device cases;
5. stream ordering, event dependency, asynchronous error surfacing and allocator-stream lifetime;
6. Tensor creation/view/copy and device-preservation checks;
7. representative eager operator and explicit unsupported/fallback behavior;
8. autocast/RNG/serialization/profiler capability cases;
9. compiled graph equivalence and dynamic-shape rejection/recompile policy;
10. CNN/Transformer inference slice, memory statistics and repeated-run stability;
11. distributed/TP cases only when the capability manifest reports them.

The private hardware run stores only a sanitized capability/version identifier, test names, pass/fail, timing/memory summaries and known limitations. Raw vendor logs remain outside this repository.

## Gate

M8 passes only when Route A and Route B both pass contract-ready tests against their mock/runtime proxy. Final hardware readiness additionally requires a documented command bundle the learner can run privately. “Runs on the third-party hardware” may be recorded only after the real adapter passes device-smoke and representative-model gates.
