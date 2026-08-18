# Broad Prior-Art Scan

## Status

```text
created: 2026-08-18
stage: first broad scan
comparison_target: Lossless Executable Materialization Protocol Candidate
claim_status: no novelty claim established
```

This scan intentionally uses terminology outside the LLM ecosystem because similar mechanisms may exist under very different names.

Target behavior:

```text
authorized canonical executable
-> lossless host-visible representation
-> ordered acquisition / assembly
-> deterministic decode / local materialization
-> exact content identity verification
-> execution eligibility only after identity PASS
-> deterministic execution
-> structured result / execution evidence
```

No single specification identified in this first scan exactly combines the full LLM-host-specific composition. However, nearly every individual mechanism has strong prior art.

The candidate should therefore **not** be framed as inventing Base64, compression, hashing, chunking, manifests, content addressing, signatures, or reproducible execution.

The potentially distinct contribution is the **composition/profile of those mechanisms around an LLM-host observation boundary**.

---

# 1. OCI Image / Artifact Content Descriptors

Official references:

- https://github.com/opencontainers/image-spec/blob/main/descriptor.md
- https://github.com/opencontainers/image-spec/blob/main/manifest.md

Relevant concepts:

```text
mediaType
digest
raw byte size
optional URLs
optional embedded data
```

OCI's optional `data` field can carry Base64-encoded referenced content. This is close to:

```text
canonical bytes
-> encoded representation
-> decode
-> size/digest verify
```

Difference: OCI assumes a conventional software client receiving/fetching artifact data. It does not model an LLM host whose semantic rendering may normalize human-readable source before a sandbox rematerializes it.

---

# 2. Subresource Integrity (SRI)

Official specification:

- https://www.w3.org/TR/sri-2/

Relevant shape:

```text
expected digest
+ remotely retrieved bytes
-> integrity verification
-> exact match: resource accepted
-> mismatch: resource rejected
```

This is strong prior art for the candidate's:

```text
identity PASS
-> execution eligibility
```

Difference: SRI verifies bytes obtained through a normal browser Fetch pipeline; it does not solve LLM-host-side lossless rematerialization.

---

# 3. The Update Framework (TUF)

Official specification:

- https://theupdateframework.github.io/specification/

TUF separates trusted metadata roles from target files. Targets metadata binds path, length, hashes, versioning, and delegated authority.

Relevant principle:

```text
authority metadata
!=
target bytes
```

This strongly resembles the candidate's requirement that Transport Representation never self-authorize.

Difference: TUF assumes conventional target download clients rather than LLM-visible lossless representations and sandbox rematerialization.

---

# 4. Nix Fixed-Output / Content-Addressed Derivations

Official reference:

- https://releases.nixos.org/nix/nix-2.28.2/manual/store/derivation/outputs/content-address.html

Relevant principle:

```text
acquisition may be impure / variable
-> recovered output
-> expected content identity check
-> mismatch = failure
```

This supports a central design choice:

```text
transport/acquisition need not be authoritative
if final bytes are cryptographically fixed and verified
```

Difference: Nix is a build/store realization system, not an LLM-hosted runtime protocol.

---

# 5. BitTorrent Pieces

Protocol:

- https://www.bittorrent.org/beps/bep_0003.html

Relevant shape:

```text
metainfo
-> fixed ordered pieces
-> piece acquisition
-> piece verification
-> final reconstruction
```

Chunking and ordered reconstruction are established concepts. The candidate uses chunking for a different reason: reliable host-visible representation across an LLM observation boundary.

---

# 6. IPFS / IPLD / CAR

Official references:

- https://docs.ipfs.tech/concepts/content-addressing/
- https://ipld.io/specs/transport/car/carv1/
- https://specs.ipfs.tech/http-gateways/trustless-gateway/

Relevant shape:

```text
content identity
-> block acquisition
-> per-block verification
-> graph/archive reconstruction
```

This prior art becomes especially relevant if the candidate expands to multi-file/dependency graphs.

