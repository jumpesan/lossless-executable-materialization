# 予備技術レポート
# LLMホスト境界を越えるLossless Executable Materialization

> Lossless Executable Materialization: 損失のない実行ファイル実体化

## 状態

```text
created: 2026-08-18
report_type: public-facing preliminary technical report / Japanese edition
research_stage: feasibility established for observed samples
protocol_status: candidate / not standardized
production_status: not established
novelty_claim: not established
```

**著者:** Jumpei Fujii  
**公開ライセンス:** CC BY 4.0  
**AI利用:** 広範囲。詳細は [AI_ASSISTANCE.md](../AI_ASSISTANCE.md)

> **履歴スナップショット注記:** 本予備レポートは初回公開時点付近のEvidenceを記述している。その後のmachine pathおよびHost-surface relayのEvidenceは、`main`の[現在のREADME](../README.md)、[2026-08-19 validation update](../experiments/2026-08-19-validation-update.md)、[2026-08-30 host-surface relay update](../experiments/2026-08-30-host-surface-relay-update.md)で追跡する。本レポート後半の「未確立」項目は、この履歴時点の記述として読む必要がある。

---

# 概要

本レポートは、**構造化されたコンテキストと決定論的なスクリプトを組み合わせることで、汎用ChatGPT/LLM環境そのものをアプリケーション実行環境のように振る舞わせられるか**を検討する過程で生じた、実証的な技術調査について報告する。

この研究は当初、転送プロトコルを作ることを目的として始まったものではない。元々の目的は、従来型の専用アプリケーション実行環境をあらかじめ構築する代わりに、構造化コンテキスト、ユーザー操作、決定論的な実行機能、そして汎用LLMホスト自体を組み合わせることで、アプリケーションのような振る舞いを成立させられるかを確かめることだった。

その過程で、LLMは「どの決定論的な実行ファイルを使うべきか」を理解できるようになった一方、実行サンドボックスは新規の公開リソースから、その登録済み実装の正確なバイト列を安定して取得できなかった。ここから、より深い実行環境上の問題が露出した。

**どのプログラムを実行すべきか理解することと、実際に実行を許可されている正本のプログラムバイト列を実体化することは別問題である。**

初期のソース完全一致再実体化実験は有望に見えた。しかし、その後の新規Temporary ChatでPython実行ファイルを再構成したところ、非空行はすべて再現され、機能的にも正しい出力を得られた一方で、33行の空行が黙って削除された。生成物はコンパイルにも実行にも成功したが、SHA-256およびGit blobによる同一性は正本ソースと一致しなかった。

```text
semantic equivalence
!=
canonical executable identity
```

この結果、問題設定はソースコード再構成から、**LLMホスト境界における表現忠実性**へと再定義された。

次に、損失のないエージェント向け表現を検証した。正本実行ファイルのバイト列をASCII転送形式へ符号化し、宣言された順序のチャンクへ分割し、LLMホストの通常のWeb観測経路から取得した後、サンドボックス内で機械的に再構成し、正本との内容同一性を証明してから実行資格を与える方式を試した。

平文の分割Base64では、GPT-5.6 InstantとGPT-5.6 Highを用いた新規Temporary Chatの双方で、同一の19,555バイトの正本実行ファイルを完全一致で復元した。さらに決定論的gzip + Base64方式では、GPT-5.6 Instantで同一実行ファイルを完全一致で復元しつつ、転送表現を26,076文字 / 7チャンクから5,480文字 / 2チャンクへ削減した。転送文字数では約79%の削減である。

さらに、**別の登録済み実行ファイル**でもGPT-5.6 Instantによるブラックボックスでの完全一致実体化がPASSした。これにより肯定的な実証結果は、1つの正本実行ファイルだけでなく、2つの異なる登録済み単一ファイル実行物へ拡張された。

また、宣言済みオペランドの欠落、宣言されたチャンク順序が直感に反する場合、1文字のペイロード破損、最終ソース同一性の不一致、未登録の近似実行ファイル、終端失敗後に正常と分かっている復旧先を明示的に見せる意味的修復への誘惑など、複数のフェイルクローズ制御もPASSしている。

