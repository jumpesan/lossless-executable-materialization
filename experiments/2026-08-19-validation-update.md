# Validation Update — 2026-08-19

## Status

```text
research = Lossless Executable Materialization
update_type = public evidence synchronization
protocol_status = candidate / not standardized
production_status = full runtime integration not established
novelty_claim = not established
```

This update records protocol-relevant evidence obtained after the `v0.1-preliminary` release snapshot.

The application domain and implementation-specific paths are intentionally omitted. The controls are reported only at the abstraction level needed to evaluate the materialization protocol candidate.

The `v0.1-preliminary` tag remains a fixed historical release snapshot. This file describes later evidence on `main`.

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

D4 declared executable dependency canonical identity mismatch
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
execution-unit membership != executable authority
data consumption != executable authority
descriptor metadata != executable authority
```

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
owner_input_valid = false
owner_invocation_eligible = false
owner execution = false
materialization state rewritten = false
```

Representative conclusion:

```text
USER_DATA != executable authority
USER_DATA != materialization descriptor control
owner-input validity != artifact materialization identity state
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

Observed:

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

Normalization witnesses produced different identities:

```text
LF-normalized copy
  size = 412
  SHA-256 = 9bd43ae992c1958d9b52c80e17345b473e841a8a90f86a0e9559d883a78cd480

NFC-normalized copy
  size = 421
  SHA-256 = 1eae4af33e71ae00f87ab8f6d3cf8d8da36b78e445117d54540ba933bb05f739
