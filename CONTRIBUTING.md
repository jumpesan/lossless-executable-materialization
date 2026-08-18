# Contributing

Thank you for helping test, challenge, or improve this research.

This project is intentionally at the **protocol-candidate** stage. Reproductions, failures, contradictory evidence, closer prior art, and design criticism are as valuable as positive results.

## What we are looking for

The highest-value contributions are:

- independent reproduction results;
- negative / fail-closed results;
- cross-model or cross-host experiments;
- examples where host-visible representation is normalized, truncated, reordered, or corrupted;
- multi-file/dependency materialization tests;
- Unicode / CRLF / BOM / newline-sensitive cases;
- large-payload / many-chunk scaling results;
- filesystem/path containment findings;
- user-data / executable-authority separation findings;
- closer prior art or existing protocols/specifications;
- protocol-state-machine or descriptor-schema criticism;
- security issues that weaken authority, identity, or fail-closed semantics.

## Evidence labels

When reporting a result, please distinguish:

```text
Observed
= directly measured in the run

Inferred
= interpretation supported by observed evidence

Hypothesized
= proposed explanation not yet established

Desired
= target architecture or expected behavior
```

Do not report an inference as if it were an observed fact.

## Reproduction expectations

Where possible, include:

```text
host/product
model
reasoning mode
session isolation level
connector/tool availability
representation profile
artifact size
artifact SHA-256
artifact content identifier (e.g. Git blob SHA if applicable)
compile result
execution result
structured output result
semantic repair used: yes/no
first failure gate
execution eligible: true/false
```

If the expected canonical identity was withheld during the run, say so explicitly.

## Negative tests

A fail-closed test is successful when the system stops at the correct gate.

Examples:

```text
missing operand
wrong declared ordering
corrupted encoded payload
compressed identity mismatch
final executable identity mismatch
unregistered executable
explicit repair temptation after terminal failure
unsafe filesystem target/path state
implicit cache/reuse temptation
```

Please do not "fix" a negative-control payload during the same attempt and then report the repaired execution as a protocol pass.

## Prior-art contributions

If you know an existing protocol, paper, package system, agent runtime, content-addressed transport, supply-chain specification, or execution-integrity mechanism that overlaps with this work, please open a Prior Art issue.

Especially useful is a responsibility-by-responsibility comparison:

```text
authority
representation
transport
assembly
identity proof
filesystem/materialization preconditions
execution-unit semantics
execution gate
semantic-repair behavior
LLM-host boundary
```

The goal is accuracy, not novelty theater.

## Pull requests

Before proposing a large normative change to `spec/`, please open an issue first so the evidence and intended protocol boundary are clear.

Small documentation corrections, reference additions, and experiment clarifications may be submitted directly.

Protocol language should use:

- **MUST** for requirements needed to preserve the stated invariant;
- **SHOULD** for recommended behavior;
- **MAY** for optional behavior.

Until the protocol matures, normative wording may still change.

## Contribution licensing

This repository uses split licensing. By intentionally submitting a contribution for inclusion in this repository, you agree that the contribution may be distributed under the license that applies to its destination file/path unless you clearly state otherwise before acceptance.

Default contribution licensing follows the root [LICENSE](LICENSE):

```text
documentation / reports / prose specifications / research notes
-> CC BY 4.0

source code / scripts / CI / machine-readable protocol examples /
executable fixtures / generated materialization artifacts
-> Apache-2.0
```

If a file contains an explicit file-level license or SPDX notice, that notice takes precedence.

Do not submit third-party material unless you have the right to do so and its license/attribution requirements are clearly identified.

## AI-assisted contributions

AI-assisted drafting or coding is allowed. Contributors remain responsible for what they submit, including correctness, licensing, provenance, and any claims made about experimental evidence.

AI-generated interpretation alone is not sufficient evidence for a protocol claim. Reproduction or experimental claims should include inspectable run/artifact evidence where possible.