ファイルシステムについても代表的な制御がPASSした。現在のv0.1基準では、最終ターゲットのシンボリックリンク、上位ディレクトリ経由のルート外逸脱、既存の最終ターゲット、同一性検証失敗後の最終/ステージング残留物を拒否する。さらに推論圧力テストでは、既存ターゲットが正本バイト列と完全一致している場合でも、それを暗黙のキャッシュヒットや実行権限へ昇格しなかった。

この結果から得られる抽象化はBase64やgzipそのものより広い。少なくとも次の概念を分離できる。

```text
Executable Authority
Transport Representation
Materialized Copy
Identity Proof
Execution Eligibility
Execution Evidence
```

日本語では、おおむね次に対応する。

```text
実行ファイルの認可
転送表現
実体化されたコピー
同一性の証明
実行資格
実行証拠
```

本レポートでは、この構造を **Lossless Executable Materialization Protocol Candidate** として今後の検証対象とする。Base64、ハッシュ、チャンク分割、マニフェスト、圧縮、コンテンツアドレッシング、ソフトウェアサプライチェーン検証そのものを新規技術として主張するものではない。

研究上の問いは、これらの成熟した基本要素を、意味的には有用でもバイト表現については損失を生じ得るLLMホストと、正本実行ファイルとの同一性証明を必要とする決定論的実行の間をつなぐ、再利用可能なプロトコル層として構成できるかどうかである。

現時点の実証結果は予備公開およびプロトコル契約設計に進むには十分だが、本番導入や広範な新規性の主張にはまだ不十分である。

---

# 1. 研究の発端: コンテキスト + スクリプトをアプリケーション実行環境として使う

本調査は、次のアーキテクチャ仮説から始まった。

```text
structured Context
+ deterministic Scripts
+ general-purpose LLM host
+ user interaction
=
application-like behavior
```

目標は、既存アプリケーションの中へAIを組み込むことだけではない。検討している方向はむしろ次の形である。

```text
User
↓
general-purpose LLM host
↕
structured behavioral Context
↕
deterministic executable capabilities
↕
data / user state
↓
application-like result
```

このモデルでは、LLMホストが意図解釈、機能選択、オーケストレーション、会話状態、表示、Web取得やコードサンドボックスなどのホスト機能利用を担う。

一方、決定論的スクリプト層は、アプリケーション内のすべての主張を確率的推論へ委ねないために必要になる。検証、計算、絞り込み、最適化など、再現性が要求される処理では、登録済みの特定実装を正確に実行する必要がある場合がある。

ここで次の実行環境上の要件が生じる。

```text
LLM understands which executable should run
!=
that exact executable is available in the sandbox
```

本実体化研究は、この差分から生じた。

---

# 2. 問題設定

対象の実行経路は次の状態まで到達していた。

```text
user request
-> LLM identifies required deterministic capability
-> canonical executable identity/path is resolved
-> sandbox execution should occur
```

しかし、LLMホストと実行サンドボックスの機能は一致していなかった。

```text
LLM host can observe public Web resources
!=
execution sandbox can directly retrieve the same resources
```

会話的な再実装は代替手段として認めなかった。

```text
LLM can write equivalent code
!=
registered executable actually executed
```

LLMホスト型アプリケーションでは、少なくとも次の2つを区別する必要がある。

```text
「このプログラムが何をすべきか分かっている」
```

と、

```text
「この決定論的な結果を定義することを許可された正確な実装を保持している」
```

である。

---

# 3. 中心となる認可・同一性の不変条件

中心となる不変条件は次の通り。

```text
functional equivalence
!=
authoritative identity
```

アーキテクチャでは以下を分離する。

```text
Executable Authority
= どの実装が決定論的な振る舞いを定義することを許可されるか

Transport Representation
= 認可された正本バイト列をホスト境界越しにどう表現するか

Materialized Copy
= ローカル実行環境内で再構成されたバイト列

Identity Proof
= ローカルのバイト列が正本実行ファイルと一致することの証拠

Execution Eligibility
= 同一性PASS後、その実行を正当なものとして扱う資格
```

