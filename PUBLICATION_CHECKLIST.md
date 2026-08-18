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
- [x] CONTRIBUTING.md
- [x] SECURITY.md
- [x] Issue / PR contribution templates
- [x] Research roadmap
- [ ] Final author name
- [ ] Final affiliation wording
- [ ] Final public license
- [ ] Final CITATION.cff
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

Do not add a repository-wide license accidentally before deciding whether code/spec/docs should share one license.

Possible split to evaluate:

```text
documentation / technical report / specification
-> CC BY 4.0 or similar documentation-friendly license

reference implementation / scripts
-> Apache-2.0 or MIT
```

This is a decision item, not a recommendation already accepted.

## Citation

`CITATION.cff` should be created only after the public author name is finalized.

Suggested title:

```text
Lossless Executable Materialization Across an LLM Host Boundary
```

Suggested initial version label:

```text
0.1-preliminary
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
