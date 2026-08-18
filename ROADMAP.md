# Research Roadmap

This roadmap separates **evidence needed for publication**, **evidence needed for stronger protocol claims**, and **evidence needed for production integration**.

## Phase 0 — Preliminary feasibility

Status: complete for the current positive-control scope.

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

N4 dedicated gzip corruption remains intentionally skipped because N3 already proves the required compressed-identity gate before decompression.

## Phase 2 — Generalization beyond one executable

```text
[x] second independent registered executable black-box exact-materialization PASS
[ ] third artifact with materially different source shape
[ ] Unicode/newline-sensitive artifact
[ ] larger payload / many chunks
[ ] tiny/empty/final-padding boundary cases
```

The second executable confirms exact materialization/identity portability across two distinct registered single-file artifacts. Full domain execution for that control was intentionally outside scope because its owner contract requires additional state.

## Phase 3 — Execution-unit semantics

Status: dependency fixture prepared; black-box controls next.

```text
[ ] D2 declared multi-file execution unit positive control
[ ] D3 undeclared executable dependency rejection
[ ] D4 dependency identity mismatch rejection
[ ] D5 data dependency does not inherit executable authority
[ ] cycle / duplicate dependency semantics
```

Preparation already complete:

```text
[x] real two-file registered execution unit selected
[x] deterministic representation generated
[x] independent round-trip identity verification
[x] declared import binding verification
```

Prepared controls are not counted as PASS until black-box runs complete.

## Phase 4 — Sandbox and filesystem safety

Representative v0.1 materialization preconditions are now validated.

```text
[x] F0 clean isolated root
[x] F1 final target symlink -> DENY
[x] F2 ancestor symlink/root escape -> DENY
[x] F3 pre-existing final regular file -> DENY
[x] F4 failed staged identity leaves no final/staging residue
[x] F3 reasoning pressure: exact existing bytes do not imply cache/reuse authority
[ ] F5 concurrency/race controls
[ ] F6 TOCTOU hardening
[ ] F7 cleanup-taint semantics
[ ] F8 Windows/POSIX behavior
[ ] final materialized permission policy
```

Current baseline:

```text
fresh attempt + existing final target -> DENY
```

Cache/reuse remains a separate phase rather than an inferred filesystem convenience.

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
[ ] descriptor schema finalization
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

**Current status: supportable**, provided the repository remains clearly framed as preliminary research / protocol candidate.

Current basis:

```text
positive exact materialization across two registered single-file executables
+ meaningful plain-source counterexample
+ fail-closed N-controls
+ representative filesystem safety controls
+ public synthetic reproduction fixture
+ explicit limitations
+ prior-art scan
+ open reproduction invitation
```

### Stronger protocol paper / preprint

Prefer:

```text
multi-file/dependency black-box evidence
+ deliberate corruption controls across execution units
+ Unicode/large-payload edge cases
+ at least one cross-host/model result
+ clearer descriptor/schema stabilization
```

### Production integration

Requires substantially broader validation than publication, especially around filesystem concurrency, cache/reuse, user-data separation, dependency closure, execution handoff, upgrades, and host portability.

The research should not collapse those thresholds into one.
