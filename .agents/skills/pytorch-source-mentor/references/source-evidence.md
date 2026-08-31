# Source evidence and debugging

## Claim discipline

Label important conclusions as:

- **Observed:** directly inspected in this checkout or command output.
- **Documented:** supported by an official source, with URL and access date.
- **Inferred:** a reasoned interpretation that still needs verification.

For changing internals, source paths must be relative to the resolved PyTorch source root and tied to `git -C <source-root> rev-parse HEAD`. Never substitute the outer learning-system commit. Generated files must be identified as generated; find their generator or schema before treating them as authoritative design intent.

## Checkout identity gate

Before relying on local source, verify all of the following:

- the configured source root exists and contains PyTorch's `torch/`, `aten/`, and `c10/` trees;
- `git -C <source-root> status --short --branch` succeeds;
- the exact commit is recorded, and an expected tag is verified rather than inferred;
- recursive submodules are initialized; leading `-`, `+`, or `U` markers from `git submodule status --recursive` are unresolved evidence limitations;
- local source changes are reported before tracing or testing against them.

If the gate fails, diagnose it without mutating the checkout. Fetching, switching revisions, cleaning, resetting, or updating submodules requires explicit learner authorization.

## Call-chain artifact

Every substantive trace should capture:

1. input program and tensor metadata;
2. public Python entry point;
3. binding or generated wrapper;
4. operator schema and overload;
5. active `DispatchKeySet` or equivalent selection evidence;
6. selected kernel/fallback and registration site;
7. important `TensorImpl`/`StorageImpl`/allocator effects;
8. output and observed verification;
9. unresolved branches.

Do not force all nine when a layer is genuinely absent; explain the absence.

## Debugging ladder

Escalate only as needed:

1. `rg` symbols, schemas, registrations, and `Note [...]` comments.
2. Python introspection and dispatcher inspection utilities present in the checkout.
3. focused Python/C++ test with a one-operation input.
4. logging/environment diagnostics documented by the checkout.
5. Python and native stack traces.
6. debugger breakpoint on a verified symbol.
7. temporary instrumentation or learning patch.

Before a command, state what result would confirm or refute the hypothesis. Afterward, record command, exit status, key output, interpretation, and limitations.

## Review checklist

- Is the exact revision recorded?
- Did the learner distinguish API contract from current implementation?
- Is each important arrow supported by source or runtime evidence?
- Were overload, dispatch key, device, dtype, layout, and execution mode specified?
- Were Python and C++ lifetime/ownership implications understood?
- Can the learner reproduce the trace without the mentor?
