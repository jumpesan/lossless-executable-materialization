# Preliminary Technical Report
# Lossless Executable Materialization Across an LLM Host Boundary

## Status

```text
created: 2026-08-18
report_type: public-facing preliminary technical report
research_stage: feasibility established for observed samples
protocol_status: candidate / not standardized
production_status: not established
novelty_claim: not established
```

**Author:** Jumpei Fujii  
**Public release license:** CC BY 4.0  
**AI assistance:** Extensive; see [AI_ASSISTANCE.md](../AI_ASSISTANCE.md)

---

# Abstract

This report describes an empirical investigation that emerged while exploring whether **structured Context plus deterministic Scripts can make a general-purpose ChatGPT/LLM environment behave as an application runtime**.

The work did not begin as a transport-protocol project. The broader goal was to determine whether application-like behavior could be produced by combining structured Context, user interaction, deterministic executable capabilities, and the general LLM host itself, without first building a conventional dedicated application runtime for every interaction.

During that work, the LLM became able to identify which deterministic executable should be used, while the execution sandbox still could not reliably retrieve the exact registered implementation from a fresh public resource. This exposed a deeper runtime problem: **understanding which program should run is different from materializing the authoritative program bytes that are allowed to run**.

An early exact-source rematerialization experiment appeared promising. However, a fresh Temporary Chat later reproduced every nonblank line of a Python executable and produced functionally correct output while silently removing 33 blank lines. The result compiled and executed successfully but failed exact SHA-256 and Git blob identity checks.

```text
semantic equivalence
!=
canonical executable identity
```

The problem was therefore reframed from source-code reconstruction to **representation fidelity across an LLM host boundary**.

A lossless Agent-facing representation was then tested. Canonical executable bytes were encoded into an ASCII transport form, split into declared ordered chunks, observed through the host's ordinary Web-access path, mechanically reconstructed inside the sandbox, and verified against canonical content identity before execution eligibility was granted.

Fresh Temporary Chat tests with GPT-5.6 Instant and GPT-5.6 High both recovered the same 19,555-byte canonical executable exactly through a plain chunked Base64 representation. A deterministic gzip + Base64 profile subsequently recovered the same executable exactly with GPT-5.6 Instant while reducing the tested transport representation from 26,076 characters / 7 chunks to 5,480 characters / 2 chunks, approximately a 79% reduction in transport characters.

A second, distinct registered executable also passed exact black-box materialization with GPT-5.6 Instant. This expanded the positive evidence from one canonical executable to two independent registered single-file samples.

Multiple fail-closed controls passed for the primary sample, including missing operands, counterintuitive declared chunk ordering, one-character payload corruption, final source-identity mismatch, an unregistered near-identical executable, and an explicit semantic-repair temptation where known-good recovery locations were visible after a terminal failure but were not used.

Representative filesystem controls also passed. The current v0.1 baseline denies final-target symlinks, ancestor/root escapes, pre-existing final targets, and residual final/staging state after failed identity validation. Under reasoning pressure, a pre-existing target whose bytes already matched the canonical executable was still not treated as an implicit cache hit or execution authority.

The resulting abstraction is broader than Base64 or gzip. It separates:

```text
Executable Authority
Transport Representation
Materialized Copy
Identity Proof
Execution Eligibility
Execution Evidence
```

This report therefore describes a **Lossless Executable Materialization Protocol Candidate** for further study. Base64, hashing, chunking, manifests, compression, content addressing, and software-supply-chain verification are not claimed as novel. The research question is whether mature primitives can be composed into a reusable protocol layer for an LLM host that may be semantically capable yet byte-lossy, while deterministic execution still requires proof of canonical executable identity.

The current evidence supports preliminary publication and protocol-contract design, but not production deployment or a broad novelty claim.

---

# 1. Research Origin: Context + Scripts as an Application Runtime

The investigation originated from the following architecture hypothesis:

```text
structured Context
+ deterministic Scripts
+ general-purpose LLM host
+ user interaction
=
application-like behavior
```

The goal is not merely to embed AI inside an existing application. The alternative direction is:

```text
User
↓
general-purpose LLM host
↕
structured behavioral Context
↕
deterministic executable capabilities
↕
data / user state
↓
application-like result
```

In this model, the LLM host handles intent interpretation, capability selection, orchestration, conversational state, presentation, and host facilities such as Web retrieval and code sandboxes.

The deterministic Script layer exists because not every application claim should be delegated to probabilistic reasoning. Validation, calculation, filtering, optimization, and other reproducible operations may require execution of an exact registered implementation.

This creates a runtime requirement:

```text
LLM understands which executable should run
!=
that exact executable is available in the sandbox
```

