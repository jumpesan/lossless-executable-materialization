# Lossless Executable Materialization

> Preliminary research on verifiable executable materialization across an LLM-host boundary.

**Author:** Jumpei Fujii (GitHub: [@jumpesan](https://github.com/jumpesan))

[日本語](#日本語) · [English](#english)

## English

This repository studies a protocol candidate for a specific runtime problem:

```text
structured Context
+ deterministic Scripts
+ general-purpose LLM host
+ user interaction
-> application-like runtime behavior
```

When deterministic behavior must be defined by an exact registered executable, semantic understanding is not enough. An LLM may understand what a program should do while the execution environment still lacks a trustworthy, byte-exact copy of the executable that is authorized to run.

The research therefore separates:

```text
Executable Authority
-> Lossless Representation
-> Host Observation / Acquisition
-> Deterministic Assembly
-> Mechanical Decode / Materialization
-> Identity Proof
-> Execution Eligibility
-> Deterministic Execution Evidence
```

The key invariant is:

```text
semantic or functional equivalence
!=
canonical executable identity
```

### Public evidence boundary

This public package is intentionally self-contained.

**All reproducible artifact identities and executable material published here are derived from the domain-neutral synthetic fixture included in this repository.** No external proprietary executable, private-project source file, private repository path, private revision, or private artifact fingerprint is required to reproduce the public materialization flow.

Public claims should be grounded only in artifacts and experiments that can be reproduced from this repository or in clearly cited public prior art.

### Public reference fixture

The repository includes a synthetic executable fixture designed only to exercise the materialization boundary:

```bash
python fixtures/verify_reference_fixture.py
```

The verifier performs:

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

The fixture is generated deterministically and has fixed public identities. See [fixtures/README.md](fixtures/README.md).

### Current research status

The public repository currently establishes a **reproducible reference implementation and protocol draft**, not a universal LLM-host result.

```text
public synthetic fixture / deterministic generation = available
public local identity/materialization verifier = available
protocol draft v0.1 = available
public prior-art scan = available
fresh LLM-host black-box reproduction on the public fixture = open work
cross-host / cross-vendor portability = open work
production safety = not established
novelty claim = not established
```

Independent reproduction, failure reports, closer prior art, and protocol criticism are welcome.

### AI assistance disclosure

This research and repository were developed with **extensive use of AI assistants**, primarily through general-purpose ChatGPT/LLM environments. AI assistance has been used for architecture exploration, hypothesis generation and critique, experiment planning, drafting/refactoring code and documentation, analysis support, prior-art search support, editing, translation, and repository preparation.

AI also appears separately as part of the runtime class being studied. These two roles are kept distinct.

AI-generated text, code, or interpretation is **not treated as experimental evidence by itself**. Public claims are intended to remain grounded in inspectable artifacts, machine-checkable identities, reproducible execution results, negative controls, and cited public sources. Human responsibility for research direction, evidence acceptance, interpretation, and publication remains explicit.

See [AI_ASSISTANCE.md](AI_ASSISTANCE.md).

### What is not claimed as new

This project does **not** claim invention of Base64, gzip, hashing, chunking, manifests, content addressing, reproducible execution, or software-supply-chain verification. Strong prior art exists in OCI, TUF, SRI, Nix, content-addressed systems, MCP resources, software-supply-chain frameworks, and related mechanisms.

The research question is whether mature primitives can be composed into a useful protocol layer for environments where:

```text
host-visible representations may be transformed or normalized
+
execution environments may have different acquisition capabilities
+
exact executable identity is still required before authoritative execution
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

See [LICENSE](LICENSE) for exact scope and [LICENSES/](LICENSES/) for license text/notices.

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

.github/ISSUE_TEMPLATE/
  reproduction.yml
  prior-art.yml
  protocol-feedback.yml

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

このRepositoryは、汎用LLM HostをApplication-like Runtimeとして利用する際に生じる、**正確なExecutable Materialization**の問題を研究する公開Repositoryです。

想定する構造は次の通りです。

```text
構造化Context
+ deterministic Scripts
+ 汎用LLM Host
+ User Interaction
-> Application-like Runtime Behavior
```

LLMが「どのProgramを使うべきか」を理解していても、そのProgramの正確なbytesがExecution Environment内に存在し、かつ実行を許可されたCanonical Executableと同一であるとは限りません。

そこで本研究では次の責務を分離します。

```text
Executable Authority
-> Lossless Representation
-> Host Observation / Acquisition
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

### 公開Evidenceの境界

この公開Packageは**単独で再現できること**を前提にしています。

公開するExecutable Material、hash、content identity、再現手順は、すべてこのRepository内で生成した**domain-neutralなsynthetic fixture**を正本とします。外部の非公開実装、非公開Repository path、private revision、private artifact fingerprintを公開再現の前提にはしません。

公開上の主張は、このRepositoryだけから再現できるArtifact/Experiment、または明示的に引用した公開Prior Artへ限定します。

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

### 現在の公開研究Status

現在の公開版で確立しているのは、**再現可能なSynthetic Reference Fixture、Verifier、Protocol Draft**です。

```text
public synthetic fixture / deterministic generation = available
public local identity/materialization verifier = available
protocol draft v0.1 = available
public prior-art scan = available
public fixtureを使ったfresh LLM-host black-box reproduction = 今後の検証
cross-host / cross-vendor portability = 今後の検証
production safety = 未確立
novelty claim = 未確立
```

再現結果、失敗例、より近いPrior Art、Protocol設計上の反論を歓迎します。

### AI利用の開示

本研究およびRepository作成では、**AI Assistantを積極的かつ広範囲に使用しています**。Architecture検討、仮説生成と反論、実験計画、code/documentのdraft・refactor、分析支援、prior-art探索支援、編集、翻訳、Repository整備などに利用しています。

一方、AI/LLMは研究支援とは別に、研究対象となるRuntime classの一部としても登場します。この2つの役割は区別します。

AI生成の文章・code・解釈そのものは、単独ではExperimental Evidenceとして扱いません。公開上の主張は、inspect可能なArtifact、machine-checkable identity、reproducible execution result、negative control、公開Sourceへ結び付けます。研究方向、Evidence採否、解釈、公開内容の責任はHuman Researcherが持ちます。

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
