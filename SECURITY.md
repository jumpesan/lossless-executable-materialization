# Security Policy

This repository contains preliminary research on executable authority, artifact identity, materialization, filesystem preconditions, and execution eligibility across LLM-host boundaries.

The project is **not production-ready**. Security findings are still valuable because they help define the protocol boundary before stronger claims are made.

## Security-sensitive areas

Please report issues involving:

- authority confusion between executable registration and transport representation;
- a representation granting itself authority;
- semantic repair after an identity/authority gate fails;
- alternate operand substitution after a terminal failure;
- path traversal, absolute-path writes, root escape, or symlink/alias confusion;
- unsafe overwrite/replacement of an existing materialization target;
- implicit cache/reuse authority derived only from local byte equality;
- undeclared executable dependencies;
- content-identity verification bypass;
- stale-revision or wrong-revision acceptance;
- cache poisoning or cache reuse without explicit authorization/re-verification;
- USER_DATA being interpreted as executable authority/instruction;
- malformed descriptor fields causing unsafe execution;
- execution occurring before all required gates pass;
- output/evidence being reported as authoritative despite execution failure;
- host retrieval behavior that silently changes supposedly lossless representation data.

## Core invariants

A security report is particularly important if it demonstrates violation of:

```text
Authority
!=
Representation
!=
Transport
!=
Materialized Copy
!=
Filesystem / Cache State
!=
Execution Evidence
```

or:

```text
identity / authority / required materialization precondition cannot be proven
-> authoritative execution eligibility = false
```

or:

```text
canonical local byte equality
!=
implicit cache/reuse authorization
```

## Reporting a vulnerability

For security-sensitive findings, please use **GitHub Private Vulnerability Reporting** when it is enabled for this public repository.

Do not publish exploit details, secret material, or a working bypass in a public issue before the maintainer has had reasonable time to evaluate it.

If private vulnerability reporting is temporarily unavailable, open a minimal public issue asking for a private security contact **without including sensitive technical details**.

Ordinary reproduction failures, model differences, host limitations, specification disagreements, or false-negative protocol behavior that do not create a security-sensitive disclosure can be reported through the normal issue templates.

## Scope and expectations

Because this repository is preliminary research:

```text
protocol candidate != production security guarantee
```

A report may still be valuable even if it affects only one model, one host, one representation profile, or one filesystem environment. Please include enough environment and reproduction detail to distinguish an observed result from an inference.

## Coordinated disclosure

Please allow reasonable time for triage, reproduction, and remediation before public disclosure of a security-sensitive issue. If the finding changes a published protocol claim, the project will aim to update the relevant specification/evidence status rather than silently treating the old claim as still established.