```

This strengthens the invariant:

```text
textual / semantic equivalence != canonical byte identity
```

---

## 4. P4 — Larger three-chunk representation — PASS

The larger scaling control is now closed.

Canonical / representation characteristics:

```text
canonical size = 13239 bytes
canonical SHA-256 = 06c229e6f37638aab38addae9808a1149864556605a5c08d47f4ef759e2c9f9a
canonical Git blob SHA = 7c728106c0c28dd5ea51b326c6de1a2fa7b85e4c
compressed size = 7334 bytes
compressed SHA-256 = 601e0c76d7e79258d1207b8c8498548b6447e4405376cb8076f657ecb9ec2724
Base64 encoded length = 9780 characters
chunk count = 3
chunk lengths = 4096 / 4096 / 1588
```

Observed:

```text
all three chunk identities = PASS
actual acquisition order = descriptor order
joined encoded length = 9780
strict Base64 decode count = 1
compressed identity = PASS
gzip decompression count = 1
canonical size/SHA/Git blob = PASS
binary materialization reread exact = true
execution_eligible = true
py_compile = PASS
owner execution = false
semantic repair/substitution = false
model = GPT-5.6 Instant
observed duration = 1m09s
```

Representative required portability controls P1-P4 are therefore closed for the tested host/model family.

---

## 5. Descriptor schema and deterministic machine path

The research moved from LLM-observed controls into a machine-enforced path.

The tested machine path now includes:

```text
descriptor schema / structural validation
-> deterministic non-authorizing preflight
-> historical positive/negative descriptor regression
-> external immutable authority binding
-> declared representation acquisition
-> exact chunk/intermediate identity gates
-> one-pass decode/decompression
-> canonical exact-byte identity proof
-> isolated filesystem publication
-> machine-readable execution eligibility
```

Observed evidence:

```text
historical D/U/P descriptor regression = PASS
wrong authority repository/revision binding = DENY / PASS
wrong/stale representation revision = DENY / PASS
unsupported representation profile = DENY / PASS
canonical Git object convergence = PASS
one-member live external materialization probe = PASS
multi-member materializer selftest = PASS
separate implementation review lane = PASS
```

Important separation:

```text
schema PASS / preflight PASS
!= executable authority
!= canonical identity PASS
!= execution eligibility
```

The deterministic materializer, rather than semantic LLM reconstruction, now owns the trusted transport/materialization path in the tested implementation.

---

## 6. Cache / reuse semantics — representative PASS

Cache/reuse was added as an explicit contract rather than inferred from local byte equality.

Accepted representative boundary:

```text
raw cache = exact byte store only
raw cache = non-authorizing
current authority must be re-resolved
cached exact bytes must be reverified
only the trusted orchestrator may restore execution_eligible=true
representation cache never becomes executable authority
failed/unverified candidate never becomes an eligible cache entry
```

This closes the tested single-member cache/reuse scope.

Not established:

```text
mixed execution-unit cache orchestration
all stale/distributed cache topologies
```

---

## 7. Execution handoff — representative PASS

The execution-handoff boundary was separately validated after materialization.

Representative separation:

```text
materialization PASS
!= owner invocation eligibility
!= process success
!= domain semantic success
```

The reviewed generic fixed-file operation demonstrated a path in which:

```text
trusted runtime binding
-> fresh isolated workspace
-> exact validator materialization
-> fixed USER_DATA file
-> executable and input integrity reverification
-> trusted host runtime/argv/cwd/env/shell policy
-> process execution
-> structured output / exit classification
-> cleanup evidence
```

Process/integrity failures remain integration failures rather than being rewritten into domain-semantic negatives.

This is representative downstream integration evidence, not a claim that arbitrary owner execution interfaces are standardized.

---

## 8. F5-F8 workspace hardening — representative PASS

The filesystem/workspace axis now extends beyond F0-F4.

Observed machine controls include:

```text
repeated/concurrent attempt root isolation = PASS
same-relative-path isolation across attempts = PASS
opaque allocator-issued workspace lease = PASS
content tamper detection = PASS
byte-identical file replacement detection = PASS
ancestor replacement / root replacement detection = PASS
cleanup isolation = PASS
cleanup failure -> monotonic TAINTED state = PASS
POSIX behavior = PASS
Windows behavior = PASS
cross-platform CI = PASS
```

The implementation distinguishes logical security state from physical cleanup state.

Not claimed:

```text
kernel-level post-verification race immunity
OS sandboxing
process-tree containment
CPU/memory resource isolation
```

---

## 9. Trusted binding and self-hosted revision resolution

A non-authorizing trusted binding layer was validated so that runtime operations select only registered descriptor/contract roles before materialization.

A separate self-hosted descriptor issue was also encountered: a descriptor stored in the same immutable Git revision it describes cannot literally contain that revision's own future commit hash without a self-reference problem.

The tested resolution uses a trusted template whose only dynamic substitution is the externally selected immutable revision:

```text
trusted runtime template
+ externally selected immutable repository/revision
-> in-memory ordinary v0.1 descriptor
-> normal preflight
-> normal authority/materialization gates
```

The resolver itself remains non-authorizing:

```text
execution_eligible = null
authority_created = false
```

Machine controls and a separate review lane passed for the tested resolver.

---

## 10. Coverage after this update

```text
Authority          = strong representative machine + black-box evidence
Representation     = 1/2/3-chunk positive shapes PASS; corruption/order/revision negatives PASS
Transform          = strict one-pass Base64/gzip path machine-enforced for tested profile
Canonical identity = strong incl. Unicode/newline and authority Git-object convergence
Filesystem         = F0-F8 representative workspace behavior PASS; kernel/OS sandbox limits remain
Dependencies       = D2-D6 representative PASS; cycle/duplicate semantics open
USER_DATA          = U1-U5 representative PASS
Descriptor/preflight = schema + historical regression PASS
External materializer = implementation/selftest/live evidence + separate review PASS
Cache/reuse        = representative single-member contract PASS; mixed-unit cache open
Execution handoff  = representative generic fixed-file operation PASS
Trusted binding    = non-authorizing resolver PASS
Self-hosted revision binding = resolver PASS
Semantic override  = strong representative resistance
Portability        = P1-P4 PASS inside observed host/model family; cross-host/vendor pending
```

The remaining major research/integration gaps are now narrower:

```text
cross-host / cross-vendor reproduction
dependency cycle/duplicate edge semantics
mixed-unit cache semantics
remaining transport-normalization/boundary cases
full trusted-host end-to-end integration
live/runtime promotion policy
broader OS/process sandbox and resource isolation
specification stabilization
```

This update does not change the project into an established standard or prove novelty. It also does not claim that full production runtime integration has been completed.