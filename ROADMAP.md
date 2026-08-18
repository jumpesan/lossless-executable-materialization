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

## Phase 2 — Generalization and representation shape

Status: multiple distinct artifact shapes now PASS; larger multi-chunk scaling is next.

```text
[x] second independent registered executable black-box exact-materialization PASS
[x] Unicode/newline-sensitive artifact exact-byte preservation PASS
[ ] P4 larger payload / three-chunk exact materialization — READY_FOR_BLACK_BOX
[ ] third artifact with another materially different source shape
[ ] tiny/empty/final-padding boundary cases
```

Current positive portability evidence includes:

```text
P1 primary executable / 19555 bytes / multi-chunk = PASS
P2 second registered executable / 5028 bytes / one chunk = PASS
P3 Unicode + mixed-newline executable / 422 bytes / one chunk = PASS
P4 larger executable / 13239 bytes / three chunks = READY
```

P3 confirms that mixed CRLF/LF and composed/decomposed Unicode distinctions can survive exact byte materialization without text normalization.

## Phase 3 — Execution-unit and dependency semantics

Status: representative executable-dependency and data-role controls PASS.

```text
[x] D2 declared multi-file execution unit positive control
[x] D3 required executable dependency omitted -> DENY
[x] D4 dependency canonical identity mismatch -> whole-unit DENY
[x] D5 DATA_REFERENCE remains non-executable read-only input
[x] D6 descriptor cannot promote DATA_REFERENCE into executable authority
[ ] cycle / duplicate executable dependency semantics
```

Current evidence supports:

```text
execution-unit membership != executable authority
data consumption != executable authority
descriptor claims != executable authority
```

Every executable member must independently satisfy authority and exact identity before the unit becomes execution-eligible.

## Phase 4 — Sandbox and filesystem safety

Representative v0.1 materialization preconditions are validated.

```text
[x] F0 clean isolated root
[x] F1 final target symlink -> DENY
[x] F2 ancestor symlink/root escape -> DENY
[x] F3 pre-existing final regular file -> DENY
[x] F4 failed staged identity leaves no final/staging residue
[x] F3 reasoning pressure: exact existing bytes do not imply cache/reuse authority
[ ] F5 repeated/concurrent attempt isolation
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

## Phase 5 — USER_DATA and untrusted-input separation

Status: representative v0.1 USER_DATA boundary U1-U5 is closed for the tested scope.

```text
[x] U1 USER_DATA cannot grant executable authority
[x] U2 USER_DATA cannot replace authority / representation revision
[x] U3 USER_DATA cannot replace chunk/base path/executable path/materialization target
[x] U4 execution-like USER_DATA remains inert data
[x] U5 malformed USER_DATA fails owner-input lane without rewriting materialization state
[ ] output provenance identifies execution inputs without leaking private data
[ ] broader arbitrary-input / serialization edge cases
```

The current controls support a separation between:

```text
artifact materialization state
!= owner-input validity
```

Malformed user data can deny owner invocation without retroactively changing a successful exact materialization result.

## Phase 6 — Cache / reuse

Status: design pending. F3 establishes the no-implicit-reuse baseline.

```text
[ ] cache identity key binds authority revision + path + canonical identity
[ ] re-verification policy
[ ] stale revision handling
[ ] corrupted cache detection
[ ] failed/unverified candidate never becomes execution-eligible cache
[ ] representation cache never becomes authority
```

## Phase 7 — Execution handoff

Status: partial; dependency and USER_DATA controls strengthened the boundary, but final owner handoff remains open.

```text
[ ] machine-readable materialization result
[ ] exact transition to EXECUTION_ELIGIBLE
[ ] owner execution interface
[ ] structured result contract
[ ] failure evidence contract
[x] compile/import occurs only after whole execution unit is eligible in representative controls
[x] owner-input validity is distinct from artifact execution eligibility
```

## Phase 8 — Cross-host / model portability

```text
[ ] another ChatGPT execution context
[ ] another model family
[ ] another LLM vendor/host
[ ] host with different Web retrieval behavior
[ ] host with different sandbox/network constraints
```

Current P1-P3 results demonstrate artifact/representation-shape portability within the observed host/model family; they do not establish cross-host portability.

## Phase 9 — Specification hardening

```text
[ ] descriptor schema refinement/finalization
[ ] machine/reference validator
[ ] normative failure codes
[ ] profile registry model
[ ] explicit retry semantics
[ ] version negotiation
[ ] upgrade / rollback semantics
[ ] authority binding to signed/provenance metadata
```

## Current recommended sequence

```text
1. P4 larger payload / three-chunk black-box exact materialization
2. descriptor schema refinement + machine validator
3. cache/reuse semantics + final execution-handoff validation
4. filesystem F5-F8 production hardening
5. cross-host/model portability
6. decide runtime manifest/schema integration only after the relevant gates close
```

## Publication thresholds

### Preliminary public release

**Current status: achieved/supportable** for a preliminary protocol-candidate release.

Current basis:

```text
positive exact materialization across multiple registered executable shapes
+ meaningful plain-source counterexample
+ fail-closed N-controls
+ representative filesystem safety controls
+ multi-file dependency authority/identity controls
+ DATA_REFERENCE role-separation controls
+ USER_DATA boundary controls
+ Unicode/newline exact-byte preservation
+ public synthetic reproduction fixture
+ explicit limitations
+ prior-art scan
+ open reproduction invitation
```

### Stronger protocol paper / preprint

Several previously preferred evidence items are now present: multi-file/dependency black-box evidence and Unicode/newline-sensitive exact-byte evidence.

Remaining high-value additions include:

```text
P4 larger multi-chunk PASS
+ descriptor/schema stabilization and machine validation
+ at least one cross-host/model result
+ cache/reuse semantics
+ clearer final execution-handoff contract
```

### Production integration

Requires substantially broader validation than publication, especially around filesystem concurrency/TOCTOU, cache/reuse, execution handoff, upgrades/rollback, broader input handling, dependency cycles, and host/platform portability.

The research should not collapse publication, stronger protocol claims, and production integration into one threshold.
