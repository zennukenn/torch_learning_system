# Error and misconception log

Track recurring misconceptions and debugging failures, not every typo.

| Date | Concept/error | Learner hypothesis | Evidence that corrected it | Root misconception | Review date | Resolved? |
|---|---|---|---|---|---|---|
| 2026-09-02 | `c10` ownership | `c10` contains communication operators | `c10/core/DispatchKey.h` and repository map; communication anchors are under `torch/distributed/` and `torch/csrc/distributed/` | Repository subsystem boundaries not established | 2026-09-03 | no |
| 2026-09-02 | `Tensor` pass-by-value | `const Tensor&` avoids allocating duplicate tensor data | `BinaryOps.cpp:151`; `Tensor` is a wrapper and pass-by-value does not copy underlying storage | Wrapper copy versus storage copy not distinguished | 2026-09-03 | no |
