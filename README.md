# Lossless Executable Materialization

> Preliminary research on verifiable executable materialization across an LLM-host boundary.

**Author:** Jumpei Fujii (GitHub: [@jumpesan](https://github.com/jumpesan))

[日本語](#日本語) · [English](#english)

## English

This repository focuses on a protocol candidate that emerged from real LLM-hosted application development:

> How can an LLM-hosted runtime obtain the exact executable bytes that are authorized to run, prove that identity locally, and fail closed when exact materialization cannot be established?

The problem appeared after the LLM could determine **which deterministic executable should run**, while the host-provided execution environment could not reliably obtain the exact registered executable bytes.

A critical black-box counterexample then showed that human-readable source can preserve program meaning while losing byte identity:

```text
functional behavior = PASS
all nonblank lines preserved = PASS
33 blank lines removed
SHA-256 / Git blob identity = FAIL
```

This changed the problem from source reconstruction to **lossless executable materialization**.

### Protocol candidate

```text
Executable Authority
-> Lossless Representation
-> Representation Acquisition
-> Deterministic Assembly
-> Mechanical Decode / Materialization
-> Identity Proof
-> Execution Eligibility
-> Deterministic Execution Evidence
```

The central invariant is:

```text
semantic or functional equivalence
!=
canonical executable identity
```

A program that compiles, runs, and produces the expected result is still not treated as the authoritative executable when exact identity is required but unproven.

### Current empirical evidence

Current evidence includes exact materialization across **two distinct registered single-file executables**.

For the primary sample:

```text
plain chunked Base64 / GPT-5.6 Instant = EXACT PASS
plain chunked Base64 / GPT-5.6 High    = EXACT PASS
deterministic gzip + Base64 / GPT-5.6 Instant = EXACT PASS
```

The deterministic gzip + Base64 profile reduced the tested transport representation from:

```text
26076 characters / 7 chunks
->
5480 characters / 2 chunks
```

or approximately **79% fewer transport characters** for that sample.

A second registered executable also passed exact black-box materialization with GPT-5.6 Instant.

Fail-closed controls for the current samples include:

```text
missing declared operands
counterintuitive declared chunk order
one-character payload corruption
final canonical identity mismatch
unregistered near-identical executable
explicit semantic-repair temptation after terminal failure
```

Representative filesystem controls F0-F4 also passed. These cover clean isolated materialization, final-target symlink denial, ancestor/root-escape denial, pre-existing final-target denial, and failed staged-materialization cleanup. A reasoning-pressure run additionally confirmed that even a pre-existing file with exact canonical bytes was **not** silently upgraded into cache/reuse authority.

Dependency execution-unit validation is the next active area and is **not yet counted as PASS**.

These results are **sample-scoped preliminary evidence**, not a production guarantee or novelty proof.

### Public reference fixture

The repository also includes a domain-neutral synthetic executable fixture so the materialization flow can be reproduced without depending on the application domain that originally exposed the problem.

```bash
python fixtures/verify_reference_fixture.py
```

The verifier exercises:

```text
ordered operand acquisition
-> strict Base64 decode
-> compressed identity verification
-> deterministic gzip decompression
-> canonical identity verification
-> compile
-> deterministic execution
-> structured-result validation
```

See [fixtures/README.md](fixtures/README.md).

### Scope

This repository intentionally focuses on the **Lossless Executable Materialization protocol candidate** and the evidence needed to evaluate it.

It does not attempt to publish a broader AI-development methodology or unrelated upstream research program. The application domain in which the problem was first encountered is not required to understand or reproduce the protocol.

### AI assistance disclosure

This research and repository were developed with **extensive use of AI assistants**, primarily through general-purpose ChatGPT/LLM environments. AI assistance has been used for protocol and architecture exploration, hypothesis generation and critique, experiment planning, drafting/refactoring code and documentation, analysis support, prior-art search support, editing, translation, and repository preparation.

AI also appears separately as part of the experimental runtime/host being studied. These two roles should not be conflated.

AI-generated text, code, or interpretation is **not treated as experimental evidence by itself**. Claims are intended to remain grounded in inspectable artifacts, cryptographic identities, machine execution results, structured outputs, negative controls, and black-box observations. Human responsibility for research direction, evidence acceptance, interpretation, and publication remains explicit.

See [AI_ASSISTANCE.md](AI_ASSISTANCE.md).

### What is not claimed as new

This project does **not** claim invention of Base64, gzip, hashing, chunking, manifests, content addressing, reproducible execution, or software-supply-chain verification. Strong prior art exists in OCI, TUF, SRI, Nix, BitTorrent/IPFS/IPLD, MCP resources, Agent Skills, in-toto/SLSA/Sigstore, and adjacent execution-integrity work.

The research question is whether those mature primitives form a useful protocol layer for an LLM-host boundary where:

```text
host-visible representations may be normalized or transformed
+
execution environments may have different acquisition capabilities
+
exact registered executable identity is still required before authoritative execution
```

### Licensing

This repository uses split licensing:

```text
documentation / reports / prose specifications / research notes
-> CC BY 4.0

source code / scripts / CI / machine-readable examples /
executable fixtures / generated materialization artifacts
-> Apache-2.0
```

See [LICENSE](LICENSE) and [LICENSES/](LICENSES/).

### Repository layout

```text
reports/
  preliminary-report.en.md
  preliminary-report.ja.md

spec/
  protocol-draft-v0.1.md
  descriptor-example.json
  failure-codes.md

experiments/
  README.md

fixtures/
  README.md
  generate_reference_fixture.py
  verify_reference_fixture.py
  representation/

research/
  prior-art.md

AI_ASSISTANCE.md
CONTRIBUTING.md
SECURITY.md
ROADMAP.md
PUBLICATION_CHECKLIST.md
CITATION.cff
LICENSE
LICENSES/
NOTICE
```

Read more:

- [Preliminary Technical Report — English](reports/preliminary-report.en.md)
- [予備技術レポート — 日本語](reports/preliminary-report.ja.md)
- [Protocol Draft v0.1](spec/protocol-draft-v0.1.md)
- [Experiment Matrix](experiments/README.md)
- [Public Reference Fixture](fixtures/README.md)
- [AI Assistance Disclosure](AI_ASSISTANCE.md)
- [Prior-Art Scan](research/prior-art.md)
- [Research Roadmap](ROADMAP.md)

Independent reproduction, counterexamples, closer prior art, cross-model/host tests, and protocol-design criticism are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 日本語

このRepositoryは、実際のLLM-hosted Application開発中に発生した **Lossless Executable Materialization** という1つのProtocol Candidateを扱う公開研究Repositoryです。

扱う問いは次です。

> LLMが「どのdeterministic executableを実行すべきか」を判断できても、Execution Environmentにその登録済みExecutableの正確なbytesが存在するとは限らない。では、そのExecutableをlosslessにmaterializeし、local identityを証明してからだけ実行資格を与えるにはどうすればよいか。

初期のblack-box testでは、人間可読なPython Sourceを再構成した際、非空行はすべて一致し、compile / execution / structured resultもPASSした一方で、33行の空行が失われ、SHA-256 / Git blob identityが一致しない反例が得られました。

```text
意味・機能が同じ
!=
正本Executableと同一
```

この結果から、Source Reconstructionではなく **Lossless Executable Materialization** をProtocolとして扱う方向へ進みました。

### Protocol Candidate

```text
Executable Authority
-> Lossless Representation
-> Representation Acquisition
-> Deterministic Assembly
-> Mechanical Decode / Materialization
-> Identity Proof
-> Execution Eligibility
-> Deterministic Execution Evidence
```

中心Invariantは次です。

```text
semantic / functional equivalence
!=
canonical executable identity
```

### 現在の実証Evidence

現在は、**2つの異なるregistered single-file executable**でexact materializationを確認しています。

Primary sampleでは:

```text
plain chunked Base64 / GPT-5.6 Instant = EXACT PASS
plain chunked Base64 / GPT-5.6 High    = EXACT PASS
deterministic gzip + Base64 / GPT-5.6 Instant = EXACT PASS
```

deterministic gzip + Base64 profileでは、同一sampleのtransport representationを

```text
26076文字 / 7 chunk
->
5480文字 / 2 chunk
```

へ削減し、約79%のtransport文字削減を確認しました。

さらにsecond registered executableでもGPT-5.6 Instantのblack-box exact materializationがPASSしています。

Fail-closed controlでは、missing operand、宣言順序の逆転、1文字corruption、final identity mismatch、未登録の近似Executable、terminal failure後のsemantic-repair temptationを検証しています。

Filesystemについても代表的なF0-F4がPASSしており、symlink/root escape、pre-existing final target、失敗後のstaging residueをdenyできています。また、既存targetがcanonical bytesと完全一致していても、それを勝手にcache/reuse authorityへ昇格しないことをreasoning-pressure testで確認しています。

Dependency execution-unit validationは次の検証対象であり、**まだPASSには数えていません**。

これらはsample-scopedなpreliminary evidenceであり、Production Safetyや一般的新規性を主張するものではありません。

### Public Reference Fixture

Application Domainに依存せず第三者がMaterialization Flowを確認できるように、domain-neutralなsynthetic executable fixtureも同梱しています。

```bash
python fixtures/verify_reference_fixture.py
```

Verifierは次をmechanicalに確認します。

```text
ordered operand acquisition
-> strict Base64 decode
-> compressed identity verification
-> deterministic gzip decompression
-> canonical identity verification
-> compile
-> deterministic execution
-> structured-result validation
```

詳細は [fixtures/README.md](fixtures/README.md) を参照してください。

### 公開範囲

このRepositoryでは、**Lossless Executable Materialization Protocolそのものと、その評価に必要なEvidence**に対象を絞ります。

より広いAI開発方法論や、今回のProtocolと直接関係しない上流研究体系を公開・解説することは目的にしません。問題が最初に発生したApplication Domainを知らなくても、このProtocolは理解・再現できる構成にします。

### AI利用の開示

本研究およびRepository作成では、**AI Assistantを積極的かつ広範囲に使用しています**。Protocol/Architecture検討、仮説生成と反論、実験計画、code/documentのdraft・refactor、分析支援、prior-art探索支援、編集、翻訳、Repository整備などに利用しています。

またAI/LLMは、研究支援とは別に、実験対象となるRuntime/Hostの一部としても登場します。この2つの役割は区別します。

AI生成の文章・code・解釈そのものは、単独ではExperimental Evidenceとして扱いません。主張は、Artifact、cryptographic identity、machine execution result、structured output、negative control、black-box observationなど検証可能なEvidenceへ結び付けます。研究方向、Evidenceの採否、解釈、公開内容についてはHuman Researcherが責任を持ちます。

詳細は [AI_ASSISTANCE.md](AI_ASSISTANCE.md) を参照してください。

### ライセンス

```text
研究文書 / Technical Report / 文章によるSpecification / Research Note
-> CC BY 4.0

Source Code / Script / CI / Machine-readable Example /
Executable Fixture / Generated Materialization Artifact
-> Apache-2.0
```

適用範囲は [LICENSE](LICENSE)、正式なLicense本文は [LICENSES/](LICENSES/) を参照してください。

- [日本語 予備技術レポート](reports/preliminary-report.ja.md)
- [English Preliminary Technical Report](reports/preliminary-report.en.md)
- [Protocol Draft v0.1](spec/protocol-draft-v0.1.md)
- [Experiment Matrix](experiments/README.md)
- [Public Reference Fixture](fixtures/README.md)
- [Prior-Art Scan](research/prior-art.md)
- [Research Roadmap](ROADMAP.md)