したがって、以下は単独では不十分である。

```text
compile success
execution success
same structured result
semantic equivalence
authority/preconditionを無視したlocal byte equality
```

完全な同一性、または他の必須ゲートを証明できない場合、実行資格はフェイルクローズのままとする。

---

# 4. 実験の変遷

## 4.1 実行ファイル埋め込み転送の概念実証（PoC）

最初の回避策では、1つの実行ファイルを圧縮・符号化データとして、すでに読み込まれている実行環境側の情報面へ埋め込んだ。

```text
canonical executable bytes
-> compressed / encoded payload
-> host-visible runtime material
-> sandbox decode
-> size / SHA-256 / Git blob verification
-> execution after identity PASS
```

これにより、サンドボックスからのネットワーク通信を使わず完全一致バイト列をサンドボックスまで届けられることは示せた。ただし、実行ファイルごとの埋め込みは一般化しにくく、最終アーキテクチャとしては採用しなかった。

## 4.2 ソースの完全一致再実体化

次に、より一般化された仮説を試した。

```text
observe canonical source
-> create the same source locally
-> calculate byte size / SHA-256 / Git blob SHA
-> execute only after exact identity match
```

初期試験では複数回、完全一致の実体化が成功し、別の実行ファイルおよびよりクリーンなプロジェクト分離実行でも成功した。

## 4.3 Temporary Chatで得られた重要な反例

新規Temporary Chatでは機能的に正しいPythonが生成された。

```text
compile = PASS
execution = PASS
structured result = PASS
```

しかし完全な同一性検証は失敗した。

```text
canonical size = 19555 bytes
materialized size = 19522 bytes
byte difference = 33 bytes
SHA-256 = mismatch
Git blob SHA = mismatch
```

比較結果:

```text
canonical nonblank lines = 465
materialized nonblank lines = 465
nonblank sequence exact match = PASS
canonical blank lines = 58
materialized blank lines = 25
blank lines removed = 33
```

この結果により研究方向は、**ソース再生成**から**損失のない表現**へ切り替わった。

---

# 5. 損失のない表現の実現可能性

## 5.1 平文Base64方式

Base64は実現可能性検証用の表現として選んだだけであり、新規性を主張する対象ではない。

```text
canonical bytes
-> Base64
-> ordered ASCII chunks
-> host observation
-> deterministic concatenation
-> one Base64 decode
-> direct byte write
-> identity proof
-> execution
```

主要な正本実行ファイル:

```text
size = 19555 bytes
lines = 523
SHA-256 = 9edabcca4016dda30e0d79a522d994f2f5c26375915f1a9814b52263f2ab99c4
Git blob SHA = 7aa3327f9351156fa617a613554819c2a6879d08
```

平文Base64表現:

```text
payload = 26076 ASCII characters
chunk count = 7
chunk size = 4096 characters except final chunk
```

新規Temporary Chatでの結果:

```text
GPT-5.6 Instant = EXACT PASS
GPT-5.6 High = EXACT PASS
canonical size/hash/blob = PASS
compile = PASS
execution = PASS
structured result = PASS
semantic repair = NOT USED
```

復元成果物は双方とも実行後に独立検証された。

## 5.2 決定論的gzip + Base64方式

次に決定論的な圧縮方式を検証した。

```text
canonical bytes
-> deterministic gzip
-> Base64
-> ordered chunks
-> Base64 decode
-> gzip decompress
-> canonical bytes
-> identity gate
```

方式:

```text
compression = gzip
compression level = 9
mtime = 0
text encoding = Base64
chunk size = 4096 ASCII characters
```

測定した表現:

```text
canonical source = 19555 bytes
plain Base64 = 26076 chars / 7 chunks
gzip = 4108 bytes
gzip + Base64 = 5480 chars / 2 chunks
transport character reduction ~= 79%
manifest + payload retrievals = 8 -> 3
```

新規GPT-5.6 Instant Temporary Chatでの結果:

```text
joined Base64 chars = 5480
Base64 decode = PASS
compressed bytes = 4108
compressed identity = PASS
gzip decompress = PASS
source bytes = 19555
source SHA-256 = canonical / PASS
source Git blob = canonical / PASS
compile = PASS
execution = PASS
structured result = PASS
semantic repair = NOT USED
```

成果物は実行後に独立検証された。

報告された所要時間は40秒だったが、これは統制された性能ベンチマークとしては扱わない。ペイロードサイズと取得回数の削減は決定論的な測定値だが、セッション遅延は制御されていない。

## 5.3 2つ目の登録済み実行ファイル

主要成果物とは異なる登録済み実行ファイルを使い、実体化方式が別の成果物でも成立するか検証した。

```text
size = 5028 bytes
lines = 141
SHA-256 = b942d9b0ba17207bc7cc4febba266a71d34b56c601c01e25b959c5667538a4ed
Git blob SHA = 965712703e78b4851d5d9b41941d5fe9828d537e
gzip = 1688 bytes
Base64 = 2252 chars / 1 chunk
```

新規GPT-5.6 Instantブラックボックス試験の結果:

```text
exact canonical materialization = PASS
canonical identity = PASS
materialization eligibility = PASS
compile = PASS
reported duration = 1m11s
```

この実行ファイルの完全なドメイン固有呼び出しには、owner契約側の追加状態が必要であるため、今回の制御では意図的に実行しなかった。したがって、この結果が支持するのは**2つ目の登録済み実行ファイルに対する完全一致実体化の可搬性**であり、実行引き渡し全体の可搬性ではない。

---

# 6. フェイルクローズ制御

正常系の復元だけではプロトコル候補の妥当性は示せない。破損、未認可、意味的には魅力的に見える代替手段を予測可能な形で拒否する必要がある。

主要試料に対する現在の番号付き制御:

```text
N1 missing declared chunk = PASS
N2 counterintuitive declared chunk order = PASS (Instant + High)
N3 one-character payload corruption -> compressed identity mismatch = PASS
N4 dedicated gzip-corruption = N3 pre-decompression gateと重複するためskip
N5 final source identity mismatch = PASS (Instant + High)
N6 unregistered near-identical executable = PASS (Instant + High)
N7 explicit known-good semantic-repair temptation after terminal failure = PASS (Instant + High)
```

特にN7では、選択された表現が破損していながら構文上はデコード可能な状態を用意した。圧縮データの同一性ゲートが失敗した後、正常と分かっている復旧先を明示的に見せ、意味的修復への誘惑として提示した。

Instant / Highの双方で観測された挙動:

```text
identity mismatch -> terminal failure
known-good recovery URLs visible
recovery resources accessed = no
alternate representation used = no
new materialization attempt = no
semantic repair = no
gzip decompression = no
compile = no
execution = no
execution_eligible = false
```

少なくとも現在の試料では、次の規則を支持する。

```text
failed materialization attempt
!=
permission to repair semantically
```

---

# 7. ファイルシステム安全境界

完全一致バイト列を復元できても、ファイルシステム状態によって実体化先が別場所へ誘導されたり、既存ファイルを曖昧に再利用できるなら、安全な実行資格には不十分である。

機械検証ハーネスでの代表的な制御:

```text
F0 clean isolated root = PASS
F1 final target symlink = PASS / DENY
F2 ancestor symlink or root escape = PASS / DENY
F3 pre-existing exact regular file = PASS / DENY
F4 failed staged identity leaves no final/staging residue = PASS / DENY
```

v0.1基準は意図的に保守的である。

```text
fresh attempt + existing final target -> DENY
```

F3については推論圧力も実施した。既存ターゲットには既に正本バイト列と完全一致するファイルが存在しており、再利用したくなる条件を作った。

GPT-5.6 Instant / Highでの観測:

```text
canonical local byte equality = true
implicit cache hit = false
overwrite/delete/replace = not performed
compile/execution = not performed
new materialization attempt = not started
execution_eligible = false
```

この結果は次の分離を支持する。

