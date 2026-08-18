# v0.1-preliminary — Release Notes

## Lossless Executable Materialization Across an LLM Host Boundary

Author: **Jumpei Fujii**

This is the first public-facing release candidate for the **Lossless Executable Materialization** protocol research.

The protocol candidate emerged from real LLM-hosted application development after a runtime reached the following boundary:

```text
LLM understands which executable should run
!=
the exact authorized executable bytes are available in the sandbox
```

The research asks how an authorized executable can be represented losslessly, materialized mechanically, verified against canonical identity, and made execution-eligible only after the required gates pass.

## Main observation

Human-readable source can remain semantically and functionally correct while exact executable identity is lost.

In the critical counterexample:

```text
nonblank source lines = 465 / 465 exact
blank lines removed = 33
compile = PASS
execution = PASS
structured result = PASS
SHA-256 = FAIL
Git blob identity = FAIL
```

This motivated a lossless representation/materialization boundary rather than semantic source reconstruction.

## Positive evidence in v0.1-preliminary

```text
Primary registered executable
  plain chunked Base64 / GPT-5.6 Instant = EXACT PASS
  plain chunked Base64 / GPT-5.6 High = EXACT PASS
  deterministic gzip + Base64 / GPT-5.6 Instant = EXACT PASS

Second registered executable
  deterministic lossless representation / GPT-5.6 Instant = EXACT MATERIALIZATION PASS
```

For the primary 19,555-byte executable, deterministic gzip + Base64 reduced the tested transport representation from:

```text
26076 Base64 chars / 7 chunks
->
5480 Base64 chars / 2 chunks
```

approximately a 79% reduction in transport characters.

## Fail-closed evidence

Current controls include:

```text
N1 missing operand = PASS
N2 counterintuitive declared order = PASS / Instant + High
N3 one-character payload corruption = PASS
N5 final canonical identity mismatch = PASS / Instant + High
N6 unregistered near-identical executable = PASS / Instant + High
N7 explicit semantic-repair temptation = PASS / Instant + High
```

The current filesystem/materialization baseline also includes:

```text
F0 clean isolated root = PASS
F1 final target symlink = DENY / PASS
F2 ancestor/root escape = DENY / PASS
F3 pre-existing final target = DENY / PASS
F4 failed staged identity leaves no prohibited residue = PASS
```

Reasoning-pressure testing also supports:

```text
canonical local byte equality
!=
implicit cache/reuse authority
```

A pre-existing exact-byte artifact was not automatically reused, replaced, compiled, or executed.

## Protocol candidate

The current abstraction separates:

```text
Executable Authority
-> Lossless Representation
-> Representation Acquisition
-> Deterministic Materialization
-> Identity Proof
-> Filesystem / Materialization Preconditions
-> Execution Eligibility
-> Deterministic Execution Evidence
```

This repository does **not** claim invention of Base64, gzip, hashing, chunking, manifests, content addressing, reproducible execution, or software-supply-chain verification.

It also does not claim that the current protocol candidate is standardized, production-ready, universally portable, or proven novel.

## Public reproduction

A domain-neutral synthetic reference fixture is included so the materialization chain can be inspected without depending on the application domain that originally exposed the problem.

```bash
python fixtures/verify_reference_fixture.py
```

## Active next validation

A real registered two-file dependency execution unit has been prepared and independently round-trip verified. Its D2-D4 black-box controls are next and are **not counted as PASS in this release**.

Other open areas include USER_DATA separation, Unicode/newline edge cases, larger payloads, explicit cache semantics, filesystem concurrency/TOCTOU, final execution handoff, and cross-host/model portability.

## AI assistance disclosure

AI assistants were used extensively in the research and engineering workflow. AI-generated text, code, or interpretation is not treated as experimental evidence by itself. See `AI_ASSISTANCE.md`.

## License

```text
Documentation / reports / prose specifications / research notes
-> CC BY 4.0

Software / scripts / CI / machine-readable examples /
executable fixtures / generated materialization artifacts
-> Apache-2.0
```

See `LICENSE` for exact scope.

## Feedback wanted

Reproduction results, counterexamples, closer prior art, cross-model/host results, security criticism, and protocol-design feedback are welcome.
