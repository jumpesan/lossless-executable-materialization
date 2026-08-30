# Research Roadmap

This roadmap separates **evidence needed for publication**, **evidence needed for stronger protocol claims**, and **evidence needed for full production/runtime integration**.

The `v0.1-preliminary` release remains a fixed historical snapshot. This roadmap tracks later work on `main`.

## Phase 0 — Preliminary feasibility

Status: complete for the tested scope.

```text
[x] human-readable source counterexample: functional PASS / byte identity FAIL
[x] plain Base64 exact materialization: GPT-5.6 Instant
[x] plain Base64 exact materialization: GPT-5.6 High
[x] deterministic gzip + Base64 exact materialization: GPT-5.6 Instant
[x] independent artifact verification
[x] initial broad prior-art scan
```

## Phase 1 — Fail-closed semantics

Status: strong representative coverage.

```text
[x] N1 missing operand
[x] N2 counterintuitive declared order
[x] N3 one-character transport corruption
[x] N5 final canonical identity mismatch
[x] N6 unregistered near-identical executable
[x] N7 explicit semantic-repair temptation after terminal failure
[x] duplicate chunk deterministic preflight denial
[x] wrong/stale authority or representation revision denial in machine path
[x] unsupported representation profile denial in machine path
[ ] transport-normalization/ASCII-whitespace profile edges
```

N4 dedicated gzip corruption remains optional because the tested contract rejects corrupted compressed identity before decompression.

## Phase 2 — Generalization and representation shape

Status: required P1-P4 representative controls closed.

```text
[x] second independent registered executable exact-materialization PASS
[x] Unicode/newline-sensitive artifact exact-byte preservation PASS
[x] P4 larger payload / three-chunk exact materialization PASS
[ ] third artifact with another materially different source shape
[ ] tiny/empty/final-padding boundary cases
```

Current positive portability evidence:

```text
P1 primary executable / 19555 bytes / multi-chunk = PASS
P2 second registered executable / 5028 bytes / one chunk = PASS
P3 Unicode + mixed-newline executable / 422 bytes / one chunk = PASS
P4 larger executable / 13239 bytes / three chunks = PASS
```

These results remain within the observed host/model family and do not establish cross-host portability.

## Phase 3 — Execution-unit and dependency semantics

Status: representative executable-dependency and data-role controls PASS.

```text
[x] D2 declared multi-file execution unit positive control
[x] D3 required executable dependency omitted -> DENY
[x] D4 dependency canonical identity mismatch -> whole-unit DENY
[x] D5 DATA_REFERENCE remains non-executable read-only input
[x] D6 descriptor cannot promote DATA_REFERENCE into executable authority
[x] machine path verifies all declared executable-member authority before representation processing
[ ] cycle / duplicate executable dependency semantics
```

Current evidence supports:

```text
execution-unit membership != executable authority
data consumption != executable authority
descriptor claims != executable authority
```

## Phase 4 — Sandbox and workspace safety

Status: representative F0-F8 workspace behavior validated.

```text
[x] F0 clean isolated root
[x] F1 final target symlink -> DENY
[x] F2 ancestor symlink/root escape -> DENY
[x] F3 pre-existing final regular file -> DENY
[x] F4 failed staged identity leaves no final/staging residue
[x] F3 exact existing bytes do not imply reuse authority
[x] F5 repeated/concurrent attempt isolation
[x] F6 ancestor/root replacement and tested TOCTOU-style detection
[x] F7 cleanup failure -> monotonic TAINTED state
[x] F8 explicit POSIX/Windows behavior + cross-platform CI
[ ] kernel-level post-verification race immunity
[ ] OS sandbox/process-tree/resource isolation
[ ] final materialized permission policy beyond tested workspace scope
```

Cache/reuse remains explicit and separate from filesystem convenience.

## Phase 5 — USER_DATA and untrusted-input separation

Status: representative v0.1 USER_DATA boundary U1-U5 closed.

```text
[x] U1 USER_DATA cannot grant executable authority
[x] U2 USER_DATA cannot replace authority / representation revision
[x] U3 USER_DATA cannot replace chunk/base path/executable path/materialization target
[x] U4 execution-like USER_DATA remains inert data
[x] U5 malformed USER_DATA fails owner-input lane without rewriting materialization state
[x] generic fixed-file operation reverifies USER_DATA integrity before execution
[ ] broader arbitrary-input / serialization edge cases
[ ] privacy-preserving provenance conventions for sensitive input
```

The current controls support:

```text
artifact materialization state != owner-input validity
```

## Phase 6 — Descriptor schema / machine preflight / materializer

Status: representative machine path implemented and reviewed in a separate review lane.

```text
[x] descriptor structural schema
[x] deterministic non-authorizing preflight
[x] historical D/U/P positive/negative descriptor regression
[x] wrong repository/revision binding denial
[x] wrong/stale representation revision denial
[x] strict external authority + representation + canonical materializer
[x] exact authority Git-object / reconstructed Git-object convergence
[x] one-member live external materialization probe
[x] multi-member materializer selftest
[x] self-hosted immutable-revision descriptor resolution without self-authorization
[ ] public reference schema/validator package stabilization
[ ] normative profile/version registry
```

Important boundary:

