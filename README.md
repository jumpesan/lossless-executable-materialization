# Lossless Executable Materialization

> Preliminary research on verifiable executable materialization across an LLM-host boundary.

**Author:** Jumpei Fujii (GitHub: [@jumpesan](https://github.com/jumpesan))

[日本語](#日本語) · [English](#english)

## English

This repository is the public research workspace for a protocol candidate that emerged while exploring a broader architecture idea:

```text
structured Context
+ deterministic Scripts
+ general-purpose ChatGPT / LLM host
+ user interaction
-> application-like runtime behavior
```

The original goal was not to invent a transport protocol. The problem appeared after the LLM could determine **which deterministic executable should run**, while the host-provided sandbox could not reliably obtain the exact registered executable bytes from a fresh public resource.

A critical black-box counterexample then showed that human-readable source can be semantically preserved while byte identity is lost:

```text
functional behavior = PASS
all nonblank lines preserved = PASS
33 blank lines removed
SHA-256 / Git blob identity = FAIL
```

This led to a different question:

> Can an LLM host transport a lossless representation, mechanically materialize the exact canonical bytes in a sandbox, prove content identity, and only then make the artifact eligible for authoritative deterministic execution?

### Current candidate flow

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

The current experiments have demonstrated exact recovery for one executable using both plain chunked Base64 and deterministic gzip + Base64. GPT-5.6 Instant and High both produced exact plain-Base64 materializations in fresh Temporary Chats. A deterministic gzip + Base64 profile also produced an exact Instant materialization while reducing the tested transport representation from 26,076 characters / 7 chunks to 5,480 characters / 2 chunks (~79% fewer transport characters).

Several fail-closed controls have also passed for the current sample, including missing operands, counterintuitive declared chunk order, one-character payload corruption, final identity mismatch, unregistered near-identical executable identity, and explicit semantic-repair temptation after terminal failure.

These results are **sample-scoped preliminary evidence**, not a production guarantee or novelty proof.

### Public reference fixture

To make the repository reproducible without access to the private implementation project that originally exposed the problem, this repository includes a **domain-neutral synthetic executable fixture** with a deterministic gzip + Base64 representation, descriptor, generator, and verifier.

```bash
python fixtures/verify_reference_fixture.py
```

The published fixture independently exercises ordered chunk acquisition, strict decode, compressed identity, decompression, final canonical identity, compile, deterministic execution, and structured output. Its artifact identities are fixed and self-checked by the generator. See [fixtures/README.md](fixtures/README.md).

### AI assistance disclosure

This research and repository were developed with **extensive use of AI assistants**, primarily through general-purpose ChatGPT/LLM environments. AI assistance has been used for architecture exploration, hypothesis generation and critique, experiment planning, drafting/refactoring code and documentation, analysis support, prior-art search support, editing, translation, and repository preparation.

AI also appears separately as part of the experimental runtime/host being studied. These two roles should not be conflated.

AI-generated text, code, or interpretation is **not treated as experimental evidence by itself**. Claims are intended to remain grounded in inspectable artifacts, cryptographic identities, machine execution results, structured outputs, negative controls, and black-box observations. Human responsibility for research direction, evidence acceptance, interpretation, and publication remains explicit.

See [AI_ASSISTANCE.md](AI_ASSISTANCE.md) for the full disclosure.

### What is not claimed as new

This project does **not** claim invention of Base64, gzip, hashing, chunking, manifests, content addressing, reproducible execution, or software-supply-chain verification. Strong prior art exists in OCI, TUF, SRI, Nix, BitTorrent/IPFS/IPLD, MCP resources, Agent Skills, in-toto/SLSA/Sigstore, and adjacent execution-integrity work.

The research question is whether those mature primitives form a useful protocol layer for a specific LLM-host boundary:

```text
semantic / human-readable observation may normalize representation
+
execution sandbox may not share host retrieval capability
+
exact registered executable identity is still required
```

### Licensing

This repository uses split licensing so research knowledge and executable material can both be reused under licenses suited to their role:

```text
documentation / reports / prose specifications / research notes
-> CC BY 4.0

source code / scripts / CI / machine-readable examples /
executable fixtures / generated materialization artifacts
-> Apache-2.0
```

See [LICENSE](LICENSE) for the exact scope and [LICENSES/](LICENSES/) for the license notices/text.

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
PUBLICATION_CHECKLIST.md
CITATION.cff
LICENSE
LICENSES/
NOTICE
```

### Status

```text
research_stage = preliminary / active
protocol_status = candidate / not standardized
production_status = not established
novelty_claim = not established
repository_visibility = private during preparation
```

Read the full report:

- [Preliminary Technical Report — English](reports/preliminary-report.en.md)
- [予備技術レポート — 日本語](reports/preliminary-report.ja.md)

Protocol and research artifacts:

- [Protocol Draft v0.1](spec/protocol-draft-v0.1.md)
- [Illustrative Descriptor](spec/descriptor-example.json)
- [Draft Failure Codes](spec/failure-codes.md)
- [Experiment Matrix](experiments/README.md)
- [Public Reference Fixture](fixtures/README.md)
- [AI Assistance Disclosure](AI_ASSISTANCE.md)
- [Prior-Art Scan](research/prior-art.md)
- [Research Roadmap](ROADMAP.md)

We welcome reproduction results, counterexamples, prior art, cross-model/host tests, and protocol-design criticism. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 日本語

このRepositoryは、次のArchitectureを検証する過程で生じた研究を外部共有するための公開準備用Repositoryです。

```text
構造化Context
+ deterministic Scripts
+ 汎用ChatGPT / LLM Host
+ User Interaction
-> Application-like Runtime Behavior
```

元々の目的はTransport Protocolを作ることではありませんでした。LLMが「どのdeterministic executableを使うべきか」を判断できるようになった一方で、Hostが提供するSandboxへ、その**登録済みExecutableの正確なbytes**を安定して持ち込めない問題が発生しました。

さらにblack-box testでは、人間向けに読めるPython Sourceを再構成した際、機能的には完全に動作する一方で33行の空行だけが失われ、SHA-256 / Git blob identityが一致しない反例が得られました。

```text
意味が同じ
!=
正本Executableと同一
```

そこで、SourceをLLMに再生成させるのではなく、losslessなRepresentationをHost越しに取得し、Sandbox内でmechanicalにdecode/materializeし、Canonical Identityを証明してから実行資格を与える方式へ研究対象を変更しました。

現在は、plain chunked Base64でGPT-5.6 Instant / Highのfresh Temporary Chat exact PASS、さらにdeterministic gzip + Base64でInstant exact PASSを観測しています。gzip profileでは同一19,555-byte executableに対し、26,076文字 / 7 chunkから5,480文字 / 2 chunkへ約79%のtransport文字削減も確認しています。

加えて、missing operand、宣言順序の逆転、1文字corruption、final identity mismatch、未登録の近似Executable、失敗後に正解のrepair候補を明示的に見せるsemantic temptationなど、複数のfail-closed controlが現在のsampleでPASSしています。

### 公開用Reference Fixture

元の非公開実装Projectを知らなくても第三者がMaterialization手順を確認できるように、domain-neutralなsynthetic executable fixtureを同梱しています。

```bash
python fixtures/verify_reference_fixture.py
```

このFixtureは、ordered chunk acquisition、strict decode、compressed identity、decompression、final canonical identity、compile、deterministic execution、structured outputまでRepository単体で検証できます。詳細は [fixtures/README.md](fixtures/README.md) を参照してください。

### AI利用の開示

この研究およびRepositoryの作成では、**AI Assistantを積極的かつ広範囲に使用しています**。主に汎用ChatGPT/LLM環境を用い、Architecture検討、仮説生成と反論、実験計画、code/documentのdraft・refactor、実験結果の分析支援、prior-art探索支援、編集、翻訳、公開Repository整備などに利用しています。

またAI/LLMは、研究支援とは別に、実験対象となるRuntime/Hostの一部としても登場します。この2つの役割は区別して扱います。

AIが生成した文章・code・解釈そのものは、**単独ではExperimental Evidenceとして扱いません**。主張は、Artifact、cryptographic identity、machine execution result、structured output、negative control、black-box observationなど検証可能なEvidenceへ結び付けます。研究方向、Evidenceの採否、解釈、公開内容についてはHuman Researcherが責任を持ちます。

詳細は [AI_ASSISTANCE.md](AI_ASSISTANCE.md) に明記しています。

### ライセンス

本Repositoryは用途に合わせたsplit licensingを採用しています。

```text
研究文書 / Technical Report / 文章によるSpecification / Research Note
-> CC BY 4.0

Source Code / Script / CI / Machine-readable Example /
Executable Fixture / Generated Materialization Artifact
-> Apache-2.0
```

適用範囲の詳細は [LICENSE](LICENSE)、各Licenseの表記・本文は [LICENSES/](LICENSES/) を参照してください。

ただし、これはまだ**Protocol Candidate**です。Production Safetyや一般的新規性を主張する段階ではありません。

- [日本語 予備技術レポート](reports/preliminary-report.ja.md)
- [English Preliminary Technical Report](reports/preliminary-report.en.md)
- [Protocol Draft v0.1](spec/protocol-draft-v0.1.md)
- [Experiment Matrix](experiments/README.md)
- [Public Reference Fixture](fixtures/README.md)
- [AI利用の開示](AI_ASSISTANCE.md)
- [Prior-Art Scan](research/prior-art.md)
- [Research Roadmap](ROADMAP.md)

再現結果、失敗例、類似技術、別Model / 別Hostでの結果、設計上の反論も歓迎します。
