# Public Release Checklist

This repository is intentionally being prepared while still private.

## Content

- [x] Public-facing README
- [x] English preliminary technical report
- [x] Japanese preliminary technical report
- [x] Protocol Draft v0.1
- [x] Illustrative descriptor and failure-code draft
- [x] Experiment matrix / reproduction guidance
- [x] Broad prior-art scan
- [x] Domain-neutral public reference fixture
- [x] Deterministic fixture generator with fixed identity self-check
- [x] Published fixture representation + descriptor
- [x] Local fixture verifier
- [x] Fixture CI workflow definition
- [x] Explicit repository-wide AI Assistance Disclosure
- [x] README summary of AI-assisted research/development methodology
- [x] CONTRIBUTING.md
- [x] SECURITY.md
- [x] Issue / PR contribution templates
- [x] Research roadmap
- [x] Final author name — Jumpei Fujii
- [x] Affiliation wording — omitted; individual research
- [x] Final public license — split licensing: CC BY 4.0 for documentation/research; Apache-2.0 for software/machine-readable executable-materialization artifacts
- [x] CITATION.cff author/repository/license metadata
- [ ] Add release date/DOI to CITATION.cff when available
- [ ] Verify all public links from a logged-out browser after visibility change
- [x] Search public-preparation repository for known internal case/project names
- [x] Confirm no private implementation case name is intentionally required for reproduction
- [ ] Final secret/private-URL scan immediately before Public
- [x] Confirm reports and README describe the same current evidence state

## Evidence before stronger claims

The repository may be published as preliminary research before every item below is complete, but claims must stay scoped accordingly.

- [x] Plain-source functional PASS / exact-identity FAIL counterexample
- [x] Plain Base64 exact PASS — GPT-5.6 Instant
- [x] Plain Base64 exact PASS — GPT-5.6 High
- [x] Deterministic gzip + Base64 exact PASS — GPT-5.6 Instant
- [x] Independent artifact verification for established positive runs
- [x] Missing-operand fail-closed control
- [x] Counterintuitive order fail-closed control
- [x] One-character payload corruption control
- [x] Final source-identity mismatch control
- [x] Unregistered near-identical executable control
- [x] Explicit semantic-repair temptation control
- [x] Domain-neutral synthetic fixture with independently recomputed fixed identities
- [ ] Second independent executable black-box PASS
- [ ] Multi-file dependency control
- [ ] Filesystem/path containment controls
- [ ] USER_DATA separation controls
- [ ] Unicode/newline-sensitive control
- [ ] Larger payload/many-chunk control
- [ ] Cross-host test
- [ ] Cross-vendor/model-family test

## Repository settings before Public

- [ ] Confirm visibility is intentionally changed from Private to Public
- [ ] Enable Issues
- [ ] Enable Discussions if community design discussion is desired
- [ ] Enable Dependabot/security features that are available
- [ ] Confirm branch protection/default branch policy
- [ ] Confirm merge strategy
- [ ] Add repository topics
- [ ] Add website/DOI later if applicable

Suggested topics:

```text
llm
agent
ai-agents
artifact-integrity
content-addressing
software-supply-chain
reproducibility
sandbox
protocol
research
```

## Licensing decision

Accepted split-license model:

```text
documentation / technical reports / prose specifications / research notes
-> CC BY 4.0

source code / scripts / CI / machine-readable protocol examples /
executable fixtures / generated materialization artifacts
-> Apache-2.0
```

Rationale:

```text
CC BY 4.0
-> encourages citation, redistribution, translation, and adaptation of research knowledge

Apache-2.0
-> software-specific permissive reuse with explicit copyright/patent terms
```

The root `LICENSE` defines path/type scope. Canonical license notices/text are under `LICENSES/`.

## Citation

`CITATION.cff` now records:

```text
author = Jumpei Fujii
version = 0.1-preliminary
repository = jumpesan/lossless-executable-materialization
report license = CC-BY-4.0
```

Release date and DOI should be added when they exist.

## Release framing

Recommended first-public wording:

> Preliminary research / protocol candidate. Reproduction, counterexamples, closer prior art, and cross-host/model results are welcome. This repository does not claim that Base64, gzip, hashing, chunking, manifests, or content addressing are novel.

Avoid wording such as:

```text
world-first protocol
proven secure
production-ready
universal across LLMs
novelty established
```

until evidence and prior-art review justify it.
