# Public Reference Fixture

This directory provides a **domain-neutral, synthetic executable fixture** so the materialization protocol candidate can be reproduced without access to the private implementation project that originally exposed the problem.

The fixture is intentionally not a production validator. Its purpose is to test:

```text
ordered representation acquisition
-> strict transport decode
-> intermediate identity verification
-> deterministic decompression
-> final canonical identity verification
-> compile
-> deterministic execution
-> structured result
```

## Files

```text
fixtures/
  generate_reference_fixture.py
  verify_reference_fixture.py
  README.md

  representation/
    reference_fixture.descriptor.json
    reference_fixture.gzip-base64.part-001.b64
    reference_fixture.gzip-base64.part-002.b64
    reference_fixture.gzip-base64.part-003.b64
```

The canonical source is **generated deterministically** by `generate_reference_fixture.py`; it does not need to be committed as a second authority source.

## Canonical identity

```text
fixture_id = lem-reference-fixture-v0.1
canonical size = 12123 bytes
canonical SHA-256 = 31594021147f13e6d824cc61c083d3fdd674bf79ee5eda590d5a4b7fe6b1123d
canonical Git blob SHA-1 = 8fcd8da1dbbb09e1cea2c565a7abc27d7363ff7a
```

Representation profile:

```text
deterministic gzip
compresslevel = 9
mtime = 0
Base64
ordered ASCII chunks
chunk target = 4096 characters
```

Observed deterministic representation identities:

```text
gzip size = 6321 bytes
gzip SHA-256 = ec5839b3636ef7d5d03b362f781c676c0812f96e80d138b4e358dba32376da08
Base64 = 8428 characters
chunks = 4096 + 4096 + 236
```

## Local verification

From the repository root:

```bash
python fixtures/verify_reference_fixture.py
```

The verifier:

```text
reads the descriptor
-> checks every declared operand length/hash
-> concatenates only in descriptor order
-> strict Base64 decode
-> verifies compressed size/SHA-256
-> gzip decompress
-> verifies final size/SHA-256/Git blob identity
-> compiles recovered source
-> executes a declared synthetic JSON input
-> validates structured status
```

No semantic source repair is part of the verifier.

## Regeneration

To recreate the canonical fixture and representation locally:

```bash
python fixtures/generate_reference_fixture.py
```

The generator contains fixed expected identities. If the deterministic source generator or compression representation changes unintentionally, generation fails instead of silently creating a new fixture identity.

The generator writes a local canonical file under:

```text
fixtures/canonical/reference_fixture.py
```

and regenerates the representation directory. The generated canonical file is a local verification artifact, not an additional authority source in this repository.

## Independent LLM-host reproduction

For a non-blind functional reproduction, an LLM-host session can be given the public descriptor and asked to follow it mechanically.

For a stronger **blind identity experiment**, do not disclose the final `canonical_identity` values to the test agent before materialization. One practical method is to copy the descriptor into a temporary test fixture with the final identity withheld from the agent, then compare the agent-reported identity against this repository's canonical values after the run.

A valid protocol test must not use `generate_reference_fixture.py` or a generated human-readable canonical source as repair material after a representation gate has failed.

## Why a synthetic fixture exists

The original empirical case is intentionally not required for public reproduction.

This fixture allows the community to test the transport/materialization boundary itself:

```text
Context / domain semantics
!=
materialization protocol evidence
```

If the protocol candidate is general, its core behavior should survive a domain-neutral executable whose only role is to provide deterministic bytes and deterministic structured execution.