```text
schema/preflight PASS != executable authority
```

## Phase 7 — Cache / reuse

Status: representative single-member cache contract PASS.

```text
[x] raw cache is a non-authorizing byte store
[x] cache use requires current authority resolution
[x] cached exact bytes are reverified
[x] failed/unverified candidate cannot become execution-eligible cache
[x] representation cache cannot become executable authority
[x] trusted orchestrator alone may restore execution_eligible=true after revalidation
[ ] mixed execution-unit cache orchestration
[ ] broader distributed/stale-cache topologies
```

## Phase 8 — Execution handoff

Status: representative execution-handoff contract and generic fixed-file validator operation PASS.

```text
[x] machine-readable materialization result
[x] explicit transition to EXECUTION_ELIGIBLE
[x] execution eligibility separated from owner invocation eligibility
[x] process success separated from domain semantic result
[x] trusted runtime/argv/cwd/env/shell ownership in tested operation
[x] fixed USER_DATA integrity reverification before launch
[x] structured result / accepted exit classification
[x] cleanup evidence and failure-domain preservation
[ ] arbitrary owner execution interfaces
```

## Phase 8A — Host-surface transfer / trusted-host integration

Status: bounded relay primitive established; generic cross-unit transport remains open.

```text
[x] H1 observe external transport while sandbox-local exact handoff is unavailable
[x] H2 local attachment-plane canonical execution PASS across low/high reasoning endpoints
[x] H2 representative owner-input semantic-negative result remains fail-closed
[x] H3 large monolithic caller-context relay FAIL under no-refetch contract
[x] H4 small chunked caller-context literal relay PASS
[ ] unit-agnostic execution-surface relay descriptor/profile
[ ] deterministic transport builder from immutable registered inputs
[ ] dynamic chunk count + per-chunk identity + final transported-object identity
[ ] cross-unit proof across materially different input/dependency shapes
[ ] full trusted-host end-to-end integration across all reviewed primitives
```

Current bounded evidence supports:

```text
resource observable by host
!= caller-context exact operand availability
!= execution-surface exact byte availability
```

It does not establish a universal safe chunk size or generic application-wide transport.

## Phase 9 — Trusted runtime binding

Status: representative non-authorizing binding controls PASS.

```text
[x] trusted operation/binding selection is host-owned
[x] unknown operation denied before referenced reads
[x] descriptor/contract role binding checked before use
[x] binding cannot select repository-reader implementation
[x] binding itself grants no executable authority
[x] self-hosted descriptor resolver substitutes only externally selected immutable revision
[ ] broader provider/transport implementations
```

## Phase 10 — Cross-host / model portability

Status: open.

```text
[ ] another ChatGPT execution context with materially different retrieval behavior
[ ] another model family
[ ] another LLM vendor/host
[ ] host with different sandbox/network constraints
[ ] independent third-party reproduction of the machine path
```

P1-P4 show artifact/representation-shape portability only within the observed host/model family.

## Phase 11 — Specification hardening

```text
[ ] stabilize public machine-readable descriptor schema
[ ] stabilize public reference validator/materializer interface
[ ] normative failure-code registry
[ ] representation profile registry
[ ] explicit retry semantics
[ ] version negotiation
[ ] upgrade / rollback semantics
[ ] signed/provenance metadata binding model
[ ] decide whether a v0.2 protocol draft or preprint is warranted
```

## Current recommended sequence

```text
1. keep current machine/review and host-surface relay evidence synchronized in the public record
2. generalize the bounded execution-surface relay into a unit-agnostic, deterministic transport contract/builder
3. prove the same relay/materializer across multiple execution-unit input/dependency shapes
4. complete full trusted-host end-to-end integration without widening authority
5. exercise remaining dependency/cache/transport boundary cases
6. obtain cross-host/vendor and ideally third-party reproduction evidence
7. stabilize the public descriptor/validator/materializer surface
8. consider a stronger protocol paper/preprint or v0.2 draft
9. keep live/runtime promotion and final release as separate authorization decisions
```

## Publication thresholds

### Preliminary public release

**Achieved/supportable.**

The existing `v0.1-preliminary` release remains a valid historical preliminary snapshot.

### Stronger protocol paper / preprint

The evidence base is now materially stronger than at preliminary release:

```text
P1-P4 exact materialization
+ multi-file/dependency controls
+ DATA_REFERENCE / USER_DATA separation
+ deterministic schema/preflight/materializer path
+ representative cache/reuse contract
+ representative execution handoff
+ F0-F8 workspace hardening
+ trusted non-authorizing binding/resolution
+ bounded host-surface transfer evidence (H1-H4)
```

High-value remaining additions:

```text
cross-host/vendor reproduction
+ third-party machine-path reproduction
+ remaining dependency/cache edge cases
+ generic cross-unit execution-surface transfer
+ public schema/interface stabilization
+ full trusted-host integration evidence
```

### Production/runtime integration

Substantially advanced, but **not complete**.

The current evidence does not claim:

```text
kernel-level race immunity
OS sandbox/resource isolation
arbitrary owner-interface coverage
mixed-unit cache completeness
cross-host universality
live/runtime promotion completion
```

Publication, stronger protocol claims, and production/runtime promotion remain separate thresholds.