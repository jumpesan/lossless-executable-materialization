# Draft Failure-Code Taxonomy

Status: **research draft / not standardized**.

A protocol-like materialization flow benefits from machine-readable failure states. The LLM should explain them, but explanation must not replace or override them.

## Authority

```text
AUTHORITY_UNRESOLVED
= the executable authority could not be established

EXECUTABLE_NOT_REGISTERED
= the requested/selected exact executable identity is absent from the authority registry

AUTHORITY_REVISION_MISMATCH
= executable authority exists but the requested revision does not match
```

## Representation resolution / acquisition

```text
REPRESENTATION_UNRESOLVED
= no authorized/declared representation could be resolved

REPRESENTATION_REVISION_MISMATCH
= the representation revision does not match the declared binding

MISSING_OPERAND
= a declared representation unit could not be acquired

DUPLICATE_OPERAND
= a descriptor declares an invalid duplicate unit under the active profile

OPERAND_IDENTITY_MISMATCH
= an acquired representation unit fails its declared identity
```

## Assembly / decoding

```text
ASSEMBLY_RULE_VIOLATION
= declared deterministic ordering/layout could not be followed

TRANSPORT_DECODE_FAILURE
= strict transport decoding failed

COMPRESSED_IDENTITY_MISMATCH
= decoded compressed/intermediate bytes fail the declared identity gate

DECOMPRESSION_FAILURE
= profile-defined decompression failed after the intermediate identity gate

UNSUPPORTED_REPRESENTATION_PROFILE
= the runtime does not support the declared mechanical transformation profile
```

## Canonical materialization

```text
CANONICAL_SIZE_MISMATCH
= final materialized byte length does not match

CANONICAL_DIGEST_MISMATCH
= final cryptographic digest does not match

CANONICAL_CONTENT_ID_MISMATCH
= final content identifier such as Git blob identity does not match

CANONICAL_IDENTITY_UNPROVEN
= required identity evidence is incomplete
```

## Filesystem / dependency

```text
OUTPUT_PATH_VIOLATION
= materialization target escapes the permitted filesystem boundary

UNDECLARED_EXECUTABLE_DEPENDENCY
= execution requires code not authorized in the execution unit

DEPENDENCY_IDENTITY_MISMATCH
= a declared executable dependency fails identity verification

EXECUTION_UNIT_INCOMPLETE
= the complete declared execution unit could not be materialized
```

## Execution

```text
NOT_EXECUTION_ELIGIBLE
= one or more required pre-execution gates did not pass

EXECUTION_FAILURE
= an eligible artifact was invoked but the registered execution interface failed

STRUCTURED_RESULT_INVALID
= execution completed but the required machine-readable result contract was not satisfied
```

## Terminal semantics

Any failure configured as terminal for the current attempt MUST preserve:

```text
execution_eligible = false
```

The current attempt MUST NOT be upgraded by:

```text
semantic source repair
alternate representation substitution
functionally equivalent reimplementation
human-obvious operand reordering
undeclared retry
```

A future explicit retry protocol may create a **new attempt**, but must not mutate a terminal failed attempt into a PASS.

## Current evidence-linked examples

```text
N1 missing declared chunk
-> MISSING_OPERAND

N2 descriptor-declared counterintuitive order causing strict Base64 failure
-> TRANSPORT_DECODE_FAILURE

N3 one-character corruption with valid Base64
-> COMPRESSED_IDENTITY_MISMATCH

N5 final source identity mismatch
-> CANONICAL_DIGEST_MISMATCH / CANONICAL_CONTENT_ID_MISMATCH

N6 unregistered near-identical executable
-> EXECUTABLE_NOT_REGISTERED

N7 known-good repair candidates visible after N3-style failure
-> COMPRESSED_IDENTITY_MISMATCH remains terminal; no repair/retry
```

This taxonomy should be revised as filesystem, dependency, USER_DATA, cache, and execution-handoff tests produce concrete evidence.