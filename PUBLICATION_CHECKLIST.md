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
- [x] v0.1-preliminary release notes draft
- [x] Final author name — Jumpei Fujii
- [x] Affiliation wording — omitted; individual research
- [x] Final public license — split licensing: CC BY 4.0 for documentation/research; Apache-2.0 for software/machine-readable executable-materialization artifacts
- [x] CITATION.cff author/repository/license metadata
- [ ] Add release date/DOI to CITATION.cff when available
- [ ] Verify all public links from a logged-out browser after visibility change
- [x] Search public-preparation repository for known internal case/project names
- [x] Confirm no private implementation case name is intentionally required for reproduction
- [x] Final repository-content review for known secret/token/email/private-case patterns
- [x] Confirm reports, README, protocol draft, and experiment matrix describe the same current evidence state

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
- [x] Second independent registered executable black-box exact-materialization PASS
- [x] Representative filesystem/path containment controls F0-F4
- [x] F3 reasoning-pressure control: exact existing bytes do not imply cache/reuse authority
- [ ] Multi-file dependency execution-unit black-box controls
- [ ] USER_DATA separation controls
- [ ] Unicode/newline-sensitive control
- [ ] Larger payload/many-chunk control
- [ ] Cross-host test
- [ ] Cross-vendor/model-family test

## Repository settings before Public

Current settings already confirmed through repository metadata:

- [x] Issues enabled
- [x] Default branch = `main`
- [x] Branch policy reviewed — currently unprotected intentionally during active rapid research; revisit after initial release
- [x] Merge strategy reviewed — squash / merge commit / rebase currently available; not a release blocker
- [ ] Change visibility from Private to Public
- [ ] Enable Discussions for open-ended community design discussion
- [ ] Enable Private Vulnerability Reporting after repository becomes Public
- [ ] Enable available Dependabot / security-analysis features
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

## Privacy note

The repository files do not intentionally include the originating private implementation case name or private project references required for reproduction.

Git commit metadata uses the GitHub account's configured commit email. That same address is already present in the author's existing public GitHub history. Future commits may be switched to a GitHub noreply address separately if desired; changing historical commit metadata would require history rewriting and is not treated as a prerequisite for this preliminary release.

## Current release boundary

Ready for first public visibility as **preliminary research / protocol candidate** after the remaining GitHub UI settings are confirmed.

The following are intentionally *not* prerequisites for initial publication, but remain prerequisites for stronger claims:

```text
dependency execution-unit completion
USER_DATA separation
cross-host/model validation
edge-case representation and scaling
production filesystem hardening
cache/reuse semantics
final execution-handoff semantics
```

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
