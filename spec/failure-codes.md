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

## Execution-surface transfer

```text
EXECUTION_SURFACE_TRANSFER_UNAVAILABLE
= declared exact transport data was resolved/observed on one host surface but could not be transferred into the execution surface under the active profile

UNAUTHORIZED_REACQUISITION_ATTEMPT
= the execution surface attempted an undeclared network/repository refetch or alternate acquisition route after host-side resolution

TRANSFERRED_OBJECT_IDENTITY_MISMATCH
= data reached the execution surface but the reconstructed transported object failed its declared final transport identity
```

Host resource visibility alone does not satisfy any of these transfer states.

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

## Filesystem / materialization preconditions

```text
MATERIALIZATION_ROOT_VIOLATION
= resolved materialization path escapes the permitted root

MATERIALIZATION_SYMLINK_DENIED
= final target or a protected path component is a disallowed symlink/alias

MATERIALIZATION_TARGET_EXISTS
= a fresh materialization attempt found a pre-existing final target under a policy that requires absence

MATERIALIZATION_STAGING_FAILURE
= the runtime could not create or safely use the required staging location

MATERIALIZATION_CLEANUP_FAILURE
= a failed attempt could not prove that prohibited final/staging residue was removed or absent

CACHE_REUSE_NOT_AUTHORIZED
= local bytes may match canonical identity, but no explicit cache/reuse policy authorizes using that existing artifact
```

The v0.1 research baseline intentionally treats:

```text
fresh attempt + existing final target
-> MATERIALIZATION_TARGET_EXISTS
-> execution_eligible = false
```

Exact local byte equality does not override this precondition.

## Dependency / execution unit

```text
UNDECLARED_EXECUTABLE_DEPENDENCY
= execution requires code not authorized in the execution unit

DEPENDENCY_IDENTITY_MISMATCH
= a declared executable dependency fails identity verification

DEPENDENCY_AUTHORITY_MISMATCH
= a declared dependency does not have the required executable authority

DEPENDENCY_BINDING_MISMATCH
= the declared dependency/import binding does not match the materialized execution unit

EXECUTION_UNIT_INCOMPLETE
= the complete declared execution unit could not be materialized

DATA_DEPENDENCY_AUTHORITY_VIOLATION
= data/reference material is being treated as executable without separate executable authority
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
implicit cache/reuse
filesystem overwrite/delete/replace for convenience
undeclared retry
```

A future explicit retry or cache protocol may create a separately authorized state, but must not mutate a terminal failed attempt into a PASS.

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

F1 final target symlink
-> MATERIALIZATION_SYMLINK_DENIED

F2 ancestor/root escape
-> MATERIALIZATION_ROOT_VIOLATION

F3 pre-existing final target
-> MATERIALIZATION_TARGET_EXISTS

F3 exact canonical bytes already present, but reuse not authorized
-> MATERIALIZATION_TARGET_EXISTS / CACHE_REUSE_NOT_AUTHORIZED

F4 failed staged identity with no allowed residue
-> canonical identity failure remains terminal; cleanup must preserve a clean final/staging state

H1 host can observe external transport but execution surface cannot receive exact bytes
-> EXECUTION_SURFACE_TRANSFER_UNAVAILABLE

H3 large caller-context object causes sandbox refetch fallback under a no-refetch contract
-> UNAUTHORIZED_REACQUISITION_ATTEMPT

H4 small exact caller-context chunks reconstruct the declared transported object
-> transfer PASS only after final transported-object identity verification
```

This taxonomy should continue to evolve as dependency, USER_DATA, cache, concurrency, cross-platform filesystem, execution-handoff, and host-surface transfer tests produce concrete evidence.
