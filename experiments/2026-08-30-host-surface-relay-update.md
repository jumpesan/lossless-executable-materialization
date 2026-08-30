# Host-Surface Relay Update — 2026-08-30

## Status

```text
research = Lossless Executable Materialization
update_type = public host-integration evidence synchronization
protocol_status = candidate / not standardized
production_status = generic trusted-host integration not established
novelty_claim = not established
claim_scope = observed host/model surface only
```

This update records a new boundary discovered while integrating exact executable materialization into a general-purpose LLM host.

The originating application domain, private repository paths, user data, and application-specific state names are intentionally omitted. The executable/capsule samples are treated as opaque application-derived artifacts. Only protocol-relevant transport identities and black-box observations are reported.

The `v0.1-preliminary` tag remains a fixed historical snapshot.

---

## 1. New boundary: host observation is not execution-surface availability

Earlier work established that semantic reconstruction can preserve behavior while losing canonical byte identity.

Trusted-host integration exposed a separate problem:

```text
resource observable by the host
!=
exact operand available in caller/model context
!=
exact bytes available in the execution surface
```

A host may successfully observe a transport resource through one surface while its code-execution sandbox cannot independently retrieve or receive the same exact bytes.

This is a transport/materialization boundary, not executable authority.

---

## 2. H1 — External resource visible, sandbox-local handoff blocked

A direct immutable transport descriptor was resolved successfully through the host retrieval surface.

Observed:

```text
descriptor resolution = PASS
external transport resource observation = PASS
canonical executable identity recognition = PASS
owner-input identity observation = PASS
semantic reimplementation = NOT USED
canonical execution = NOT COMPLETED
```

The remaining blocker was:

```text
host-visible transport payload
-> sandbox-local exact bytes
```

The host could read the external transport and could separately execute Python, but the current surface did not provide a reliable exact-data bridge between those capabilities.

Classification:

```text
H1_EXTERNAL_RESOURCE_TO_EXECUTION_SURFACE_HANDOFF = BLOCKED / OBSERVED
```

This result narrowed the problem away from executable selection or canonical-identity ambiguity.

---

## 3. H2 — Local attachment plane exact canonical execution PASS

The same opaque execution capsule was then made directly available on the local attachment plane rather than requiring Web-to-sandbox transfer.

Fresh isolated sessions established:

```text
GPT-5.6 Instant = canonical execution PASS
GPT-5.6 High    = canonical execution PASS
repository/network fetch during execution = not required
```

The execution path verified the transport representation, reconstructed the canonical executable, verified exact identity, invoked it, and accepted the structured result.

A representative semantic-negative owner input was also exercised through the same exact capsule:

```text
canonical materialization = PASS
canonical invocation = PASS
accepted process exit = true
structured negative result = PASS
success state was not conversationally upgraded
```

Representative conclusion:

```text
execution transport availability
!= reasoning level
```

for this bounded gate.

The attachment plane is experimental evidence only. Requiring an ordinary user to manage execution infrastructure is not treated as the desired final product path.

---

## 4. H3 — Large monolithic caller-context relay FAIL

The next candidate attempted to remove manual capsule attachment.

An immutable staging object contained the exact execution capsule as one large encoded scalar.

Representative shape:

```text
one-line staging object ~= 13.2 KB
exact encoded capsule scalar = 10944 characters
decoded capsule target = 8207 bytes
```

The intended route was:

```text
host/caller-side immutable resource resolution
-> exact scalar available in caller context
-> literal transfer into sandbox
-> local exact capsule reconstruction
```

Observed instead:

```text
staging object recognized = partial
full exact scalar caller-context availability = not established
sandbox network/refetch attempt = observed
sandbox network resolution = failed
exact local capsule staging = not reached
canonical execution = not reached
```

The consumer then began semantically inspecting owner input before canonical validation, which was outside the bounded contract.

Classification:

```text
large monolithic caller-context relay = FAIL
execution-surface refetch fallback = route drift
semantic reimplementation pressure = observed
```

The exact large-object representation was rejected for this host surface rather than retried unchanged.

---

## 5. H4 — Small chunked caller-context literal relay PASS

The next probe changed only the relay granularity.

The same exact encoded capsule was split into small exact chunks:

```text
chunk count = 8
each chunk.data length = 1368 characters
combined encoded length = 10944 characters
decoded capsule size = 8207 bytes
decoded capsule SHA-256 =
ecbe9641f9569c10d00b380de9f7bb1d28b0cbc564dabaa0dc499347f70e1e7f

canonical executable size = 20541 bytes
canonical executable SHA-256 =
0a363c3f88c9b5585567a846384984bbbd81bf2cf314f8e21a08d89c05cd2331
```

Required route:

```text
resolve small exact chunks on caller/host side
-> pass exact chunk scalar values as literal sandbox inputs
-> no sandbox URL/network/repository refetch
-> deterministic ordered concatenation
-> exact transported-object identity proof
-> canonical executable identity proof
-> canonical execution
```

