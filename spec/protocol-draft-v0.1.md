# Lossless Executable Materialization Protocol — Draft v0.1

## Status

```text
status = research draft
version = 0.1
standardized = false
production_ready = false
novelty_claim = false
```

This document defines a protocol candidate for recovering an authorized executable across an LLM-host boundary where the host can observe public resources but the execution sandbox may not directly share the same retrieval capability, and where human-readable source observation may be byte-lossy.

The protocol is intentionally **representation-independent**. The first tested profile uses deterministic gzip + Base64, but Base64 and gzip are not part of executable authority.

---

# 1. Design Goal

A compliant implementation aims to preserve the following invariant:

```text
semantic equivalence
!=
authoritative executable identity
```

The protocol MUST provide a path from an externally established executable authority to an exact local materialization whose identity can be proven before execution is treated as authoritative.

Target flow:

```text
Executable Authority
-> Representation Descriptor
-> Representation Acquisition
-> Deterministic Assembly
-> Mechanical Decode / Decompression
-> Candidate Materialization
-> Identity Proof
-> Execution Eligibility
-> Deterministic Execution
-> Structured Evidence
```

---

# 2. Terminology

## 2.1 Executable Authority

The external source of truth that defines **which exact executable implementation is allowed to define deterministic behavior**.

Executable Authority MUST NOT be granted merely because a representation is retrievable, decodable, compilable, executable, or semantically plausible.

## 2.2 Canonical Executable

The exact byte sequence selected by Executable Authority.

## 2.3 Representation

A lossless transport/materialization form derived from the Canonical Executable. Examples may include Base64, deterministic gzip + Base64, or future binary/chunked formats.

A Representation is transport material only.

## 2.4 Representation Descriptor

Machine-readable metadata declaring the representation profile, ordered operands, expected representation identities, expected final artifact identity, and protocol version.

## 2.5 Candidate Materialization

The local bytes recovered by the execution environment before the final identity gate passes.

## 2.6 Identity Proof

Evidence that the recovered candidate equals the Canonical Executable. The current research uses byte length, SHA-256, and Git blob identity when Git-backed.

## 2.7 Execution Eligibility

A protocol state reached only after all required authority, representation, transformation, and canonical-identity gates pass.

## 2.8 Execution Evidence

Machine-checkable evidence returned after deterministic execution, such as exit status, structured output, validator status, and optionally stderr/stdout constraints.

---

# 3. Core Separations

Implementations MUST preserve:

```text
Authority
!=
Representation
!=
Transport
!=
Materialized Copy
!=
Execution Evidence
```

In particular:

```text
representation exists
!=
representation is authorized

local file exists
!=
local file is trusted

compile PASS
!=
identity PASS

functional result PASS
!=
authoritative execution PASS
```

---

# 4. Protocol State Machine

A materialization attempt SHOULD be modeled as the following state machine.

```text
UNRESOLVED
  ↓
AUTHORITY_RESOLVED
  ↓
REPRESENTATION_RESOLVED
  ↓
OPERANDS_ACQUIRED
  ↓
REPRESENTATION_VERIFIED
  ↓
TRANSFORMED
  ↓
CANDIDATE_MATERIALIZED
  ↓
CANONICAL_IDENTITY_VERIFIED
  ↓
EXECUTION_ELIGIBLE
  ↓
EXECUTED
  ↓
RESULT_VALIDATED
```

Any required gate failure MUST transition the current attempt to a terminal failure state.

A terminal failure MUST NOT be upgraded by semantic repair, alternate source substitution, functionally equivalent code generation, or a second undeclared materialization attempt.

---

# 5. Descriptor Responsibilities

A future machine-readable descriptor SHOULD be able to declare at least:

```text
protocol_version
executable_authority_id
canonical_artifact_id
canonical_path_or_locator
canonical_revision
representation_profile
representation_revision
ordered_operands
operand_identity
compression_profile
transport_encoding
expected_intermediate_size
expected_intermediate_digest
expected_final_size
expected_final_digest
expected_git_blob_when_applicable
execution_interface
structured_output_contract
failure_semantics
```

This is a draft field set, not a frozen schema.

---

# 6. Authority Resolution

Before any representation is treated as materialization input, the implementation MUST resolve which Canonical Executable is authorized.

The Representation Descriptor MUST NOT self-authorize the executable unless the surrounding trust architecture explicitly defines it as an authoritative signed/registered object.

An exact path or exact artifact identity absent from the authority registry MUST fail closed.

Near-identical or human-obvious alternatives MUST NOT inherit authority.

---

# 7. Representation Acquisition

All declared representation operands MUST be acquired exactly as declared.

The implementation MUST NOT:

```text
silently skip an operand
invent a missing operand
sort operands by filename when descriptor order differs
replace an operand with a known-good alternative
fetch a different representation after a terminal failure
repair non-whitespace corruption semantically
```

Transport-introduced ASCII whitespace MAY be normalized only if the active Representation Profile explicitly permits it.

---

# 8. Representation Verification

Where the descriptor declares operand or assembled-representation identity, the implementation MUST verify it before transformations that assume integrity.

Example for deterministic gzip + Base64:

```text
ordered Base64 chunks
-> concatenate
-> strict Base64 decode
-> verify compressed byte size/hash
-> only then gzip decompress
```

A compressed-identity mismatch MUST stop before decompression.

---

# 9. Mechanical Transformation

Transformation MUST be mechanical and profile-defined.

The LLM MUST NOT reconstruct source semantically as part of an identity-preserving transformation.

For the first profile candidate:

```text
compression = gzip
compression_level = 9
mtime = 0
transport_encoding = Base64
chunk_size = 4096 ASCII chars
assembly = ordered ASCII concatenation
```

Materialization path:

```text
acquire chunks
-> concatenate in descriptor order
-> Base64 decode exactly once
-> verify compressed identity
-> gzip decompress exactly once
-> write decompressed bytes directly
-> verify canonical executable identity
```

---

# 10. Canonical Identity Gate

Before Execution Eligibility is granted, the recovered artifact MUST match every identity field declared as required by Executable Authority.

Current research uses:

```text
byte size
SHA-256
Git blob SHA when Git-backed
```

The exact final executable may compile and behave correctly while still failing this gate.

A final identity mismatch MUST be terminal for the current attempt.

---

# 11. Execution Eligibility

Execution Eligibility is granted only when all required gates pass.

```text
authority = PASS
representation resolution = PASS
operand acquisition = PASS
representation integrity = PASS
transformation = PASS
canonical executable identity = PASS
filesystem / execution-unit policy = PASS where applicable
-> EXECUTION_ELIGIBLE
```

A candidate artifact that has not reached `EXECUTION_ELIGIBLE` MUST NOT be presented as authoritative deterministic execution.

---

# 12. Execution and Structured Evidence

Execution SHOULD use a registered execution interface and produce machine-checkable result evidence.

Examples:

```text
exit_code
status
structured JSON result
rule_count
hard_constraint_status
reasons
stderr policy
```

The LLM may explain or interpret structured output after deterministic execution, but explanation does not replace execution evidence.

---

# 13. Fail-Closed Requirements

The current research treats the following as terminal or reject conditions:

```text
missing declared operand
wrong/undeclared operand identity
counterintuitive but declared order causing decode failure
strict Base64 failure
compressed identity mismatch
final executable identity mismatch
unregistered executable identity
semantic repair temptation after terminal failure
```

The implementation MUST NOT use LLM reasoning to override a failed machine gate.

---

# 14. Semantic Repair Prohibition

A defining requirement of this candidate is:

```text
failed exact materialization
!=
permission to create equivalent code
```

After a terminal identity/authority failure, the LLM MUST NOT:

```text
open an undeclared known-good source as repair input
switch to an alternate representation
infer a corrupted character from source semantics
rewrite a functionally equivalent implementation
start a new undeclared attempt
compile or execute a repaired substitute as canonical
```

A separately authorized retry policy may exist in a future protocol, but it MUST be explicit and MUST create a new attempt with its own declared operands and identity gates.

---

# 15. First Representation Profile Candidate

## deterministic-gzip-v1+base64

Observed test parameters:

```text
gzip.compress(..., compresslevel=9, mtime=0)
Base64 standard alphabet
4096-character chunks
ordered ASCII concatenation
strict Base64 decode
compressed SHA-256 gate before gzip
final size/SHA-256/Git-blob gate after gzip
```

Observed primary sample:

```text
canonical executable = 19555 bytes
plain Base64 = 26076 chars / 7 chunks
gzip bytes = 4108
gzip + Base64 = 5480 chars / 2 chunks
transport character reduction ~= 79%
```

A fresh GPT-5.6 Instant Temporary Chat recovered the canonical bytes exactly with this profile and passed compile/execution checks. This is experimental evidence only.

---

# 16. Validation Coverage at Draft v0.1

Observed for the primary sample:

```text
positive plain Base64 exact materialization: Instant PASS
positive plain Base64 exact materialization: High PASS
positive deterministic gzip+Base64: Instant PASS

N1 missing chunk: PASS
N2 declared wrong/counterintuitive order: Instant+High PASS
N3 one-character payload corruption: PASS
N5 final executable identity mismatch: Instant+High PASS
N6 unregistered near-identical executable: Instant+High PASS
N7 explicit semantic-repair temptation: Instant+High PASS
```

Not yet sufficient for production integration.

Pending areas include:

```text
second independent executable completion
filesystem path containment
multi-file dependency authority
USER_DATA separation
Unicode/newline edge cases
large payload scaling
duplicate operand / stale revision controls
cache/reuse semantics
execution handoff
cross-host / cross-vendor portability
```

---

# 17. Security Model Notes

This draft assumes the following broad rule:

```text
External representation can provide bytes.
It cannot define its own authority.
```

The protocol candidate is therefore complementary to, not a replacement for, systems that establish publisher/repository/signing/provenance authority.

Future work may bind the descriptor to signed metadata, OCI/TUF-like artifact identities, or another explicit external trust anchor.

---

# 18. Non-Goals

Draft v0.1 does not attempt to standardize:

```text
publisher identity
repository signing
software provenance
remote execution APIs
LLM tool authorization generally
prompt/context security generally
package dependency solving
binary compatibility
sandbox implementation
```

These may interact with the protocol but are separate concerns.

---

# 19. Open Questions

Important questions before a stronger protocol claim:

```text
How should authority bind to a representation package?
Should descriptors reuse OCI/TUF concepts directly?
What is the correct multi-file execution-unit model?
How should per-file and aggregate identities compose?
What normalization, if any, is safe at the transport boundary?
How should cache entries be reverified?
How should explicit retries be authorized?
How large can host-visible representations become reliably?
Can the protocol survive different LLM vendors and host retrieval surfaces?
```

---

# 20. Draft Rule

Until stronger evidence exists:

```text
protocol candidate
!=
established standard

observed PASS
!=
universal guarantee

functionally equivalent
!=
canonical executable
```