Difference: IPFS/IPLD does not define LLM-host executable authority or execution eligibility.

---

# 7. RFC 6920 Named Information URIs

Official RFC:

- https://www.rfc-editor.org/rfc/rfc6920.html

Relevant principle:

```text
where bytes came from
!=
what bytes they are
```

This aligns directly with content identity being independent from retrieval location or transport representation.

---

# 8. Model Context Protocol Resources

Official references:

- https://modelcontextprotocol.io/specification/2025-11-25/server/resources
- https://modelcontextprotocol.io/specification/2025-11-25/schema

MCP Resources support binary content via Base64-encoded blob representation.

Relevant shape:

```text
LLM client
<- resource metadata + Base64 blob
```

Difference: MCP resource transport does not itself define the candidate's canonical executable authority, digest gate, ordered rematerialization contract, or semantic-repair prohibition.

---

# 9. Agent Skills

Official references:

- https://agentskills.io/specification
- https://agentskills.io/skill-creation/using-scripts

Agent Skills package instructions, scripts, references, and assets as reusable LLM capabilities.

Relevant layout:

```text
SKILL.md
scripts/
references/
assets/
```

Difference: the current specification is about package behavior and execution, not public-Web lossless rematerialization plus byte-exact execution eligibility.

---

# 10. in-toto / SLSA / Sigstore

Official references:

- https://in-toto.io/
- https://github.com/in-toto/docs/blob/master/in-toto-spec.md
- https://slsa.dev/spec/v1.2/verifying-artifacts
- https://docs.sigstore.dev/about/bundle/

These systems address artifact provenance, publisher/signature evidence, and digest verification.

They are likely important for future publisher/provenance authority, but they do not replace the materialization transport layer.

---

# 11. Context-to-Execution Integrity (CXI)

Research paper:

- https://arxiv.org/abs/2607.06000

CXI studies authorization boundaries between attacker-writable LLM context and protected tool/effect execution.

Conceptual overlap:

```text
semantic context alone
!=
execution authority
```

Difference: CXI primarily controls authority over effects/tool calls. The current candidate operates one layer lower: acquiring the exact executable implementation that is allowed to execute.

---

# Similarity Map

```text
Candidate responsibility                         Closest prior art
------------------------------------------------ -------------------------------
manifest/component description                   OCI manifests/descriptors
Base64 representation of opaque bytes            OCI descriptor data, MCP blob
fixed chunk ordering                             BitTorrent pieces, block archives
content-addressed identity                       OCI, IPFS/IPLD, RFC 6920, Nix
length/hash acceptance                           OCI, TUF, Nix, SRI
exact identity before execution                  SRI
trusted role/target authority                    TUF
artifact provenance/publisher evidence           in-toto, SLSA, Sigstore
LLM-native package with scripts                  Agent Skills
LLM tool/effect authority boundary               CXI
LLM-host normalizing observation workaround      no direct equivalent found yet
sandbox rematerialization after host observation no direct equivalent found yet
semantic repair forbidden as canonical authority no direct equivalent found yet
```

---

# Current Interpretation

The candidate can currently be understood roughly as a composition of:

```text
TUF-like authority / target identity
        +
OCI-like content descriptor / encoded representation
        +
MCP-like LLM-facing binary-resource representation
        +
SRI-like exact-identity-before-execution gate
```

with BitTorrent/IPFS-like chunking/content addressing becoming increasingly relevant as payload size and dependency graphs grow.

The first scan did not find an established specification whose explicit problem statement is:

```text
A general LLM host can observe public resources,
but its human-readable / semantic representation may normalize bytes,
and its execution sandbox may not have equivalent direct retrieval.

Therefore expose an authorized executable through a lossless Agent-facing representation,
let the host acquire and assemble it,
mechanically decode/materialize inside the sandbox,
prove canonical content identity,
and only then permit authoritative deterministic execution.
```

This remains a **prior-art observation, not a novelty proof**.

Contributions identifying closer prior art are explicitly welcome.