Final bounded classification:

```text
caller-side small-chunk resolution = PASS
caller-context -> sandbox literal relay primitive = PASS
sandbox network/refetch avoidance = PASS
exact capsule reconstruction = PASS
capsule identity verification = PASS
canonical executable identity verification = PASS
canonical execution = PASS
structured result = PASS
```

### Evidence reconciliation note

The first successful execution visibly established the intended literal sandbox route and canonical execution, but one displayed chunk-length value contradicted the later exact total.

A second run against the same immutable candidate reconciled the deterministic identities:

```text
chunk lengths = 1368 x 8
combined length = 10944
decoded size = 8207
decoded SHA-256 = exact
canonical executable identity = exact
canonical result = PASS
```

The host Activity UI exposed only the early portion of the second run rather than one complete end-to-end trace.

The final H4 verdict therefore uses convergent evidence across two runs against the same immutable candidate:

```text
Run A = visible literal relay + canonical execution evidence
Run B = exact transport-identity reconciliation
H4 = bounded composite PASS
```

This is disclosed explicitly because it is weaker evidence than one complete independently inspectable single-run trace.

---

## 6. Controlled comparison

| Condition | Host resource observation | Exact transfer to execution surface | Canonical execution | Classification |
|---|---:|---:|---:|---|
| Direct external transport | PASS | BLOCKED | NOT REACHED | H1 negative observation |
| Local attachment plane | local | PASS | PASS | H2 positive |
| One large caller-context staging object | partial | FAIL | NOT REACHED | H3 negative |
| Eight small caller-context literals | PASS | PASS | PASS | H4 bounded composite positive |

The controlled contrast supports a new host-boundary interpretation:

```text
lossless representation exists
!=
host exposes the representation at the required surface
!=
host can relay that exact representation into the execution substrate
```

---

## 7. Inference: execution-surface transfer is a protocol boundary

Current evidence supports adding an optional protocol stage when host retrieval and execution surfaces differ:

```text
Executable Authority
-> Lossless Representation
-> Representation Acquisition
-> Execution-Surface Transfer
-> Representation Identity Gates
-> Mechanical Materialization
-> Exact Identity Proof
-> Execution Eligibility
```

This stage is non-authorizing.

```text
successful relay != executable authority
transport chunk != executable authority
local attachment != executable authority
```

Authority still comes from the external trusted registration and exact final identity gates.

---

## 8. Transport granularity is a host-surface parameter

The H3/H4 comparison suggests that relay granularity can materially affect whether exact data is available across an LLM-host internal boundary.

Current evidence supports only:

```text
large monolithic sample on observed surface = FAIL
small eight-chunk sample on observed surface = PASS
```

It does **not** establish:

```text
a universal maximum safe scalar length
a universal optimum chunk size
a model-independent threshold
a cross-host/vendor transport rule
```

Chunk size/count should therefore be modeled as a transport-profile parameter rather than domain/application semantics.

---

## 9. Generic transport is still open

The current H4 PASS proves a bounded relay primitive for one opaque execution capsule shape.

It does not prove a generic application-wide execution transport.

Before stronger promotion, high-value requirements include:

```text
unit-agnostic descriptor/transport binding
0..N executable dependencies
0..N immutable data dependencies
multiple input-binding shapes
generic argv/invocation contract
generic structured result contract
dynamic chunk count
per-chunk identity
final transported-object identity
deterministic transport builder
filesystem/resource limits
cross-unit proof across materially different execution-unit shapes
```

Representative target:

```text
same generic relay/materializer
-> simple fixed-file input unit
-> typed-field unit with executable/data dependencies
-> application-constructed structured-input unit
```

Until such evidence exists:

```text
bounded execution-surface relay primitive = PASS
generic cross-unit execution transport = OPEN
full trusted-host end-to-end integration = OPEN
```

---

## 10. Public reproducibility boundary

The existing public synthetic fixture reproduces the basic deterministic representation/materialization chain locally.

It does **not** reproduce the host-internal caller-context -> execution-surface relay behavior reported here.

Therefore:

```text
local fixture reproduction = available for basic materialization
host-surface relay reproduction = black-box evidence only
independent third-party host-surface reproduction = open
cross-host/vendor reproduction = open
```

This distinction should be preserved in future protocol claims.

---

## 11. Current claim boundary

Observed:

```text
H1 external visible transport -> execution-surface handoff blocked
H2 local attachment plane -> canonical execution PASS
H3 large monolithic caller-context relay -> FAIL
H4 small chunked caller-context literal relay -> bounded composite PASS
```

Inferred:

```text
Host Resource Visibility
!= Caller-Context Availability
!= Execution-Surface Availability
```

Hypothesized / not yet established:

```text
generic cross-unit execution-surface transport
cross-host/vendor relay portability
universal chunk-size thresholds
production-ready trusted-host integration
```