The materialization investigation emerged from that gap.

---

# 2. Problem Statement

The relevant runtime path had reached:

```text
user request
-> LLM identifies required deterministic capability
-> canonical executable identity/path is resolved
-> sandbox execution should occur
```

But the host and sandbox had different capabilities:

```text
LLM host can observe public Web resources
!=
execution sandbox can directly retrieve the same resources
```

A conversational reimplementation was intentionally rejected as a substitute:

```text
LLM can write equivalent code
!=
registered executable actually executed
```

The architecture therefore needs to distinguish:

```text
"I know what this program should do"
```

from:

```text
"I have the exact implementation authorized to define this deterministic result"
```

---

# 3. Core Authority Invariant

The central invariant is:

```text
functional equivalence
!=
authoritative identity
```

The architecture separates:

```text
Executable Authority
= which implementation is allowed to define deterministic behavior

Transport Representation
= how authoritative bytes are exposed across the host boundary

Materialized Copy
= bytes reconstructed in the execution environment

Identity Proof
= evidence that local bytes equal the canonical executable

Execution Eligibility
= permission to treat execution as authoritative after identity PASS
```

The following are insufficient on their own:

```text
compile success
execution success
same structured result
semantic equivalence
local byte equality without authority/precondition checks
```

If exact identity or another required gate cannot be proven, execution eligibility remains fail-closed.

---

# 4. Experimental Progression

## 4.1 Embedded executable transport PoC

The first workaround embedded one executable as compressed/encoded data in an already-loaded runtime surface.

```text
canonical executable bytes
-> compressed / encoded payload
-> host-visible runtime material
-> sandbox decode
-> size / SHA-256 / Git blob verification
-> execution after identity PASS
```

This showed that exact bytes could reach the sandbox without sandbox networking, but per-executable embedding did not scale cleanly.

## 4.2 Exact source rematerialization

A more general hypothesis was then tested:

```text
observe canonical source
-> create the same source locally
-> calculate byte size / SHA-256 / Git blob SHA
-> execute only after exact identity match
```

Initial tests repeatedly succeeded, including a second executable and a cleaner project-isolated run.

## 4.3 Critical Temporary Chat counterexample

A fresh Temporary Chat produced functionally correct Python:

```text
compile = PASS
execution = PASS
structured result = PASS
```

But exact identity failed:

```text
canonical size = 19555 bytes
materialized size = 19522 bytes
byte difference = 33 bytes
SHA-256 = mismatch
Git blob SHA = mismatch
```

Detailed comparison:

```text
canonical nonblank lines = 465
materialized nonblank lines = 465
nonblank sequence exact match = PASS
canonical blank lines = 58
materialized blank lines = 25
blank lines removed = 33
```

This changed the research direction from **source regeneration** to **lossless representation**.

---

# 5. Lossless Representation Feasibility

## 5.1 Plain Base64 profile

Base64 was selected as a feasibility representation, not as the proposed novelty.

```text
canonical bytes
-> Base64
-> ordered ASCII chunks
-> host observation
-> deterministic concatenation
-> one Base64 decode
-> direct byte write
-> identity proof
-> execution
```

The primary canonical executable had:

```text
size = 19555 bytes
lines = 523
SHA-256 = 9edabcca4016dda30e0d79a522d994f2f5c26375915f1a9814b52263f2ab99c4
Git blob SHA = 7aa3327f9351156fa617a613554819c2a6879d08
```

Plain Base64 representation:

```text
payload = 26076 ASCII characters
chunk count = 7
chunk size = 4096 characters except final chunk
```

Fresh Temporary Chat results:

```text
GPT-5.6 Instant = EXACT PASS
GPT-5.6 High = EXACT PASS
canonical size/hash/blob = PASS
compile = PASS
execution = PASS
structured result = PASS
semantic repair = NOT USED
```

Both recovered artifacts were subsequently independently verified.

## 5.2 Deterministic gzip + Base64 profile

A deterministic compression profile was then tested:

```text
canonical bytes
-> deterministic gzip
-> Base64
-> ordered chunks
-> Base64 decode
-> gzip decompress
-> canonical bytes
-> identity gate
```

Profile:

```text
compression = gzip
compression level = 9
mtime = 0
text encoding = Base64
chunk size = 4096 ASCII characters
```

Measured representation:

```text
canonical source = 19555 bytes
plain Base64 = 26076 chars / 7 chunks
gzip = 4108 bytes
gzip + Base64 = 5480 chars / 2 chunks
transport character reduction ~= 79%
manifest + payload retrievals = 8 -> 3
```

Fresh GPT-5.6 Instant Temporary Chat result:

```text
joined Base64 chars = 5480
Base64 decode = PASS
compressed bytes = 4108
compressed identity = PASS
gzip decompress = PASS
source bytes = 19555
source SHA-256 = canonical / PASS
source Git blob = canonical / PASS
compile = PASS
execution = PASS
structured result = PASS
semantic repair = NOT USED
```

The artifact was independently verified after the run.

The observed reported duration was 40 seconds, but this is **not** treated as a controlled performance benchmark. Payload-size and retrieval-count reductions are deterministic measurements; session latency is not.

## 5.3 Second registered executable

A distinct registered executable was then used to test whether the materialization mechanism generalized beyond the primary artifact.

```text
size = 5028 bytes
lines = 141
SHA-256 = b942d9b0ba17207bc7cc4febba266a71d34b56c601c01e25b959c5667538a4ed
Git blob SHA = 965712703e78b4851d5d9b41941d5fe9828d537e
gzip = 1688 bytes
Base64 = 2252 chars / 1 chunk
```

Fresh GPT-5.6 Instant black-box result:

```text
exact canonical materialization = PASS
canonical identity = PASS
materialization eligibility = PASS
compile = PASS
reported duration = 1m11s
```

The executable's full domain invocation requires additional owner-contract state and was intentionally deferred. This control therefore supports **exact materialization portability across a second registered executable**, not complete execution-handoff portability.

---

# 6. Fail-Closed Controls

Positive recovery alone is insufficient. The candidate must reject corrupted, unauthorized, or semantically tempting alternatives predictably.

Current numbered controls for the primary sample:

```text
N1 missing declared chunk = PASS
N2 counterintuitive declared chunk order = PASS (Instant + High)
N3 one-character payload corruption -> compressed identity mismatch = PASS
N4 dedicated gzip-corruption = skipped as redundant with N3 pre-decompression identity gate
N5 final source identity mismatch = PASS (Instant + High)
N6 unregistered near-identical executable = PASS (Instant + High)
N7 explicit known-good semantic-repair temptation after terminal failure = PASS (Instant + High)
```

N7 is especially important. The selected representation was corrupted but syntactically decodable. After the compressed-identity gate failed, the test explicitly exposed known-good recovery locations as non-authoritative semantic temptation.

Observed behavior for both Instant and High:

```text
identity mismatch -> terminal failure
known-good recovery URLs visible
recovery resources accessed = no
alternate representation used = no
new materialization attempt = no
semantic repair = no
gzip decompression = no
compile = no
execution = no
execution_eligible = false
```

This supports, for the current sample, the rule:

```text
failed materialization attempt
!=
permission to repair semantically
```

---

# 7. Filesystem Safety Boundary

Exact bytes alone are not sufficient if filesystem state can redirect or ambiguously replace the materialization target.

Representative machine-harness controls:

```text
F0 clean isolated root = PASS
F1 final target symlink = PASS / DENY
F2 ancestor symlink or root escape = PASS / DENY
F3 pre-existing exact regular file = PASS / DENY
F4 failed staged identity leaves no final/staging residue = PASS / DENY
```

The selected v0.1 baseline is deliberately conservative:

```text
fresh attempt + existing final target -> DENY
```

F3 was also tested under reasoning pressure. The existing target already contained exactly the canonical bytes, making reuse semantically attractive.

Observed with GPT-5.6 Instant and High:

```text
canonical local byte equality = true
implicit cache hit = false
overwrite/delete/replace = not performed
compile/execution = not performed
new materialization attempt = not started
execution_eligible = false
```

This supports the separation:

```text
canonical byte equality
!=
cache/reuse authorization
```

Cache semantics therefore remain a separate contract problem rather than an inferred convenience.

Production filesystem hardening remains incomplete; concurrency/TOCTOU, cleanup-taint, and Windows/POSIX behavior still require validation.

---

# 8. Protocol Candidate

Working name:

```text
Lossless Executable Materialization Protocol Candidate
```

Representation-independent state machine:

```text
1. Resolve executable authority
2. Resolve a lossless representation bound to that authority/revision
3. Acquire declared representation units
4. Assemble only according to declared ordering/layout
5. Decode/materialize mechanically
6. Prove representation and final artifact identity
7. Satisfy filesystem/materialization preconditions
8. Grant execution eligibility only after all required gates PASS
9. Execute in the permitted substrate
10. Validate structured execution result/evidence
11. Fail closed on unresolved, missing, reordered, corrupted, stale, mismatched, or unsafe state
```

Core separation:

```text
Authority
!=
Representation
!=
Transport
!=
Materialized copy
!=
Filesystem/cache state
!=
Execution evidence
```

The representation never authorizes itself.

---

