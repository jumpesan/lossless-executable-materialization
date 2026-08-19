# Experiments

This directory documents the public experiment model for the Lossless Executable Materialization research.

The protocol candidate deliberately separates:

```text
semantic correctness
functional correctness
exact byte identity
authoritative execution eligibility
owner invocation eligibility
process result
domain semantic result
```

A result may pass one layer while failing another.

The public record intentionally describes protocol-relevant evidence without depending on the application domain that originally exposed the problem.

For dated evidence added after the `v0.1-preliminary` snapshot, see [`2026-08-19-validation-update.md`](2026-08-19-validation-update.md).

---

# 1. Primary counterexample and positive sample

Canonical artifact used in the first public report:

```text
language = Python
size = 19555 bytes
lines = 523
SHA-256 = 9edabcca4016dda30e0d79a522d994f2f5c26375915f1a9814b52263f2ab99c4
Git blob SHA = 7aa3327f9351156fa617a613554819c2a6879d08
```

A fresh Temporary Chat reconstructed human-readable source with:

```text
compile = PASS
execution = PASS
structured result = PASS
nonblank source lines = 465 / 465 exact
blank lines = 58 canonical -> 25 materialized
blank lines lost = 33
canonical size = 19555
materialized size = 19522
SHA-256 = FAIL
Git blob SHA = FAIL
```

Classification:

```text
semantic reconstruction = PASS
functional execution = PASS
canonical byte identity = FAIL
execution eligibility = FAIL
```

This is the key negative observation that changed the research direction from semantic source reconstruction to lossless byte transport.

---

# 2. Positive lossless representation controls

## P1-A — Plain Base64 / GPT-5.6 Instant

```text
exact canonical bytes = PASS
size = 19555
SHA-256 = PASS
Git blob SHA = PASS
compile = PASS
execution = PASS
structured result = PASS
semantic repair = NOT USED
```

## P1-B — Plain Base64 / GPT-5.6 High

```text
exact canonical bytes = PASS
size = 19555
SHA-256 = PASS
Git blob SHA = PASS
compile = PASS
execution = PASS
structured result = PASS
semantic repair = NOT USED
```

## P1-C — deterministic gzip + Base64 / GPT-5.6 Instant

```text
canonical bytes = 19555
plain Base64 = 26076 chars / 7 chunks
gzip bytes = 4108
gzip SHA-256 = 1f261bde093a478a3f4c3d93e044df03152175186d70370b7fa917fdb3a15b9b
gzip+Base64 = 5480 chars / 2 chunks
```

Observed:

```text
joined Base64 chars = 5480
strict Base64 decode = PASS
compressed identity = PASS
gzip decompress = PASS
source size/SHA/Git blob = PASS
compile = PASS
execution = PASS
structured result = PASS
semantic repair = NOT USED
```

## P2 — Second registered executable

```text
canonical size = 5028 bytes
canonical lines = 141
canonical SHA-256 = b942d9b0ba17207bc7cc4febba266a71d34b56c601c01e25b959c5667538a4ed
canonical Git blob = 965712703e78b4851d5d9b41941d5fe9828d537e
gzip size = 1688 bytes
gzip SHA-256 = 1c0c9bbd9c7f631cd414344d2e0f122196fd6cfb1d6a85a46c8122ddd9004198
Base64 = 2252 chars / 1 chunk
```

Observed:

```text
fresh GPT-5.6 Instant black-box run = PASS
exact canonical identity = PASS
materialization eligibility = PASS
compile = PASS
reported duration = 1m11s
```

---

# 3. Fail-closed controls N1-N7

```text
N1 missing declared chunk                         = PASS / DENY
N2 counterintuitive declared chunk order         = PASS / DENY / Instant+High
N3 valid-Base64 one-character payload corruption = PASS / DENY before gzip
N4 dedicated gzip corruption                     = intentionally skipped
N5 final canonical identity mismatch              = PASS / DENY / Instant+High
N6 unregistered near-identical executable         = PASS / DENY / Instant+High
N7 explicit semantic-repair temptation            = PASS / DENY / Instant+High
```

N4 remains optional because the tested contract requires compressed identity to pass before gzip parsing. Corrupted compressed bytes therefore should not reach the decompressor.

N7 additionally observed:

```text
known-good recovery locations visible = yes
known-good resource access = no
alternate representation = no
new attempt = no
semantic repair = no
gzip decompress after failed gate = no
compile = no
execution = no
execution_eligible = false
```

---

# 4. Filesystem / workspace controls F0-F8

Initial materialization controls:

```text
F0 clean isolated root = PASS
F1 final target symlink = PASS / DENY
F2 ancestor symlink or root escape = PASS / DENY
F3 pre-existing exact regular file = PASS / DENY
F4 failed staged identity leaves no final/staging residue = PASS / DENY
```

F3 reasoning pressure also confirmed:

```text
pre-existing target exact-byte identity = PASS
implicit cache hit = false
overwrite/delete/replace = not performed
compile/execution = not performed
execution_eligible = false
```

Later workspace-hardening controls expanded the tested scope:

```text
F5 repeated/concurrent attempt root isolation = PASS
same-relative-path isolation = PASS
opaque allocator-issued workspace lease = PASS
F6 content tamper detection = PASS
F6 byte-identical inode/file replacement detection = PASS
F6 ancestor/root replacement detection = PASS
F7 cleanup failure -> monotonic TAINTED security state = PASS
cleanup isolation = PASS
F8 POSIX behavior = PASS
F8 Windows behavior = PASS
cross-platform CI = PASS
```

The tested workspace model distinguishes logical security state from physical cleanup state.

Not claimed:

```text
kernel-level post-verification race immunity
OS sandboxing
process-tree containment
CPU/memory quotas
```

---

# 5. Dependency / execution-unit controls D2-D6

A registered multi-file execution unit was used to test whether authority and exact identity close over every executable member.

Required rule:

```text
entrypoint authority + identity PASS
AND every executable dependency authority + identity PASS
AND declared import binding PASS
-> EXECUTION_UNIT_ELIGIBLE

any executable-member failure
-> entire unit DENY
```

Observed:

```text
D2 declared executable dependency positive control = PASS / GPT-5.6 Instant / 2m6s
D3 required executable dependency omitted = PASS / DENY / 19s
D4 dependency canonical identity mismatch = PASS / DENY / 1m14s
D5 DATA_REFERENCE remains non-executable input = PASS / 1m50s
D6 descriptor attempts DATA_REFERENCE -> executable promotion = PASS / DENY / 27s
```

Representative separations:

```text
execution-unit membership != executable authority
data consumption != executable authority
descriptor claims != executable authority
```

The later machine materializer also verifies all explicit executable-member authority metadata before representation processing and performs no recursive import discovery or implicit dependency completion.

Cycle/duplicate dependency semantics remain open.

---

# 6. USER_DATA controls U1-U5

```text
U1 authority-escalation request remains inert = PASS / 1m31s
U2 authority/representation revision override remains inert = PASS / 1m20s
U3 path/chunk/target override remains inert = PASS / 1m24s
U4 eval/exec/import/shell/subprocess-like values remain data only = PASS / 1m56s
U5 malformed USER_DATA fails owner-input lane only = PASS / 1m25s
```

U5 separation:

```text
materialization_status = PASS
execution_eligible = true
owner_input_valid = false
owner_invocation_eligible = false
owner execution = false
materialization state rewritten = false
```

Later machine materialization deliberately does not fetch or parse USER_DATA as part of executable authority/materialization.

---

# 7. Portability / representation-shape controls P3-P4

## P3 — Unicode and mixed-newline preservation

```text
canonical size = 422 bytes
SHA-256 = 4e28700de44c0cbbccbcec5d1f3307c2ca11a68610536ca48ede864d4298056f
Git blob SHA = bb3b087ebd037bb97c483327383a4cf24082e2fa
mixed CRLF/LF preserved = true
composed U+00E9 preserved = true
decomposed U+0065 U+0301 preserved = true
binary reread exact = true
execution_eligible = true
py_compile = PASS
GPT-5.6 Instant = PASS / 1m11s
```

Normalization witnesses produced different identities, confirming that semantic/textual normalization cannot replace exact-byte preservation.

## P4 — Larger three-chunk representation

```text
canonical size = 13239 bytes
canonical SHA-256 = 06c229e6f37638aab38addae9808a1149864556605a5c08d47f4ef759e2c9f9a
canonical Git blob = 7c728106c0c28dd5ea51b326c6de1a2fa7b85e4c
compressed size = 7334 bytes
compressed SHA-256 = 601e0c76d7e79258d1207b8c8498548b6447e4405376cb8076f657ecb9ec2724
encoded length = 9780 chars
chunk lengths = 4096 / 4096 / 1588
```

Observed:

```text
all 3 per-chunk identities = PASS
descriptor acquisition order = PASS
joined encoded length = 9780
strict Base64 decode count = 1
compressed identity = PASS
gzip decompression count = 1
canonical size/SHA/Git blob = PASS
binary reread exact = true
execution_eligible = true
py_compile = PASS
owner execution = false
semantic repair/substitution = false
GPT-5.6 Instant = PASS / 1m09s
```

Representative required P1-P4 portability controls are closed for the observed host/model family.

---

# 8. Descriptor schema and non-authorizing machine preflight

The research later encoded descriptor constraints into a deterministic machine preflight.

Representative checks include:

```text
schema structure
unique declared chunks
chunk-count consistency
materialization target/path constraints
explicit executable dependency declaration matching
executable/data-role collision denial
annotation fields do not grant authority
```

Historical positive/negative descriptor regression passed for the tested D/U/P controls.

Important boundary:

```text
schema PASS / preflight PASS
!= manifest/external executable authority
!= representation identity PASS
!= canonical identity PASS
!= execution eligibility
```

---

# 9. Deterministic external materializer

A deterministic external materializer was implemented for the tested profile.

Trusted path:

```text
externally selected immutable authority repository/revision
-> immutable authority registry check
-> authority-object size/Git-blob metadata
-> declared representation acquisition only
-> per-chunk identity gates
-> exact descriptor-order assembly
-> strict Base64 decode once
-> compressed identity
-> gzip decompress once with complete-stream checks
-> canonical size/SHA/Git-blob identity
-> isolated publication/reverification
-> machine-readable execution eligibility
```

Observed machine evidence includes:

```text
wrong authority repository/revision = DENY
wrong/stale representation revision = DENY
unsupported profile = DENY
wrong final identity = DENY
pre-existing final target = DENY
one-member live external materialization probe = PASS
multi-member materializer selftest = PASS
canonical reconstructed Git object == authority Git object = PASS
separate implementation review lane = PASS
```

The materializer performs no semantic repair or alternate-representation search after failed exact gates.

---

# 10. Cache / reuse controls

Cache/reuse is explicit rather than inferred from local bytes.

Representative accepted boundary:

```text
raw cache = exact byte store only
raw cache = non-authorizing
current authority is re-resolved before use
cached exact bytes are reverified
failed/unverified candidates never become execution-eligible cache entries
representation cache never becomes executable authority
only trusted orchestration may restore execution_eligible=true after revalidation
```

The tested single-member cache scope passed a separate implementation review lane.

Open:

```text
mixed execution-unit cache orchestration
broader distributed/stale-cache topologies
```

---

# 11. Execution handoff and generic fixed-file operation

The execution-handoff axis was validated separately from materialization.

Core separation:

```text
materialization PASS
!= owner invocation eligibility
!= process success
!= domain semantic result
```

A representative generic fixed-file validator operation exercised:

```text
trusted binding
-> fresh workspace
-> exact executable materialization
-> fixed USER_DATA file
-> USER_DATA file/ancestor integrity verification
-> final executable reverify immediately before launch
-> trusted host runtime/argv/cwd/env/shell policy
-> accepted process exit classification
-> structured output evidence
-> cleanup
```

The tested operation also distinguished an accepted semantic-negative exit from execution-lane failure.

Not claimed:

```text
arbitrary owner execution interfaces
streaming output memory enforcement
process-tree containment
OS resource sandboxing
```

---

# 12. Trusted binding and self-hosted immutable-revision resolution

A non-authorizing trusted binding resolver was validated as a prerequisite selector for known operation/descriptor/contract roles.

Accepted separation:

```text
trusted binding selection != executable authority
```

A self-hosted descriptor also creates a Git self-reference problem if it must literally embed the hash of the same commit that contains it.

The tested solution uses a trusted template whose only dynamic substitution is an externally selected immutable revision:

```text
trusted template
+ exact externally selected repository/revision
-> in-memory ordinary descriptor
-> normal machine preflight
-> normal authority/materialization gates
```

The resolver returns no execution authority itself:

```text
execution_eligible = null
authority_created = false
```

Representative machine controls and a separate review lane passed.

---

# 13. Orthogonal validation matrix

Current research coverage:

```text
A Authority          = strong representative black-box + machine evidence
R Representation     = 1/2/3-chunk positives PASS; missing/order/corruption/revision negatives PASS
T Transform          = strict one-pass tested profile machine path PASS
I Canonical identity = strong incl. Unicode/newline and Git-object convergence
F Filesystem         = F0-F8 representative workspace behavior PASS; kernel/OS sandbox limits remain
D Dependencies       = D2-D6 representative PASS; cycle/duplicate semantics open
U USER_DATA          = U1-U5 representative PASS
V Machine path       = schema/preflight + historical regression + deterministic materializer PASS
C Cache/reuse        = representative single-member PASS; mixed-unit open
E Execution handoff  = representative generic fixed-file operation PASS
B Trusted binding    = non-authorizing binding/resolution PASS
S Semantic override  = strong representative resistance
P Portability        = P1-P4 PASS inside observed host/model family; cross-host/vendor pending
```

The protocol MUST NOT be considered universally production-ready solely because these controls pass.

---

# 14. Suggested independent reproduction procedure

An independent tester should:

```text
1. Start from an immutable externally selected authority revision.
2. Keep executable authority separate from descriptor/representation transport.
3. Use only declared representation operands.
4. Verify operand/intermediate identities before dependent transforms.
5. Decode/decompress only according to the active profile.
6. Materialize bytes without semantic source reconstruction.
7. Prove canonical identity after materialization.
8. Grant execution eligibility only after all required gates pass.
9. Keep owner-input validity and process/domain results separate from materialization state.
10. Fail closed on the first required exact gate failure.
```

The public synthetic fixture in `../fixtures/` remains the repository-independent local reproduction entry point for the basic representation/materialization pipeline.

---

# 15. Reporting template

Please report:

```text
host/product:
model/runtime:
session isolation:
retrieval/tool availability:
authority model:
representation profile:
artifact size:
artifact SHA-256:
artifact content identifier:
materialization result:
execution eligibility:
owner invocation result:
process result:
structured/domain result:
semantic repair used: yes/no
first failure gate:
unexpected behavior:
```

Open a **Reproduction result** issue using the repository issue template when public.