# 日本語翻訳ガイド

## 目的

このガイドは、Lossless Executable Materialization公開研究リポジトリの英語文書を日本語化する際の表記方針を固定するためのものです。

単なる直訳ではなく、日本語の技術文書として自然に読めること、英語と日本語が不必要に混在しないこと、英語版との証拠照合ができることを同時に重視します。

---

## 1. 基本方針

本文、見出し、表の説明、概念図、説明用の擬似状態は、可能な限り日本語へ翻訳します。

特に、一般的なIT用語として日本語表現が定着している語は、日本語またはカタカナ表記を優先します。

例:

```text
host                    -> ホスト
resource                -> リソース
sandbox                 -> サンドボックス
caller context          -> 呼び出し側コンテキスト
execution surface       -> 実行環境側
relay                   -> 中継転送
transport               -> 転送
materialization         -> 実体化
canonical               -> 正本 / 正本の
exact                   -> 完全一致 / 正確な
identity                -> 同一性
authority               -> 認可 / 認可根拠
descriptor              -> 記述子
immutable               -> 変更不能 / 不変
evidence                -> 証拠
fixture                 -> フィクスチャ
black-box               -> ブラックボックス
fail-closed             -> フェイルクローズ
generic                 -> 汎用
cross-unit              -> 実行単位横断
trusted host            -> 信頼済みホスト
```

文脈により、機械的な一語一訳より自然な日本語を優先します。

---

## 2. 固定識別子は翻訳しない

英語版との照合や機械的な検証に使う固定識別子は原文を保持します。

代表例:

```text
PASS
FAIL
BLOCKED
OPEN
H1 / H2 / H3 / H4
SHA-256
Base64
GPT-5.6 Instant
GPT-5.6 High
v0.1-preliminary
ファイル名
パス
URL
ハッシュ値
エラーコード
状態コード
スキーマ上の固定フィールド名
```

状態語を本文で説明する場合は、日本語を併記してよいですが、証拠表や識別子として使う箇所では原文を残します。

---

## 3. プロトコル固有語

研究上の正式名称は、最初の出現で日本語説明を付け、その後は日本語中心で記述します。

例:

```text
Lossless Executable Materialization
-> 損失のない実行ファイル実体化

Executable Authority
-> 実行ファイルの認可

Execution Eligibility
-> 実行資格

Execution-Surface Transfer
-> 実行環境側への転送

Identity Proof
-> 同一性の証明
```

正式なプロトコル名そのものは固有名として英語表記を保持してよいものとします。

---

## 4. 概念図・擬似コード

説明用の概念図や擬似コードは、機械実行されるコードではないため、原則として日本語化します。

例:

```text
ホストでリソースを観測
-> 呼び出し側コンテキストで完全一致データを取得
-> 実行環境側へ中継転送
-> 正本同一性を検証
-> 実行
```

ただし、実際の状態コード、フィールド名、ハッシュ、コマンド、プログラムコードは翻訳しません。

---

## 5. 証拠と解釈を分ける

日本語化によって証拠の強さを変えません。

次を区別します。

```text
観測済み
推定
仮説
未確立
```

英語版で限定されている主張を、日本語版で強く断定してはいけません。

---

## 6. 不要な英語混在を避ける

次のような表記は、固定識別子でない限り避けます。

```text
host surface
caller-context
exact bytes
relay primitive
canonical execution
generic transport
cross-host portability
```

日本語では、原則として次のように記述します。

```text
ホスト側の取得経路
呼び出し側コンテキスト
完全一致バイト列
中継転送の基本機構
正本実行
汎用転送
ホスト間の可搬性
```

---

## 7. 日本語版ファイル名

英語版と対になる日本語文書は、原則として同じ基本ファイル名に `.ja.md` を付けます。

例:

```text
2026-08-30-host-surface-relay-update.md
2026-08-30-host-surface-relay-update.ja.md
```

英語版と日本語版は相互リンクします。
