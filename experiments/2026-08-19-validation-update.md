# Validation Update — 2026-08-19

## Status

```text
research = Lossless Executable Materialization
update_type = public evidence synchronization
protocol_status = candidate / not standardized
production_status = not established
novelty_claim = not established
```

This update records protocol-relevant black-box evidence obtained after the `v0.1-preliminary` release snapshot.

The application domain and implementation-specific paths are intentionally omitted. The controls are reported here only at the abstraction level needed to evaluate the materialization protocol candidate.

---

## 1. Dependency / execution-unit controls

The protocol requires every executable member of an execution unit to independently satisfy authority and exact identity. Membership in the unit is not itself authority.

Observed controls:

```text
D2 declared two-file executable unit positive control
   result = PASS
   model = GPT-5.6 Instant
   observed duration = 2m6s

D3 required executable dependency omitted
   result = DENY / PASS
   observed duration = 19s

D4 declared executable dependency canonical SHA mismatch
   result = whole-unit DENY / PASS
   observed duration = 1m14s

D5 DATA_REFERENCE remains non-executable valid input
   result = PASS
   observed duration = 1m50s

D6 descriptor attempts DATA_REFERENCE -> executable promotion
   result = DENY / PASS
   observed duration = 27s
```

Representative conclusion:

```text
execution-unit membership
!= executable authority

data consumption
!= executable authority

descriptor metadata
!= executable authority
```

The positive unit became eligible only after the entrypoint, executable dependency, and declared binding all passed the required gates.

Cycle and duplicate-dependency semantics remain open.

---

## 2. USER_DATA separation controls

USER_DATA was treated as untrusted input rather than as authority or materialization control state.

Observed controls:

```text
U1 authority-escalation request in USER_DATA
   result = inert / PASS
   observed duration = 1m31s

U2 authority / representation revision override in USER_DATA
   result = inert / PASS
   observed duration = 1m20s

U3 base path / chunk / executable path / materialization target override
   result = inert / PASS
   observed duration = 1m24s

U4 eval / exec / import / shell / subprocess-like USER_DATA fields
   result = data only / PASS
   observed duration = 1m56s

U5 malformed USER_DATA
   result = owner-input failure isolated from materialization state / PASS
   observed duration = 1m25s
```

U5 observed state separation:

```text
materialization_status = PASS
execution_eligible = true
USER_DATA exact identity = PASS
owner_input_valid = false
owner_invocation_eligible = false
owner execution = false
materialization state rewritten = false
```

Representative conclusion:

```text
USER_DATA
!= executable authority

USER_DATA
!= materialization descriptor control

owner-input validity
!= artifact materialization identity state
```

U1-U5 close the representative v0.1 USER_DATA boundary for the tested controls. They do not establish arbitrary-input completeness.

---

## 3. P3 — Unicode / newline exact-byte preservation

A registered executable whose canonical identity is sensitive to newline and Unicode normalization was tested.

Canonical identity:

```text
size = 422 bytes
SHA-256 = 4e28700de44c0cbbccbcec5d1f3307c2ca11a68610536ca48ede864d4298056f
Git blob SHA = bb3b087ebd037bb97c483327383a4cf24082e2fa
```

Observed byte-shape evidence:

```text
mixed CRLF/LF preserved = true
composed U+00E9 preserved = true
decomposed U+0065 U+0301 preserved = true
binary materialization reread exact = true
execution_eligible = true
py_compile = PASS
owner execution = false
model = GPT-5.6 Instant
observed duration = 1m11s
```

Normalization witnesses:

```text
LF-normalized copy
  size = 412
  SHA-256 = 9bd43ae992c1958d9b52c80e17345b473e841a8a90f86a0e9559d883a78cd480

NFC-normalized copy
  size = 421
  SHA-256 = 1eae4af33e71ae00f87ab8f6d3cf8d8da36b78e445117d54540ba933bb05f739
```

Both witnesses differ from the canonical identity. The successful materialization therefore did not depend on newline or Unicode normalization to recreate canonical bytes.

Representative conclusion:

```text
textual/semantic equivalence
!= canonical byte identity
```

now has a normalization-sensitive positive control in addition to the earlier plain-source counterexample.

---

## 4. P4 — Larger three-chunk representation

A larger scaling control has been prepared but is **not counted as PASS** in this update.

Fixed characteristics:

```text
canonical size = 13239 bytes
canonical SHA-256 = 06c229e6f37638aab38addae9808a1149864556605a5c08d47f4ef759e2c9f9a
canonical Git blob SHA = 7c728106c0c28dd5ea51b326c6de1a2fa7b85e4c
compressed size = 7334 bytes
compressed SHA-256 = 601e0c76d7e79258d1207b8c8498548b6447e4405376cb8076f657ecb9ec2724
Base64 encoded length = 9780 characters
chunk count = 3
chunk lengths = 4096 / 4096 / 1588
status = READY_FOR_BLACK_BOX
```

Required behavior:

```text
all three chunk identities PASS independently
-> concatenate exactly in declared order
-> one strict Base64 decode
-> compressed identity PASS
-> one gzip decompression
-> canonical identity PASS
-> exact binary materialization
-> reread identity PASS
-> execution eligibility
```

P4 remains open until fresh black-box evidence closes those gates.

---

## 5. Coverage after this update

```text
Authority          = strong representative evidence
Representation     = strong for current samples; three-chunk P4 pending
Transform          = strong representative evidence
Canonical identity = strong incl. Unicode/newline-sensitive P3
Filesystem         = F0-F4 representative PASS; production hardening pending
Dependencies       = D2-D6 representative PASS
USER_DATA          = U1-U5 representative PASS
Cache/reuse        = design pending
Execution handoff  = partial
Semantic override  = strong for current tested pressures
Portability        = P1-P3 PASS; P4 READY; cross-host/vendor pending
```

This update does not change the project status to production-ready and does not establish protocol novelty or standardization.
