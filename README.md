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

It does not attempt to publish the broader application architecture or domain implementation from which the problem was first encountered. The application domain is not required to understand or reproduce the protocol.

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
RELEASE_NOTES.md
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
- [v0.1-preliminary Release Notes](RELEASE_NOTES.md)

Independent reproduction, counterexamples, closer prior art, cross-model/host tests, and protocol-design criticism are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 日本語

このリポジトリは、実際のLLMホスト型アプリケーション開発中に発生した **Lossless Executable Materialization**（損失のない実行ファイル実体化）という1つの**プロトコル候補**を扱う公開研究リポジトリです。

扱う問いは次です。

> LLMが「どの決定論的な実行ファイルを実行すべきか」を判断できても、実行環境にその登録済み実行ファイルの正確なバイト列が存在するとは限らない。では、その実行ファイルを損失なく実体化し、ローカルで正本との同一性を証明してからだけ実行資格を与えるにはどうすればよいか。

初期のブラックボックス試験では、人間可読なPythonソースを再構成した際、非空行はすべて一致し、コンパイル・実行・構造化結果もPASSした一方で、33行の空行が失われ、SHA-256 / Git blobによる同一性検証がFAILする反例が得られました。

```text
意味・機能が同じ
!=
正本の実行ファイルと同一
```

この結果から、ソース再構成ではなく **Lossless Executable Materialization** をプロトコルとして扱う方向へ進みました。

### プロトコル候補

仕様上の概念名は英語表記を維持しますが、日本語ではおおむね次の意味です。

```text
Executable Authority        実行ファイルの認可
-> Lossless Representation  損失のない表現
-> Representation Acquisition 表現の取得
-> Deterministic Assembly    決定論的な組み立て
-> Mechanical Decode / Materialization 機械的な復号・実体化
-> Identity Proof            同一性の証明
-> Execution Eligibility     実行資格
-> Deterministic Execution Evidence 決定論的実行の証拠
```

中心となる不変条件は次です。

```text
意味的・機能的な同等性
!=
正本実行ファイルとの同一性
```

### 現在の実証結果

現在は、**2つの異なる登録済み単一ファイル実行物**で完全一致の実体化を確認しています。

主要な試料では:

```text
plain chunked Base64 / GPT-5.6 Instant = EXACT PASS
plain chunked Base64 / GPT-5.6 High    = EXACT PASS
deterministic gzip + Base64 / GPT-5.6 Instant = EXACT PASS
```

決定論的gzip + Base64方式では、同一試料の転送表現を

```text
26076文字 / 7チャンク
->
5480文字 / 2チャンク
```

へ削減し、約79%の転送文字数削減を確認しました。

さらに2つ目の登録済み実行ファイルでも、GPT-5.6 Instantによるブラックボックスでの完全一致実体化がPASSしています。

フェイルクローズ（失敗時は安全側に拒否する）制御では、宣言済みオペランドの欠落、直感に反するチャンク順序、1文字のペイロード破損、最終的な正本同一性の不一致、未登録の近似実行ファイル、終端失敗後の意味的修復への明示的な誘惑を検証しています。

ファイルシステムについても代表的なF0-F4がPASSしており、シンボリックリンク、ルート外への逸脱、既存の最終ターゲット、失敗後のステージング残留物を拒否できています。また、既存ターゲットが正本バイト列と完全一致していても、それを暗黙のキャッシュヒットや再利用権限へ昇格しないことを推論圧力テストで確認しています。

依存関係を含む実行単位の検証は次の検証対象であり、**まだPASSには数えていません**。

これらは現在の試料に限定した予備的な実証結果であり、本番運用の安全性や一般的な新規性を主張するものではありません。

### 公開用参照フィクスチャ

アプリケーションの分野に依存せず第三者が実体化手順を確認できるように、分野非依存の合成実行フィクスチャも同梱しています。

```bash
python fixtures/verify_reference_fixture.py
```

検証器は次を機械的に確認します。

```text
宣言順にオペランドを取得
-> 厳密なBase64復号
-> 圧縮データの同一性検証
-> 決定論的なgzip展開
-> 正本との同一性検証
-> コンパイル
-> 決定論的な実行
-> 構造化結果の検証
```

詳細は [fixtures/README.md](fixtures/README.md) を参照してください。

### 公開範囲

このリポジトリでは、**Lossless Executable Materializationプロトコルそのものと、その評価に必要な実証結果**に対象を絞ります。

問題が最初に発生したアプリケーション全体のアーキテクチャや分野固有の実装を公開・解説することは目的にしません。元のアプリケーション分野を知らなくても、このプロトコルは理解・再現できる構成にします。

### AI利用の開示

本研究およびリポジトリ作成では、**AIアシスタントを積極的かつ広範囲に使用しています**。プロトコル/アーキテクチャ検討、仮説生成と反論、実験計画、コード・文書の下書きやリファクタリング、分析支援、先行技術調査支援、編集、翻訳、リポジトリ整備などに利用しています。

またAI/LLMは、研究支援とは別に、実験対象となる実行環境/ホストの一部としても登場します。この2つの役割は区別します。

AI生成の文章・コード・解釈そのものは、単独では実験的証拠として扱いません。主張は、検査可能な成果物、暗号学的な同一性情報、機械実行結果、構造化出力、否定系制御、ブラックボックス観測などの検証可能な証拠へ結び付けます。研究方向、証拠の採否、解釈、公開内容については人間の研究者が責任を持ちます。

詳細は [AI_ASSISTANCE.md](AI_ASSISTANCE.md) を参照してください。

### ライセンス

```text
研究文書 / 技術レポート / 文章による仕様 / 研究ノート
-> CC BY 4.0

ソースコード / スクリプト / CI / 機械可読な例 /
実行フィクスチャ / 生成された実体化成果物
-> Apache-2.0
```

適用範囲は [LICENSE](LICENSE)、正式なライセンス本文は [LICENSES/](LICENSES/) を参照してください。

- [日本語 予備技術レポート](reports/preliminary-report.ja.md)
- [英語 予備技術レポート](reports/preliminary-report.en.md)
- [プロトコル草案 v0.1](spec/protocol-draft-v0.1.md)
- [実験一覧](experiments/README.md)
- [公開用参照フィクスチャ](fixtures/README.md)
- [先行技術調査](research/prior-art.md)
- [研究ロードマップ](ROADMAP.md)
- [v0.1-preliminary リリースノート](RELEASE_NOTES.md)