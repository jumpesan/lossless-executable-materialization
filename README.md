# Lossless Executable Materialization

> Preliminary research on verifiable executable materialization across an LLM-host boundary.

**Author:** Jumpei Fujii (GitHub: [@jumpesan](https://github.com/jumpesan))

[日本語](#日本語) · [English](#english)

## English

This repository focuses on a protocol candidate that emerged from real LLM-hosted application development:

> How can an LLM-hosted runtime obtain the exact executable bytes that are authorized to run, prove that identity locally, and fail closed when exact materialization cannot be established?

The problem appeared after the LLM could determine **which deterministic executable should run**, while the host-provided execution environment could not reliably obtain the exact registered executable bytes.

A critical black-box counterexample showed that human-readable source can preserve meaning and behavior while losing byte identity:

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
-> Materialization Descriptor / Trusted Binding
-> Lossless Representation
-> Representation Acquisition
-> Execution-Surface Transfer (where required)
-> Deterministic Assembly
-> Mechanical Decode / Materialization
-> Exact Identity Proof
-> Filesystem / Workspace Preconditions
-> Execution Eligibility
-> Owner Invocation Eligibility
-> Process / Structured Evidence
```

The central invariant is:

```text
semantic or functional equivalence
!=
canonical executable identity
```

A program that compiles, runs, and produces the expected result is still not treated as the authoritative executable when exact identity is required but unproven.

### Current empirical evidence

The evidence base has moved substantially beyond the initial feasibility experiments.

Observed black-box / artifact-shape controls now include:

```text
P1 primary executable / plain Base64 + gzip/Base64 = PASS
P2 second registered executable = PASS
P3 Unicode + mixed CRLF/LF exact-byte preservation = PASS
P4 larger 13,239-byte / three-chunk materialization = PASS
D2-D6 multi-file dependency / DATA_REFERENCE controls = PASS
U1-U5 USER_DATA separation controls = PASS
N1-N7 representative fail-closed controls = PASS (N4 intentionally skipped)
H1 external resource visible -> sandbox-local handoff = BLOCKED / observed
H2 local attachment-plane canonical execution = PASS / Instant + High
H3 large monolithic caller-context relay = FAIL / route drift
H4 small chunked caller-context literal relay = PASS
```

The original primary gzip + Base64 profile reduced the tested transport representation from:

```text
26076 characters / 7 chunks
->
5480 characters / 2 chunks
```

or approximately **79% fewer transport characters** for that sample.

P4 later confirmed exact ordered materialization across three chunks:

```text
canonical size = 13239 bytes
encoded length = 9780 characters
chunk lengths = 4096 / 4096 / 1588
strict Base64 decode count = 1
gzip decompression count = 1
canonical identity = PASS
binary reread exact = true
execution_eligible = true
```

### Host-surface transfer boundary

Later trusted-host integration exposed a second boundary beyond representation fidelity:

```text
resource observable by the host
!=
exact operands available in caller/model context
!=
exact bytes available to the execution surface
```

Representative application-derived, domain-neutral observations now include:

```text
external transport observed through the host Web surface
-> exact handoff into the execution sandbox = BLOCKED

the same execution capsule available on the local attachment plane
-> exact canonical execution = PASS / Instant + High

one large caller-context staging object
-> exact scalar relay not established
-> sandbox refetch fallback attempted
-> FAIL

8 small exact caller-context chunks
-> literal transfer into sandbox
-> exact capsule reconstruction
-> canonical execution = PASS
```

For the positive small-chunk sample:

```text
chunk count = 8
chunk length = 1368 characters each
concatenated encoded length = 10944
decoded capsule size = 8207 bytes
exact capsule identity = PASS
canonical execution = PASS
```

The H4 verdict uses convergent evidence from two runs against the same immutable candidate because the host Activity UI did not expose one complete end-to-end trace. It therefore establishes a **bounded relay primitive** for the observed host/model surface, not generic application-wide transport or cross-host portability.

Transport granularity is treated as a host-surface transport parameter. It does not create executable authority and does not belong to application/domain semantics.

This repository still does not expand into application bootstrap, application-state ownership, or user-interface behavior; those remain outside the Lossless Executable Materialization scope.

See [2026-08-30 Host-Surface Relay Update](experiments/2026-08-30-host-surface-relay-update.md).

### Machine-enforced path

The research also moved from LLM-observed procedure into a deterministic machine path.

Representative validated components now include:

```text
descriptor schema / structural validation
non-authorizing machine preflight
historical positive/negative descriptor regression
external immutable authority binding
deterministic representation acquisition/materialization
exact canonical Git-object convergence
single-member cache/reuse contract
execution-handoff separation
generic fixed-file validator operation
F0-F8 workspace hardening across POSIX/Windows
non-authorizing trusted runtime binding
self-hosted immutable-revision descriptor resolution
```

The trusted path keeps the following separation explicit:

```text
schema/preflight PASS
!= executable authority

materialization PASS
!= owner invocation eligibility
!= process success
!= domain semantic success
```

The deterministic materializer does not use semantic LLM reconstruction, repair, alternate-representation search, or functional plausibility to override failed exact gates.

### Filesystem and cache boundary

Representative F0-F8 workspace controls now pass for the tested implementation, including repeated/concurrent attempt isolation, tamper/replacement detection, monotonic TAINTED cleanup-failure state, and explicit POSIX/Windows behavior.

Cache/reuse is also explicit rather than inferred from local byte equality:

```text
raw cache = non-authorizing exact byte store
current authority must be re-resolved
cached bytes must be reverified
only trusted orchestration may restore execution_eligible=true
```

Mixed execution-unit cache orchestration remains open.

### What is still open

These results are **sample-scoped research evidence**, not a universal production guarantee or novelty proof.

Important remaining work includes:

```text
cross-host / cross-vendor reproduction
independent third-party machine-path reproduction
dependency cycle/duplicate edge semantics
mixed-unit cache semantics
remaining transport-normalization/boundary cases
generic cross-unit execution-surface relay and full trusted-host end-to-end integration
broader OS/process sandbox and resource isolation
public schema/interface stabilization
```

Live/runtime promotion and final release remain separate authorization decisions from protocol validation.

### Public reference fixture

The repository includes a domain-neutral synthetic executable fixture so the basic materialization flow can be reproduced without depending on the application domain that originally exposed the problem.

```bash
python fixtures/verify_reference_fixture.py
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

The research question is whether mature primitives can form a useful protocol layer for an LLM-host boundary where:

```text
host-visible representations may be normalized or transformed
+
host-observed exact data may not be transferable into the execution surface
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
  2026-08-19-validation-update.md
  2026-08-30-host-surface-relay-update.md

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
- [2026-08-19 Validation Update](experiments/2026-08-19-validation-update.md)
- [2026-08-30 Host-Surface Relay Update](experiments/2026-08-30-host-surface-relay-update.md)
- [Public Reference Fixture](fixtures/README.md)
- [AI Assistance Disclosure](AI_ASSISTANCE.md)
- [Prior-Art Scan](research/prior-art.md)
- [Research Roadmap](ROADMAP.md)
- [v0.1-preliminary Release Notes](RELEASE_NOTES.md)

The `v0.1-preliminary` release/tag is a fixed historical snapshot; later evidence is tracked on `main`.

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

```text
Executable Authority              実行ファイルの認可
-> Materialization Descriptor     実体化記述子
-> Trusted Binding                信頼された選択・結び付け
-> Lossless Representation        損失のない転送表現
-> Representation Acquisition     表現の取得
-> Execution-Surface Transfer     実行Surfaceへの転送（必要な場合）
-> Deterministic Assembly         決定論的な組み立て
-> Mechanical Materialization     機械的な実体化
-> Exact Identity Proof           完全同一性の証明
-> Workspace Preconditions        作業領域の前提条件
-> Execution Eligibility          実行資格
-> Owner Invocation Eligibility   所有側呼び出し資格
-> Process / Structured Evidence  プロセス・構造化証拠
```

中心となる不変条件は次です。

```text
意味的・機能的な同等性
!=
正本実行ファイルとの同一性
```

### 現在の実証結果

現在は初期のBase64実験を越えて、次の代表系まで進んでいます。

```text
P1 主要実行物 = PASS
P2 2つ目の登録済み実行物 = PASS
P3 Unicode + CRLF/LF混在の完全バイト保持 = PASS
P4 13,239バイト / 3チャンクの実体化 = PASS
D2-D6 複数ファイル依存関係 / DATA_REFERENCE境界 = PASS
U1-U5 USER_DATA境界 = PASS
N1-N7 代表的fail-closed制御 = PASS（N4は意図的skip）
H1 外部resource観測 -> sandbox-local handoff = BLOCKED / 観測済み
H2 local attachment planeでのcanonical execution = PASS / Instant + High
H3 大きな単一caller-context relay = FAIL / route drift
H4 小チャンクcaller-context literal relay = PASS
```

主要試料では決定論的gzip + Base64によって、転送表現を

```text
26076文字 / 7チャンク
->
5480文字 / 2チャンク
```

へ削減しました。

P4では3チャンクについて、全チャンクの個別同一性確認後に宣言順で1回だけ結合し、Base64復号1回、gzip展開1回、正本同一性確認、binary rereadまで完全一致しています。

### Host Surface間の転送境界

その後のtrusted-host統合では、表現忠実性とは別に、LLM Host内部のSurface間転送という境界が観測された。

```text
Hostがresourceを観測できる
!=
caller/model Contextでexact operandを利用できる
!=
execution sandboxでexact bytesを利用できる
```

分野固有情報を除いた代表的な観測は次のとおり。

```text
外部transportをHost Web surfaceで観測
-> execution sandboxへのexact handoff = BLOCKED

同じexecution capsuleをlocal attachment planeに配置
-> exact canonical execution = PASS / Instant + High

大きな単一caller-context staging object
-> exact scalar relayを確立できず
-> sandbox refetchへfallback
-> FAIL

8個の小さいexact chunk
-> caller Contextからsandboxへliteral転送
-> exact capsule再構成
-> canonical execution = PASS
```

小チャンク正常系では、

```text
chunk数 = 8
各chunk = 1368文字
結合後encoded length = 10944
decoded capsule = 8207バイト
capsule exact identity = PASS
canonical execution = PASS
```

を確認した。H4は、HostのActivity UIが単一runの完全なend-to-end traceを表示しなかったため、同じimmutable candidateに対する2回の収束したEvidenceを組み合わせて判定している。このため主張範囲は、観測したHost/model surfaceにおける**限定されたrelay primitiveの成立**までであり、application-wideな汎用transportやcross-host portabilityまでは含まない。

chunk granularityはHost surfaceのtransport parameterとして扱い、実行ファイルの認可やApplication Domain semanticsを生成しない。

本公開Repoは引き続きApplication bootstrap、Application state ownership、UI/UX挙動そのものは対象外とする。

詳細: [2026-08-30 Host-Surface Relay Update](experiments/2026-08-30-host-surface-relay-update.md)

### Machine実装への移行

現在は「LLMが手順を守れるか」という観測だけではなく、機械的に強制する経路まで進んでいます。

代表的に確認済みなのは次です。

```text
記述子schema / 構造検証
非認可のmachine preflight
過去descriptorのpositive/negative回帰
外部immutable authority binding
決定論的representation取得・実体化
canonical Git objectとの完全一致
単一member cache/reuse Contract
Execution Handoff分離
固定USER_DATAファイルを使うgeneric validator operation
F0-F8 workspace hardening（POSIX/Windows）
非認可のtrusted runtime binding
self-hosted immutable revision descriptor解決
```

ここでも、

```text
schema/preflight PASS
!= 実行ファイルの認可

materialization PASS
!= owner invocation eligibility
!= process success
!= domain semantic success
```

を維持します。

決定論的materializerは、失敗したexact gateをLLMによる意味的修復・推測・別representation探索・「動きそうだから」という判断で上書きしません。

### Filesystem / Cache

F0-F8の代表的workspace制御は、繰り返し/同時attemptの分離、内容改変・ファイル置換・ancestor/root置換の検知、cleanup failure時の単調な`TAINTED`状態、POSIX/Windows双方のmachine evidenceまでPASSしています。

Cache/reuseも既存fileの一致から暗黙に推論せず、明示的なContractになっています。

```text
raw cache = 認可を持たないexact byte store
current authorityを毎回再確認
cache bytesを再検証
trusted orchestrationだけが再検証後にexecution_eligible=trueを復元可能
```

複数memberを含むcache orchestrationはまだ未完です。

### まだ未完了のもの

現在の結果は**試料・実装範囲に限定した研究Evidence**であり、普遍的なProduction保証や新規性証明ではありません。

主な残りは次です。

```text
cross-host / cross-vendor再現
第三者によるmachine path再現
dependency cycle/duplicate edge
mixed-unit cache
transport normalization / boundary edge
generic cross-unit execution-surface relay + trusted-host全体のend-to-end統合
OS/process sandbox・resource isolation
公開schema/interfaceの安定化
```

Runtime live promotionやfinal releaseは、Protocol検証とは別の認可判断です。

### 公開用参照フィクスチャ

アプリケーション分野に依存せず第三者が基本的な実体化手順を確認できるよう、分野非依存の合成実行フィクスチャも同梱しています。

```bash
python fixtures/verify_reference_fixture.py
```

詳細は [fixtures/README.md](fixtures/README.md) を参照してください。

### 公開範囲

このリポジトリでは、**Lossless Executable Materializationプロトコルそのものと、その評価に必要な実証結果**に対象を絞ります。

問題が最初に発生したアプリケーション全体のアーキテクチャや分野固有の実装を公開・解説することは目的にしません。

### AI利用の開示

本研究およびリポジトリ作成では、AIアシスタントを積極的かつ広範囲に使用しています。プロトコル/アーキテクチャ検討、仮説生成と反論、実験計画、コード・文書作成、分析、調査支援、編集・翻訳などに利用しています。

一方でAI/LLMは、研究支援とは別に実験対象となるホスト/実行環境の一部でもあります。この2つの役割は区別します。

AI生成物そのものは単独では実験的証拠として扱わず、検査可能なartifact、暗号学的identity、machine execution、structured output、negative control、black-box observationへ結び付けます。

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
- [2026-08-19 Validation Update](experiments/2026-08-19-validation-update.md)
- [2026-08-30 Host-Surface Relay Update](experiments/2026-08-30-host-surface-relay-update.md)
- [公開用参照フィクスチャ](fixtures/README.md)
- [先行技術調査](research/prior-art.md)
- [研究ロードマップ](ROADMAP.md)
- [v0.1-preliminary リリースノート](RELEASE_NOTES.md)

`v0.1-preliminary`タグは固定された過去スナップショットであり、その後のEvidenceは`main`で更新します。