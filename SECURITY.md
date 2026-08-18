# Security Policy

This repository contains preliminary research on executable authority, artifact identity, materialization, and execution eligibility across LLM-host boundaries.

The project is **not production-ready**. Security findings are still valuable because they help define the protocol boundary before stronger claims are made.

## Security-sensitive areas

Please report issues involving:

- authority confusion between executable registration and transport representation;
- a representation granting itself authority;
- semantic repair after an identity/authority gate fails;
- alternate operand substitution after a terminal failure;
- path traversal, absolute-path writes, or base-directory escape;
- undeclared executable dependencies;
- content-identity verification bypass;
- stale-revision or wrong-revision acceptance;
- cache poisoning or cache reuse without re-verification;
- USER_DATA being interpreted as executable authority/instruction;
- malformed descriptor fields causing unsafe execution;
- execution occurring before all required gates pass;
- output/evidence being reported as authoritative despite execution failure;
- host retrieval behavior that silently changes supposedly lossless representation data.

## Core invariant

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
Execution Evidence
```

or:

```text
identity cannot be proven
-> authoritative execution eligibility = false
```

## Reporting

While this repository is private during preparation, report issues directly to the repository owner through the available private communication channel.

Before public release, this document will be updated with the preferred public/private disclosure mechanism.

Please avoid publishing a working exploit against an active downstream system before the maintainer has had reasonable time to evaluate it.

## Non-security research failures

Ordinary reproduction failures, model differences, host limitations, or false-negative protocol behavior can be reported through the normal issue templates after the repository becomes public.
