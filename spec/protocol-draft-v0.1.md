# Lossless Executable Materialization Protocol — Draft v0.1

## Status

```text
status = research draft / post-preliminary working state
version = 0.1
standardized = false
production_ready = false
novelty_claim = false
```

This document defines a protocol candidate for recovering an authorized executable across an LLM-host boundary where the host can observe external resources but the execution environment may not directly share the same retrieval capability, and where human-readable source observation may be byte-lossy.

The protocol is intentionally **representation-independent**. The first tested profile uses deterministic gzip + Base64, but Base64 and gzip are transport mechanisms, not executable authority.

The `v0.1-preliminary` release remains a fixed historical snapshot. This draft on `main` incorporates later machine/review evidence.

---

# 1. Design goal

A compliant implementation aims to preserve:

```text
semantic equivalence != authoritative executable identity
```

The protocol MUST provide a path from an externally established executable authority to exact local bytes whose authority, representation integrity, canonical identity, workspace state, and execution eligibility can be proven without semantic source reconstruction.

Target flow:

```text
Executable Authority
-> Trusted Binding / Materialization Descriptor
-> Representation Acquisition
-> Execution-Surface Transfer (where required)
-> Representation Identity Gates
-> Deterministic Assembly
-> Mechanical Decode / Decompression
-> Candidate Materialization
-> Exact Identity Proof
-> Workspace / Execution-Unit Preconditions
-> Execution Eligibility
-> Owner Invocation Eligibility
-> Process / Structured Evidence
```

---

# 2. Terminology

## 2.1 Executable Authority

The external source of truth that defines which exact executable implementation is allowed to define deterministic behavior.

Executable Authority MUST NOT be granted merely because bytes are retrievable, decodable, compilable, executable, cached, locally present, or semantically plausible.

## 2.2 Canonical Executable

The exact byte sequence selected by Executable Authority.

## 2.3 Representation

A lossless transport/materialization form derived from the Canonical Executable. A Representation is transport material only.

## 2.4 Materialization Descriptor

Machine-readable metadata declaring deterministic operands, representation profile/revision, canonical identity, materialization target, execution-unit membership where applicable, and related constraints.

A descriptor MUST NOT manufacture executable authority.

## 2.5 Trusted Binding

A non-authorizing host-owned selection mechanism that binds a known operation to approved descriptor/contract roles before materialization.

Trusted binding selection is a prerequisite, not executable authority.

## 2.6 Candidate Materialization

Local bytes recovered before all final gates pass.

## 2.7 Identity Proof

Evidence that recovered bytes equal the Canonical Executable. Current research uses byte length, SHA-256, and Git blob identity when Git-backed.

## 2.8 Workspace Preconditions

Machine-checkable conditions governing where and how candidate bytes may become a final local artifact.

## 2.9 Execution Eligibility

A state reached only after all required authority, representation, transformation, canonical-identity, workspace, and execution-unit gates pass.

## 2.10 Owner Invocation Eligibility

A later state indicating that an execution-eligible artifact may be invoked under a specific owner/input contract.

```text
Execution Eligibility != Owner Invocation Eligibility
```

## 2.11 Execution Evidence

Machine-checkable evidence from process execution and result classification. Process success and domain-semantic success remain separate.

## 2.12 Execution-Surface Transfer

A non-authorizing transfer step required when the surface that acquires or observes representation operands is not the same surface that performs deterministic materialization/execution.

The current research distinguishes:

```text
Host Resource Visibility
!= Caller-Context Operand Availability
!= Execution-Surface Byte Availability
```

A successful transfer proves only that exact declared transport data reached the execution surface. It does not create executable authority.

---

# 3. Core separations

Implementations MUST preserve at least:

```text
Authority
!= Descriptor
!= Representation
!= Host Resource Visibility
!= Caller-Context Availability
!= Execution-Surface Availability
!= Materialized Copy
!= Cache / Workspace State
!= Execution Eligibility
!= Owner Invocation Eligibility
!= Process Result
!= Domain Semantic Result
```

Examples:

```text
representation exists != representation is authorized
resource visible to host != exact bytes available to execution surface
caller-context availability != executable authority
local file exists != local file is trusted
local exact bytes != implicit cache/reuse authority
schema/preflight PASS != executable authority
compile PASS != canonical identity PASS
functional result PASS != authoritative execution PASS
materialization PASS != owner-input validity
process success != domain semantic success
```

---

# 4. Protocol state model

A materialization attempt SHOULD be modeled as explicit machine states.