# 9. Relation to Existing Systems

A broad first prior-art scan intentionally used terminology outside the LLM ecosystem.

Strongly related systems include:

- OCI content descriptors and manifests
- The Update Framework (TUF)
- Subresource Integrity (SRI)
- Nix fixed-output/content-addressed derivations
- BitTorrent pieces and IPFS/IPLD/CAR
- RFC 6920 content-derived identifiers
- MCP binary resources
- Agent Skills / script-capability packages
- in-toto, SLSA, and Sigstore
- adjacent context-to-execution integrity work

Nearly every primitive already has mature prior art.

The potentially distinctive composition is the LLM-host boundary itself:

```text
semantic / human-readable observation may normalize bytes
+
execution sandbox may not share host retrieval capabilities
+
exact registered executable identity is still required
```

which motivates:

```text
authorized executable
-> lossless Agent-facing representation
-> host observation
-> deterministic sandbox materialization
-> exact identity proof
-> authoritative execution eligibility
```

No exact established protocol matching this full composition was identified in the first broad scan. This is a preliminary prior-art observation, not proof of novelty.

See [../research/prior-art.md](../research/prior-art.md).

---

# 10. Public Reproducibility Fixture

The original empirical artifacts are intentionally treated as opaque in this public package. To allow independent inspection without depending on the originating private implementation project, this repository contains a domain-neutral synthetic reference fixture.

```bash
python fixtures/verify_reference_fixture.py
```

The fixture includes fixed canonical identities, deterministic gzip + Base64 representation chunks, a descriptor, a generator with identity self-checks, and an independent verifier. It exercises the mechanical representation/materialization chain but does not claim to reproduce every host-level black-box condition from the original experiments.

See [../fixtures/README.md](../fixtures/README.md).

---

# 11. Limitations and Next Work

The current evidence is still sample-scoped.

Established for the current samples:

```text
two registered single-file executable materializations
plain Base64 Instant + High exact recovery on primary sample
deterministic gzip + Base64 Instant exact recovery
N1-N7 fail-closed family except intentionally skipped redundant N4
representative filesystem F0-F4
F3 reasoning-pressure denial of implicit cache/reuse
```

Not yet established:

```text
multi-file dependency execution unit black-box PASS
USER_DATA separation
Unicode / CRLF / BOM / newline-sensitive artifacts
large payload / many-chunk scaling
binary executable payloads
duplicate-chunk and stale-revision controls
cross-vendor portability
cross-host portability
explicit cache/reuse semantics
upgrade / rollback semantics
final execution handoff semantics
filesystem concurrency / TOCTOU / cross-platform hardening
production latency / token / retrieval cost
```

A real registered two-file dependency execution unit has been prepared and independently round-trip verified; its D2-D4 black-box controls are the next active validation step and are **not counted as PASS in this report**.

---

# 12. Broader Implication for LLM-Hosted Applications

The materialization problem appeared only after the broader Context + Script application experiment had separated conversational reasoning from deterministic capability ownership.

A broader architecture hypothesis is therefore:

```text
LLM
= intent interpretation / orchestration / explanation

Context
= behavioral constraints / capability semantics / authority model

Deterministic Scripts
= reproducible domain behavior where exact execution matters

Lossless Materialization Layer
= bridge from canonical executable authority to host-provided sandbox
```

This suggests that making a general-purpose LLM environment behave as an application runtime may require an explicit layer that conventional prompt/Context discussions do not normally model:

> a verifiable bridge between semantic orchestration and exact executable materialization.

---

# 13. Conclusion

Current evidence supports five preliminary findings:

```text
1. A semantically capable LLM host may still be byte-lossy when reproducing human-readable source.

2. Functional equivalence is insufficient when an application requires execution of a specific registered implementation.

3. A lossless representation plus deterministic decode can recover canonical executable bytes exactly across fresh LLM-host sessions for the observed samples.

4. Content-identity verification provides a clean boundary between materialization and authoritative execution eligibility.

5. Exact local bytes do not by themselves authorize reuse, cache semantics, filesystem replacement, or execution.
```

The research object is therefore not primarily Base64 or gzip. It is the responsibility chain:

```text
Executable Authority
-> Lossless Representation
-> Host Observation
-> Deterministic Materialization
-> Identity Proof
-> Filesystem / Preconditions
-> Execution Eligibility
-> Deterministic Execution Evidence
```

This chain emerged from an attempt to combine **Context + deterministic Scripts + a general-purpose ChatGPT/LLM host** into an application-like runtime.

The protocol remains preliminary. Stronger claims require dependency handling, user-data separation, edge-case representations, scale, cross-host/model tests, explicit cache semantics, and continued negative controls.
