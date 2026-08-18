# Lossless Executable Materialization

> Preliminary research on verifiable executable materialization across an LLM-host boundary.

**Author:** Jumpei Fujii (GitHub: [@jumpesan](https://github.com/jumpesan))

[日本語](#日本語) · [English](#english)

## English

This repository focuses on one narrow problem:

> How can an LLM-hosted runtime obtain the exact executable bytes that are authorized to run, prove that identity locally, and fail closed when exact materialization cannot be established?

The problem appears when an LLM can identify which deterministic executable is required, while the execution environment does not automatically possess a trustworthy byte-exact copy of that executable.

The protocol candidate separates:

```text
Executable Authority
-> Lossless Representation
-> Representation Acquisition
-> Deterministic Assembly
-> Mechanical Materialization
-> Identity Proof
-> Execution Eligibility
-> Deterministic Execution Evidence
```

Its core invariant is:

```text
semantic or functional equivalence
!=
canonical executable identity
```

A program that compiles, runs, and produces the expected result is still not treated as the authoritative executable when exact identity is required but unproven.

### Scope

This repository is intentionally limited to the **Lossless Executable Materialization protocol candidate** and the evidence needed to evaluate it.

It does not attempt to publish or document the broader application architecture, product, domain implementation, or upstream research program from which the materialization problem was first encountered.

### Public evidence boundary

The public reproduction package is self-contained.

All executable material and exact artifact identities intentionally published for reproduction are derived from the domain-neutral synthetic fixture included in this repository. No private source file, private repository path, private revision, or private artifact fingerprint is required for public reproduction.

Earlier empirical observations are described only to the extent needed to motivate or evaluate the protocol boundary. The public fixture is the reference artifact for independent reproduction.

### Public reference fixture

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

### Current status

```text
protocol draft v0.1 = available
public synthetic fixture = available
public deterministic generator/verifier = available
public prior-art scan = available
independent LLM-host reproduction using the public fixture = open work
cross-host / cross-vendor portability = open work
production safety = not established
novelty claim = not established
```

Independent reproduction, counterexamples, closer prior art, and protocol-design criticism are welcome.

### AI assistance disclosure

This research and repository were developed with **extensive use of AI assistants**, primarily through general-purpose ChatGPT/LLM environments. AI assistance has been used for architecture and protocol exploration, hypothesis generation and critique, experiment planning, drafting/refactoring code and documentation, analysis support, prior-art search support, editing, translation, and repository preparation.

AI also appears separately as part of the runtime class being studied. These roles are kept distinct.

AI-generated text, code, or interpretation is **not treated as experimental evidence by itself**. Public claims are intended to remain grounded in inspectable artifacts, machine-checkable identities, reproducible execution results, negative controls, and cited public sources.

See [AI_ASSISTANCE.md](AI_ASSISTANCE.md).

### What is not claimed as new

This project does **not** claim invention of Base64, gzip, hashing, chunking, manifests, content addressing, reproducible execution, or software-supply-chain verification.

The research question is whether mature primitives can be composed into a useful protocol layer for an LLM-host boundary where exact executable identity must remain authoritative despite host/sandbox acquisition differences or representation normalization.

### Licensing

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
CITATION.cff
LICENSE
LICENSES/
NOTICE
```

Read more:

- [Preliminary Technical Report — English](reports/preliminary-report.en.md)
- [予備技術レポート — 日本語](reports/preliminary-report.ja.md)
- [Protocol Draft v0.1](spec/protocol-draft-v0.1.md)
- [Experiment / Reproduction Guide](experiments/README.md)
- [Public Reference Fixture](fixtures/README.md)
- [Prior-Art Scan](research/prior-art.md)
- [Research Roadmap](ROADMAP.md)

---

## 日本語

このRepositoryは、**Lossless Executable Materializationという1つのProtocol Candidate**に対象を絞った公開研究Repositoryです。

扱う問いは次です。

> LLM Hostが必要なdeterministic executableを識別できても、Execution Environmentにその正確なbytesが存在するとは限らない。では、authorizedなExecutableをlosslessにmaterializeし、local identityを証明してからだけ実行資格を与えるにはどうすればよいか。

Protocol Candidateでは次の責務を分離します。

```text
Executable Authority
-> Lossless Representation
-> Representation Acquisition
-> Deterministic Assembly
-> Mechanical Materialization
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

compileできる、動く、期待した結果が出る、というだけでは、Exact Identityが要求されるExecutableのauthorityを満たしたことにはしません。

### 公開範囲

このRepositoryでは、**Materialization Protocolそのものと、その評価に必要なEvidenceだけ**を扱います。

この問題が最初に発生した上位Application Architecture、Domain Implementation、Product、上流の研究体系全体を公開・解説することは目的にしません。

### 公開Evidenceの境界

第三者向けの再現Artifactは、このRepository内の**domain-neutral synthetic fixture**だけで完結させます。

公開再現のために、private source、private repository path、private revision、private artifact fingerprintは必要ありません。初期のempirical observationについては、Protocol境界を説明・評価するために必要な範囲だけを一般化して扱います。

### Public Reference Fixture

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

### 現在のStatus

```text
protocol draft v0.1 = available
public synthetic fixture = available
public deterministic generator/verifier = available
public prior-art scan = available
public fixtureを使ったindependent LLM-host reproduction = 今後の検証
cross-host / cross-vendor portability = 今後の検証
production safety = 未確立
novelty claim = 未確立
```

再現結果、反例、より近いPrior Art、Protocol設計上の批判を歓迎します。

### AI利用の開示

本研究およびRepository作成では、**AI Assistantを積極的かつ広範囲に使用しています**。Protocol/Architecture検討、仮説生成と反論、実験計画、code/documentのdraft・refactor、分析支援、prior-art探索支援、編集、翻訳、Repository整備などに利用しています。

一方、AI/LLMは研究支援とは別に、研究対象となるRuntime classの一部としても登場します。この2つの役割は区別します。

AI生成の文章・code・解釈そのものは、単独ではExperimental Evidenceとして扱いません。公開上の主張は、inspect可能なArtifact、machine-checkable identity、reproducible execution result、negative control、公開Sourceへ結び付けます。

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
- [Experiment / Reproduction Guide](experiments/README.md)
- [Public Reference Fixture](fixtures/README.md)
- [Prior-Art Scan](research/prior-art.md)
- [Research Roadmap](ROADMAP.md)