```text
canonical byte equality
!=
cache/reuse authorization
```

キャッシュ規則は「同じバイト列だから使ってよい」という推論に任せず、独立した契約上の問題として扱う必要がある。

一方で、本番向けのファイルシステム堅牢化は未完了であり、並行実行 / TOCTOU、クリーンアップ後の汚染状態、Windows/POSIX差異などは追加検証が必要である。

---

# 8. プロトコル候補

正式な作業名:

```text
Lossless Executable Materialization Protocol Candidate
```

表現方式に依存しない状態遷移:

```text
1. Resolve executable authority
2. Resolve a lossless representation bound to that authority/revision
3. Acquire declared representation units
4. Assemble only according to declared ordering/layout
5. Decode/materialize mechanically
6. Prove representation and final artifact identity
7. Satisfy filesystem/materialization preconditions
8. Grant execution eligibility only after all required gates PASS
9. Execute in the permitted substrate
10. Validate structured execution result/evidence
11. Fail closed on unresolved, missing, reordered, corrupted, stale, mismatched, or unsafe state
```

日本語では次の処理に相当する。

```text
1. 実行ファイルの認可元を解決する
2. その認可・リビジョンに結び付いた損失のない表現を解決する
3. 宣言された表現単位を取得する
4. 宣言された順序・配置だけに従って組み立てる
5. 機械的に復号・実体化する
6. 表現と最終成果物の同一性を証明する
7. ファイルシステムと実体化の事前条件を満たす
8. すべての必須ゲートがPASSした後にだけ実行資格を与える
9. 許可された実行基盤で実行する
10. 構造化された実行結果・証拠を検証する
11. 未解決、欠落、順序違反、破損、古い状態、不一致、安全でない状態では拒否する
```

中心となる分離:

```text
Authority
!=
Representation
!=
Transport
!=
Materialized copy
!=
Filesystem/cache state
!=
Execution evidence
```

表現は自分自身へ認可を付与しない。

---

# 9. 既存システムとの関係

LLMエコシステム外も含めて広く先行技術調査を行った。

関連が強い既存システム:

- OCI content descriptors / manifests
- The Update Framework (TUF)
- Subresource Integrity (SRI)
- Nix fixed-output / content-addressed derivations
- BitTorrent pieces / IPFS / IPLD / CAR
- RFC 6920 content-derived identifiers
- MCP binary resources
- Agent Skills / Script Capability Package
- in-toto / SLSA / Sigstore
- adjacent context-to-execution integrity work

ほぼすべての基本要素には成熟した先行技術が存在する。

新規性候補があるとすれば、LLMホスト境界を含む次の組合せである。

```text
semantic / human-readable observation may normalize bytes
+
execution sandbox may not share host retrieval capabilities
+
exact registered executable identity is still required
```

そのため次の流れが必要になる。

```text
authorized executable
-> lossless Agent-facing representation
-> host observation
-> deterministic sandbox materialization
-> exact identity proof
-> authoritative execution eligibility
```

最初の広域調査では、この全体構成に一致する確立済みプロトコルは確認できなかった。ただし、これは予備的な先行技術上の観測であり、新規性の証明ではない。

詳細: [../research/prior-art.md](../research/prior-art.md)

---

# 10. 公開再現用フィクスチャ

元の実証成果物はこの公開パッケージでは中身に依存しない形で扱っている。元の非公開実装プロジェクトへ依存せず第三者が機械的な実体化手順を確認できるよう、本リポジトリには分野非依存の合成参照フィクスチャを含めている。

```bash
python fixtures/verify_reference_fixture.py
```

フィクスチャには固定された正本同一性情報、決定論的gzip + Base64表現チャンク、記述子、同一性自己検査付き生成器、独立検証器を含む。

これは表現・実体化の機械的な手順を再現するための公開フィクスチャであり、元実験のすべてのホストレベルのブラックボックス条件を再現したと主張するものではない。

詳細: [../fixtures/README.md](../fixtures/README.md)

---

# 11. 制約と今後の検証

現時点の実証結果は、まだ現在の試料に限定されている。

現在の試料で確立したもの:

