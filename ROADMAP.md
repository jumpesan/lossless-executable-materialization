# Research Roadmap

This roadmap separates **evidence needed for publication**, **evidence needed for stronger protocol claims**, and **evidence needed for production integration**.

## Phase 0 — Preliminary feasibility

Status: substantially complete for the primary sample.

```text
[x] human-readable source counterexample: functional PASS / byte identity FAIL
[x] plain Base64 exact materialization: GPT-5.6 Instant
[x] plain Base64 exact materialization: GPT-5.6 High
[x] deterministic gzip + Base64 exact materialization: GPT-5.6 Instant
[x] independent artifact verification
[x] initial broad prior-art scan
```

## Phase 1 — Fail-closed semantics

Status: strong for the primary sample, not universal.

```text
[x] N1 missing operand
[x] N2 counterintuitive declared order
[x] N3 one-character transport corruption
[x] N5 final canonical identity mismatch
[x] N6 unregistered near-identical executable
[x] N7 explicit semantic-repair temptation after terminal failure
[ ] duplicate operand declaration
[ ] stale/wrong representation revision
[ ] transport-normalization edge cases
```

## Phase 2 — Generalization beyond one executable

```text
[ ] second independent registered executable black-box PASS
[ ] third artifact with materially different source shape
[ ] Unicode/newline-sensitive artifact
[ ] larger payload / many chunks
[ ] tiny/empty/final-padding boundary cases
```

## Phase 3 — Execution-unit semantics

```text
[ ] multi-file execution unit
[ ] declared executable dependency identity
[ ] undeclared executable dependency rejection
[ ] dependency identity mismatch rejection
[ ] data dependency does not inherit executable authority
[ ] cycle / duplicate dependency semantics
```

## Phase 4 — Sandbox and filesystem safety

```text
[ ] canonical output base directory
[ ] path traversal rejection
[ ] absolute-path rejection
[ ] overwrite policy
[ ] symlink / alias behavior where relevant
[ ] materialized file permissions
```

## Phase 5 — User data and context separation

```text
[ ] USER_DATA cannot grant executable authority
[ ] USER_DATA cannot modify descriptor identity requirements
[ ] executable receives only declared user-data operands
[ ] user data is not treated as instruction during mechanical materialization
[ ] output provenance identifies execution inputs without leaking private data
```

## Phase 6 — Cache / reuse

```text
[ ] cache identity key
[ ] re-verification policy
[ ] stale revision handling
[ ] corrupted cache detection
[ ] cache never becomes authority
```

## Phase 7 — Execution handoff

```text
[ ] machine-readable materialization result
[ ] exact transition to EXECUTION_ELIGIBLE
[ ] owner execution interface
[ ] structured result contract
[ ] failure evidence contract
```

## Phase 8 — Portability

```text
[ ] another ChatGPT execution context
[ ] another model family
[ ] another LLM vendor/host
[ ] host with different Web retrieval behavior
[ ] host with different sandbox/network constraints
```

## Phase 9 — Specification hardening

```text
[ ] descriptor schema
[ ] reference validator
[ ] normative failure codes
[ ] profile registry model
[ ] explicit retry semantics
[ ] version negotiation
[ ] upgrade / rollback semantics
[ ] authority binding to signed/provenance metadata
```

## Publication thresholds

### Preliminary public release

Already supportable if clearly framed as preliminary:

```text
positive exact materialization evidence
+ meaningful negative counterexample
+ fail-closed controls
+ limitations
+ prior-art scan
+ open reproduction invitation
```

### Stronger protocol paper / preprint

Prefer:

```text
>= 2 independent executables
+ multi-file/dependency evidence
+ deliberate corruption controls
+ Unicode/large-payload edge cases
+ at least one cross-host/model result
```

### Production integration

Requires substantially broader validation than publication.

The research should not collapse those thresholds into one.