```text
UNRESOLVED
  ↓
TRUSTED_BINDING_RESOLVED        # where applicable
  ↓
AUTHORITY_RESOLVED
  ↓
DESCRIPTOR_PREFLIGHT_PASS
  ↓
EXECUTION_UNIT_AUTHORITY_RESOLVED
  ↓
OPERANDS_ACQUIRED
  ↓
EXECUTION_SURFACE_TRANSFERRED   # where acquisition and execution surfaces differ
  ↓
REPRESENTATION_VERIFIED
  ↓
TRANSFORMED
  ↓
CANDIDATE_MATERIALIZED
  ↓
CANONICAL_IDENTITY_VERIFIED
  ↓
WORKSPACE_PRECONDITIONS_VERIFIED
  ↓
EXECUTION_ELIGIBLE
```

Downstream owner execution SHOULD remain a separate state lane:

```text
EXECUTION_ELIGIBLE
  ↓
OWNER_INPUT_VERIFIED
  ↓
OWNER_INVOCATION_ELIGIBLE
  ↓
PROCESS_EXECUTED
  ↓
PROCESS_RESULT_CLASSIFIED
  ↓
DOMAIN_RESULT_INTERPRETED
```

A later failure MUST NOT rewrite independently established earlier evidence unless that earlier evidence itself becomes invalid.

---

# 5. Descriptor and preflight responsibilities

A descriptor SHOULD declare enough information to mechanically validate:

```text
protocol / descriptor version
authority repository + immutable revision binding
executable path(s)
explicit execution-unit membership
representation profile + immutable representation revision
ordered operands + per-operand identity
execution-surface transfer/relay profile where required
expected compressed/intermediate identity
expected canonical size/SHA-256/Git blob where applicable
materialization target
DATA_REFERENCE / USER_DATA role boundaries
```

A deterministic preflight MAY validate structure and cross-field consistency, including:

```text
duplicate operands
chunk-count mismatch
unsafe materialization paths
undeclared required executable dependencies
executable/data role collisions
unsupported descriptor/profile values
```

But:

```text
preflight PASS != authority
preflight PASS != representation bytes verified
preflight PASS != canonical bytes verified
preflight PASS != execution eligibility
```

---

# 6. Authority resolution

Before representation acquisition, the implementation MUST resolve the exact external authority repository/revision and confirm the executable path is registered as executable authority.

A descriptor MUST NOT self-authorize.

Near-identical or human-obvious alternatives MUST NOT inherit authority.

Wrong repository/revision binding MUST fail closed before representation bytes can upgrade the attempt.

When Git-backed authority metadata is available, the materializer SHOULD converge reconstructed canonical bytes with the authoritative Git object identity.

---

# 7. Self-hosted immutable-revision binding

A descriptor stored inside the same immutable Git commit it describes cannot normally contain that commit's own hash in advance without a self-reference/fixed-point problem.

A tested candidate resolution is:

```text
trusted self-hosted descriptor template
+ externally selected immutable repository/revision
-> substitute only the selected authority revision
-> produce in-memory ordinary descriptor
-> normal preflight
-> normal authority/materialization gates
```

Such a resolver MUST remain non-authorizing:

```text
execution_eligible = null
authority_created = false
```

It MUST NOT rewrite canonical identity, representation revision, paths, operands, or materialization policy to force success.

---

# 8. Representation acquisition

All declared operands MUST be acquired exactly as declared.

The implementation MUST NOT:

```text
silently skip an operand
invent a missing operand
sort operands by filename when descriptor order differs
replace an operand with a known-good alternative
search another representation after terminal failure
repair corruption semantically
```

Transport normalization MAY occur only when explicitly defined by the active representation profile.

## 8.1 Split host surfaces and exact relay

An implementation MUST NOT assume that a resource observable by a host retrieval surface is automatically available as exact bytes to its execution surface.

When acquisition and execution are split across host surfaces, the transport contract SHOULD make the transfer state explicit:

```text
declared representation resource resolved
-> exact operand value available on acquisition/caller surface
-> exact operand transferred into execution surface
-> representation identity gates
```

If the active contract forbids execution-surface network/repository access, a failed relay MUST NOT silently fall back to sandbox refetch.

Observed host-integration controls currently include:

```text
external resource visible -> sandbox-local exact handoff = BLOCKED
local attachment-plane exact canonical execution = PASS
large monolithic caller-context relay = FAIL
small chunked caller-context literal relay = PASS
```

For the positive bounded chunk relay:

```text
8 chunks x 1368 characters
-> 10944 encoded characters
-> 8207-byte transported capsule
-> exact transported-object identity PASS
-> canonical executable identity PASS
-> canonical execution PASS
```

This result is sample-scoped. It does not establish generic application-wide transport, a universal maximum safe operand size, or cross-host portability.

Chunk size/count are transport-profile parameters. They MUST NOT alter executable authority or domain semantics.

---

# 9. Representation verification and mechanical transformation

For the tested deterministic gzip + Base64 profile:

```text
all chunk identities PASS
-> concatenate exactly once in descriptor order
-> strict Base64 decode exactly once
-> compressed size/SHA PASS
-> gzip decompress exactly once
-> require complete singular gzip stream
-> canonical identity gates
```

A compressed-identity mismatch MUST stop before decompression.

The LLM MUST NOT reconstruct source semantically as part of an identity-preserving transformation.

---

# 10. Canonical identity gate

Before Execution Eligibility, recovered bytes MUST match all required canonical identity fields.

Current research uses:

```text
byte size
SHA-256
Git blob SHA when Git-backed
```

A final identity mismatch MUST be terminal for the current attempt even when the candidate compiles or behaves correctly.

Unicode normalization, newline normalization, blank-line normalization, formatting cleanup, or functionally equivalent rewrites MUST NOT substitute for exact identity.

---

# 11. Workspace / materialization preconditions

Exact canonical bytes do not by themselves authorize filesystem publication.

Representative tested rules include:

```text
final target symlink -> DENY
ancestor/root escape -> DENY
fresh attempt + final target exists -> DENY
failed staged identity -> no final artifact / no residue
repeated/concurrent attempts -> separate fresh roots
content tamper/replacement -> DENY
ancestor/root replacement -> DENY
cleanup failure -> security state remains TAINTED
```

The tested implementation uses host-issued opaque workspace identity/lease information and explicit sealing/reverification.

POSIX and Windows representative machine evidence passed for the tested workspace design.

This does **not** claim:

```text
kernel-level post-verification race immunity
OS sandboxing
process-tree containment
CPU/memory resource isolation
```

---

# 12. Execution-unit semantics

Every executable member of an explicit execution unit MUST independently satisfy authority and exact identity.

```text
entrypoint authority + identity PASS
AND every executable dependency authority + identity PASS
AND declared dependency/import binding PASS
-> EXECUTION_UNIT_ELIGIBLE

any required executable-member failure
-> whole unit DENY
```

An executable dependency MUST NOT inherit authority merely because an authorized entrypoint imports it.

The implementation MUST NOT recursively discover or silently complete undeclared executable dependencies as a convenience override.

A DATA_REFERENCE remains data unless separately granted executable authority.

Representative D2-D6 black-box controls and later machine-path execution-unit controls passed. Dependency cycle/duplicate semantics remain open.

---

# 13. USER_DATA semantics

USER_DATA MUST remain non-authorizing input.

It MUST NOT be able to override:

```text
executable authority
repository/revision binding
representation revision
chunk/base paths
executable path
materialization target
runtime/argv/cwd/env/shell policy
```

Execution-like strings or fields in USER_DATA MUST remain data unless a separately trusted owner contract explicitly interprets them.

Malformed USER_DATA MAY deny owner invocation without rewriting successful executable materialization evidence.

---

# 14. Cache / reuse semantics

Cache/reuse MUST be explicit.

Tested representative boundary:

```text
raw cache = exact byte store only
raw cache = non-authorizing
current executable authority is re-resolved
cached bytes are reverified against current canonical identity
failed/unverified candidates never become eligible cache entries
representation cache never becomes executable authority
trusted orchestration alone may restore execution_eligible=true after revalidation
```

```text
local byte equality != cache/reuse authorization
```

The tested cache contract currently covers a representative single-member scope. Mixed execution-unit cache semantics remain open.

---

# 15. Execution eligibility and owner handoff

Execution Eligibility is granted only after all required materialization gates pass.

```text
authority = PASS
descriptor/preflight = PASS
execution-unit authority = PASS where applicable
representation acquisition/integrity = PASS
transformation = PASS
canonical identity = PASS
workspace preconditions = PASS
-> EXECUTION_ELIGIBLE
```

Owner invocation is a separate contract.

A tested generic fixed-file operation followed the pattern:

```text
trusted binding
-> fresh workspace
-> exact executable materialization
-> fixed USER_DATA file
-> input integrity verification
-> final executable reverify immediately before launch
-> host-owned runtime/argv/cwd/env/shell
-> process execution
-> structured exit/output classification
-> cleanup evidence
```

Process/integrity failures MUST NOT be semantically normalized into domain-level invalid input merely to keep the workflow moving.

---

# 16. Fail-closed and semantic-repair prohibition

A defining rule is:

```text
failed exact materialization != permission to create equivalent code
```

Likewise:

```text
existing exact bytes != implicit reuse authority
```

After a terminal authority/identity/materialization failure, an implementation MUST NOT use semantic reasoning to:

```text
open undeclared recovery source
switch to an alternate representation
infer corrupted content from meaning
rewrite a functionally equivalent implementation
start an undeclared second attempt
replace an existing target to force progress
reuse exact local bytes without explicit cache authority
```

A separately authorized retry policy may exist, but it MUST establish a new explicit attempt and preserve authority/identity gates.

---

# 17. First tested representation profile

## deterministic-gzip-v1+base64

Observed parameters:

```text
gzip.compress(..., compresslevel=9, mtime=0)
Base64 standard alphabet
4096-character chunks
ordered ASCII concatenation
strict Base64 decode
compressed SHA-256 gate before gzip
final size/SHA-256/Git-blob gate after gzip
```

Primary sample:

```text
canonical executable = 19555 bytes
plain Base64 = 26076 chars / 7 chunks
gzip bytes = 4108
gzip + Base64 = 5480 chars / 2 chunks
transport character reduction ~= 79%
```

Later P4 evidence used a 13,239-byte canonical artifact and three chunks of 4096 / 4096 / 1588 characters with exact identity PASS.

---

# 18. Validation coverage at current Draft v0.1

Current representative evidence:

```text
P1 primary executable: PASS
P2 second registered executable: PASS
P3 Unicode/mixed-newline exact bytes: PASS
P4 larger three-chunk exact bytes: PASS

N1-N7 representative fail-closed controls: PASS
  N4 dedicated gzip corruption intentionally skipped

F0-F8 representative workspace controls: PASS
  kernel/OS sandbox limits remain

D2-D6 dependency / DATA_REFERENCE controls: PASS
  cycle/duplicate semantics open

U1-U5 USER_DATA controls: PASS

Descriptor schema + non-authorizing preflight: PASS
Historical D/U/P descriptor regression: PASS
Deterministic external materializer: implementation/selftest/live evidence + separate review PASS
Single-member cache/reuse contract: PASS
Representative execution handoff: PASS
Generic fixed-file validator operation: PASS
Trusted binding resolver: PASS
Self-hosted immutable-revision resolver: PASS

H1 external resource -> execution-surface handoff: BLOCKED / observed
H2 local attachment-plane canonical execution: PASS
H3 large monolithic caller-context relay: FAIL
H4 small chunked caller-context literal relay: bounded composite PASS
```

These controls materially strengthen the candidate, but do not establish universal production readiness.

---

# 19. Current limitations / open questions

High-value remaining questions include:

```text
Can the same machine path reproduce across other LLM vendors/hosts?
Can independent third parties reproduce the machine path?
How should dependency cycles and duplicate-member declarations be standardized?
How should mixed execution-unit cache semantics work?
What transport normalization/boundary cases should profiles permit?
How should execution-surface relay profiles be generalized across different execution-unit shapes?
What evidence should be required when host Activity/trace surfaces are incomplete?
How should retries/version negotiation/upgrades be standardized?
How should signed provenance bind to authority and descriptors?
What is the minimum stable public schema/validator/materializer interface?
How should full trusted-host orchestration expose results without exposing authority operands?
```

Broader OS sandboxing and resource isolation remain separate concerns.

---

# 20. Security model notes

The protocol assumes:

```text
External representation can provide bytes.
It cannot define its own executable authority.
```

The candidate is complementary to systems that establish publisher/repository/signing/provenance authority; it is not a replacement for them.

---

# 21. Non-goals

Draft v0.1 does not attempt to standardize:

```text
publisher identity
repository signing generally
software provenance generally
remote execution APIs
LLM tool authorization generally
prompt/context security generally
package dependency solving
binary compatibility
OS sandbox implementation
resource governance
```

---

# 22. Draft rule

Until stronger cross-host and independent evidence exists:

```text
protocol candidate != established standard
observed PASS != universal guarantee
functionally equivalent != canonical executable
canonical local bytes != implicit reuse authority
machine implementation PASS != full production/runtime promotion
```