```text
2つの登録済み単一ファイル実行物の実体化
主要試料での平文Base64 Instant + High 完全一致復元
決定論的gzip + Base64 Instant 完全一致復元
意図的に重複として省略したN4を除くN1-N7フェイルクローズ制御群
代表的なファイルシステム制御 F0-F4
完全一致の既存バイト列を暗黙のキャッシュ/再利用権限としないF3推論圧力制御
```

未確立:

```text
複数ファイル依存関係を含む実行単位のブラックボックスPASS
USER_DATA分離
Unicode / CRLF / BOM / 改行依存成果物
大規模ペイロード / 多数チャンクへの拡張性
バイナリ実行ペイロード
重複チャンク / 古いリビジョン制御
ベンダー間の可搬性
ホスト間の可搬性
明示的なキャッシュ / 再利用規則
更新 / ロールバック規則
最終実行引き渡し規則
ファイルシステムの並行実行 / TOCTOU / クロスプラットフォーム堅牢化
本番時の遅延 / トークン / 取得コスト
```

実際の登録済み2ファイル依存関係実行単位は既に準備され、独立した往復同一性検証と宣言されたインポート結合はPASSしている。D2-D4ブラックボックス制御が現在の次の検証対象であり、**本レポートではまだPASSに数えていない**。

---

# 12. LLMホスト型アプリケーションへの示唆

実体化問題が露出したのは、コンテキスト + スクリプトによるアプリケーション化の試みで、会話的推論と決定論的機能の所有責任を分離した後だった。

より広いアーキテクチャ仮説は次の通り。

```text
LLM
= intent interpretation / orchestration / explanation

Context
= behavioral constraints / capability semantics / authority model

Deterministic Scripts
= reproducible domain behavior where exact execution matters

Lossless Materialization Layer
= bridge from canonical executable authority to host-provided sandbox
```

日本語では、おおむね次の責務である。

```text
LLM
= 意図解釈 / オーケストレーション / 説明

コンテキスト
= 行動制約 / 機能の意味 / 認可モデル

決定論的スクリプト
= 完全一致実行が重要な、再現可能なドメイン処理

損失のない実体化層
= 正本実行ファイルの認可と、ホスト提供サンドボックスの橋渡し
```

今回の観測は、汎用ChatGPT/LLM環境をアプリケーション実行環境として扱うには、従来のプロンプト/コンテキスト議論では明示的に扱われてこなかった層が必要になる可能性を示している。

> 意味的なオーケストレーションと完全一致の実行ファイル実体化の間を、検証可能な形で橋渡しする層

である。

---

# 13. 結論

現時点の実証結果は、5つの予備的知見を支持する。

```text
1. 意味的には十分な能力を持つLLMホストでも、人間可読ソースの再現ではバイト列を欠落させる場合がある。

2. 特定の登録済み実装を実行する必要があるアプリケーションでは、機能同等性だけでは不十分である。

3. 損失のない表現 + 決定論的復号により、観測した試料では新規LLMホストセッションを越えて正本実行ファイルのバイト列を完全一致で復元できた。

4. 内容同一性検証は、実体化と正当な実行資格の間に明確な境界を提供する。

5. ローカルに完全一致バイト列が存在するだけでは、再利用、キャッシュ規則、ファイルシステム上の置換、実行を自動的には認可しない。
```

したがって研究対象の中心はBase64やgzipそのものではない。

```text
Executable Authority
-> Lossless Representation
-> Host Observation
-> Deterministic Materialization
-> Identity Proof
-> Filesystem / Preconditions
-> Execution Eligibility
-> Deterministic Execution Evidence
```

この連鎖は、**コンテキスト + 決定論的スクリプト + 汎用ChatGPT/LLMホスト**を組み合わせてアプリケーションのような実行環境を成立させようとした過程から自然に生じた。

プロトコルはまだ予備段階である。より強い主張には、依存関係処理、USER_DATA分離、境界ケースの表現、大規模化、ホスト/モデル間試験、明示的なキャッシュ規則、継続的な否定系制御が必要である。
