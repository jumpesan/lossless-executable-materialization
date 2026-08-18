# 予備技術レポート
# LLMホスト境界を越えるLossless Executable Materialization

## Status

```text
created: 2026-08-18
report_type: public-facing preliminary technical report / Japanese edition
research_stage: feasibility established for observed sample
protocol_status: candidate / not standardized
production_status: not established
novelty_claim: not established
```

**著者:** TBD  
**所属:** TBD  
**公開ライセンス:** TBD

---

# 概要

本レポートは、**構造化されたContextとdeterministic Scriptを組み合わせることで、汎用ChatGPT/LLM環境そのものをApplication Runtimeのように振る舞わせられるか**を検討する過程で生じた、実証的な技術調査について報告する。

この研究は当初、Transport Protocolを作ることを目的として始まったものではない。元々の目的は、従来型の専用Application Runtimeをあらかじめ構築する代わりに、構造化Context、User Interaction、deterministicな実行能力、そして汎用LLM Host自体を組み合わせることで、Application-likeな振る舞いを成立させられるかを確かめることだった。

その過程で、LLMは「どのdeterministic executableを使うべきか」を理解できるようになった一方、Execution Sandboxはfreshな公開Resourceから、その登録済みimplementationの正確なbytesを安定して取得できなかった。ここから、より深いRuntime上の問題が露出した。

**どのProgramを実行すべきか理解することと、実際に実行を許可されているauthoritativeなProgram bytesをmaterializeすることは別問題である。**

初期のExact Source Rematerialization実験は有望に見えた。しかし、その後fresh Temporary ChatでPython executableを再構成したところ、非空行はすべて再現され、機能的にも正しい出力を得られた一方で、33行の空行が黙って削除された。生成物はcompileにもexecutionにも成功したが、SHA-256およびGit blob identityはcanonical sourceと一致しなかった。

```text
semantic equivalence
!=
canonical executable identity
```

この結果、問題設定はSource Code Reconstructionから、**LLM Host境界におけるRepresentation Fidelity**へと再定義された。

次に、losslessなAgent-facing Representationを検証した。Canonical Executable BytesをASCII transport formへencodeし、順序付きchunkへ分割し、manifest/descriptorで記述した。LLM Hostの通常のWeb観測経路からそれらを取得し、Sandbox内でmechanicalに再構成し、execution前にcanonical content identityと照合した。

plain chunked Base64では、GPT-5.6 InstantとGPT-5.6 Highを用いたfresh Temporary Chatの双方で、同一の19,555-byte canonical executableを完全一致で復元した。さらにdeterministic gzip + Base64 profileでは、GPT-5.6 Instantで同一Executableを完全一致で復元しつつ、transport representationを26,076文字 / 7 chunkから5,480文字 / 2 chunkへ削減した。transport文字数では約79%の削減である。

また、missing operand、宣言されたchunk順序が直感に反する場合、1文字payload corruption、final source identity mismatch、未登録のnear-identical executable、terminal failure後にknown-good recovery locationを明示的に見せるsemantic-repair temptationなど、複数のfail-closed controlも現在のsampleでPASSしている。

この結果から得られる抽象化はBase64やgzipそのものより広い。少なくとも次の概念を分離できる。

```text
Executable Authority
Transport Representation
Materialized Copy
Identity Proof
Execution Eligibility
Execution Evidence
```

本レポートでは、この構造を **Lossless Executable Materialization Protocol Candidate** として今後の検証対象とする。Base64、hashing、chunking、manifest、compression、content addressing、software supply-chain verificationそのものを新規技術として主張するものではない。

研究上の問いは、これらの成熟したprimitiveを、semanticには有用でもbyte representationについてはlossyであり得るLLM Hostと、canonical executable identityの証明を必要とするdeterministic executionの間をつなぐ、再利用可能なProtocol Layerとして構成できるかどうかである。

現時点のevidenceは予備公開およびProtocol Contract設計に進むには十分だが、production deploymentや広範なnovelty claimにはまだ不十分である。

---

# 1. 研究の発端: Context + ScriptsをApplication Runtimeとして使う

本調査は、次のArchitecture仮説から始まった。

```text
structured Context
+ deterministic Scripts
+ general-purpose LLM host
+ user interaction
=
application-like behavior
```

目標は、既存Applicationの中へAIを組み込むことだけではない。検討している方向はむしろ次の形である。

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

このモデルでは、LLM Hostがintent interpretation、capability selection、orchestration、conversation state、presentation、Web retrievalやcode sandboxなどのHost facility利用を担う。

一方、deterministic Script Layerは、Application内のすべての主張をprobabilistic reasoningへ委ねないために必要になる。Validation、calculation、filtering、optimizationなど、再現性が要求される処理では、登録済みの特定implementationを正確に実行する必要がある場合がある。

ここで次のRuntime Requirementが生じる。

```text
LLM understands which executable should run
!=
that exact executable is available in the sandbox
```

本Materialization研究は、この差分から生じた。

---

# 2. 問題設定

対象Runtime Pathは次の状態まで到達していた。

```text
user request
-> LLM identifies required deterministic capability
-> canonical executable identity/path is resolved
-> sandbox execution should occur
```

しかし、LLM HostとExecution Sandboxのcapabilityは一致していなかった。

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

LLM-hosted Applicationでは、少なくとも次の2つを区別する必要がある。

```text
「このProgramが何をすべきか分かっている」
```

と、

```text
「このdeterministic resultを定義することを許可された正確なimplementationを保持している」
```

である。

---

# 3. Core Authority Invariant

中心となるInvariantは次の通り。

```text
functional equivalence
!=
authoritative identity
```

Architectureでは以下を分離する。

```text
Executable Authority
= どのimplementationがdeterministic behaviorを定義することを許可されるか

Transport Representation
= authoritative bytesをHost境界越しにどう表現するか

Materialized Copy
= local execution environment内で再構成されたbytes

Identity Proof
= local bytesがcanonical executableと一致することの証拠

Execution Eligibility
= identity PASS後、そのexecutionをauthoritativeとして扱う資格
```

したがって、以下は単独では不十分である。

```text
compile success
execution success
same structured result
semantic equivalence
```

Exact Identityが必要で、それを証明できない場合、Execution Eligibilityはfail-closedのままとする。

---

# 4. 実験の変遷

## 4.1 Embedded Executable Transport PoC

最初の回避策では、1つのExecutableをcompressed/encoded dataとして、すでに読み込まれているRuntime Surfaceへ埋め込んだ。

```text
canonical executable bytes
-> compressed / encoded payload
-> host-visible runtime material
-> sandbox decode
-> size / SHA-256 / Git blob verification
-> execution after identity PASS
```

これにより、Sandbox Networkingを使わずexact bytesをSandboxまで届けられることは示せた。ただし、Executableごとの埋め込みは一般化しにくく、最終Architectureとしては採用しなかった。

## 4.2 Exact Source Rematerialization

次に、より一般化された仮説を試した。

```text
observe canonical source
-> create the same source locally
-> calculate byte size / SHA-256 / Git blob SHA
-> execute only after exact identity match
```

初期試験では複数回exact materializationが成功し、別ExecutableおよびよりcleanなProject-isolated runでも成功した。

## 4.3 Critical Temporary Chat Counterexample

fresh Temporary Chatでは機能的に正しいPythonが生成された。

```text
compile = PASS
execution = PASS
structured result = PASS
```

しかしExact Identityは失敗した。

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

この結果により研究方向は、**Source Regeneration**から**Lossless Representation**へ切り替わった。

---

# 5. Lossless Representation Feasibility

## 5.1 Plain Base64 Profile

Base64はFeasibility検証用のRepresentationとして選んだだけであり、新規性を主張する対象ではない。

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

Tested Canonical Executable:

```text
size = 19555 bytes
lines = 523
SHA-256 = 9edabcca4016dda30e0d79a522d994f2f5c26375915f1a9814b52263f2ab99c4
Git blob SHA = 7aa3327f9351156fa617a613554819c2a6879d08
```

Plain Base64 Representation:

```text
payload = 26076 ASCII characters
chunk count = 7
chunk size = 4096 characters except final chunk
```

fresh Temporary Chatでの結果:

```text
GPT-5.6 Instant = EXACT PASS
GPT-5.6 High = EXACT PASS
canonical size/hash/blob = PASS
compile = PASS
execution = PASS
structured result = PASS
semantic repair = NOT USED
```

復元artifactは双方ともrun後に独立検証された。

## 5.2 Deterministic Gzip + Base64 Profile

次にdeterministic compression profileを検証した。

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

Profile:

```text
compression = gzip
compression level = 9
mtime = 0
text encoding = Base64
chunk size = 4096 ASCII characters
```

Measured Representation:

```text
canonical source = 19555 bytes
plain Base64 = 26076 chars / 7 chunks
gzip = 4108 bytes
gzip + Base64 = 5480 chars / 2 chunks
transport character reduction ~= 79%
manifest + payload retrievals = 8 -> 3
```

fresh GPT-5.6 Instant Temporary Chat result:

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

artifactはrun後に独立検証された。

reported durationは40秒だったが、これはcontrolled performance benchmarkとしては扱わない。Payload SizeとRetrieval Countの削減はdeterministic measurementだが、Session Latencyは制御されていない。

---

# 6. Fail-Closed Controls

Positive RecoveryだけではProtocol Candidateの妥当性は示せない。Corrupted / Unauthorized / Semantically Temptingな代替を予測可能にrejectする必要がある。

Primary Sampleに対する現在のNumbered Control:

```text
N1 missing declared chunk = PASS
N2 counterintuitive declared chunk order = PASS (Instant + High)
N3 one-character payload corruption -> compressed identity mismatch = PASS
N4 dedicated gzip-corruption = N3 pre-decompression gateと重複するためskip
N5 final source identity mismatch = PASS (Instant + High)
N6 unregistered near-identical executable = PASS (Instant + High)
N7 explicit known-good semantic-repair temptation after terminal failure = PASS (Instant + High)
```

特にN7では、selected representationがcorruptedでありながらsyntactically decodableな状態を用意した。Compressed Identity Gateが失敗した後、known-good recovery locationを明示的に見せ、semantic temptationとして提示した。

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

少なくとも現在のsampleでは、次のRuleを支持する。

```text
failed materialization attempt
!=
permission to repair semantically
```

---

# 7. Protocol Candidate

Working Name:

```text
Lossless Executable Materialization Protocol Candidate
```

Representation-independentなState Machine:

```text
1. Resolve executable authority
2. Resolve a lossless representation bound to that authority/revision
3. Acquire declared representation units
4. Assemble only according to declared ordering/layout
5. Decode/materialize mechanically
6. Prove representation and final artifact identity
7. Grant execution eligibility only after exact PASS
8. Execute in the permitted substrate
9. Validate structured execution result/evidence
10. Fail closed on unresolved, missing, reordered, corrupted, stale, or mismatched content
```

Core Separation:

```text
Authority
!=
Representation
!=
Transport
!=
Materialized copy
!=
Execution evidence
```

Representationは自分自身へAuthorityを付与しない。

---

# 8. Existing Systemsとの関係

LLM ecosystem外も含めて広くprior-art scanを行った。

関連が強い既存System:

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

ほぼすべてのPrimitiveには成熟したprior artが存在する。

新規性候補があるとすれば、LLM Host Boundaryを含む次のCompositionである。

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

最初の広域scanでは、この全体Compositionに一致するestablished protocolは確認できなかった。ただし、これはpreliminaryなprior-art observationであり、novelty proofではない。

詳細: [../research/prior-art.md](../research/prior-art.md)

---

# 9. Limitations / Next Work

現時点のEvidenceはまだsample-scopedである。

未確立:

```text
second independent executable exact PASS under finalized descriptor shape
multi-file dependency graphs
filesystem safety / path containment
USER_DATA separation
Unicode / CRLF / BOM / newline-sensitive artifacts
large payload / many-chunk scaling
binary executable payloads
duplicate-chunk / stale-revision controls
cross-vendor portability
cross-host portability
cache / reuse semantics
upgrade / rollback semantics
final execution handoff semantics
production latency / token / retrieval cost
```

second registered single-file executableは次のpositive-control candidateとしてすでにpackage済みだが、black-box runが完了するまでは本レポートのPASS evidenceには含めない。

---

# 10. LLM-hosted Applicationへの広い意味

Materialization Problemが露出したのは、Context + ScriptによるApplication化の試みで、Conversational ReasoningとDeterministic Capability Ownershipを分離した後だった。

より広いArchitecture Hypothesisは次の通り。

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

今回の観測は、汎用ChatGPT/LLM環境をApplication Runtimeとして扱うには、従来のPrompt/Context議論では明示的に扱われてこなかったLayerが必要になる可能性を示している。

> Semantic OrchestrationとExact Executable Materializationの間を検証可能な形で橋渡しするLayer

である。

---

# 11. Conclusion

現時点のEvidenceは、4つのpreliminary findingを支持する。

```text
1. Semanticには十分な能力を持つLLM Hostでも、human-readable sourceの再現ではbyte-lossyになり得る。

2. 特定のregistered implementationを実行する必要があるApplicationでは、functional equivalenceだけでは不十分である。

3. Lossless Representation + Deterministic Decodeにより、observed sampleではfresh LLM-host sessionを越えてcanonical executable bytesを完全一致で復元できた。

4. Content-identity verificationは、MaterializationとAuthoritative Execution Eligibilityの間に明確なboundaryを提供する。
```

したがって研究対象の中心はBase64やgzipそのものではない。

```text
Executable Authority
-> Lossless Representation
-> Host Observation
-> Deterministic Materialization
-> Identity Proof
-> Execution Eligibility
-> Deterministic Execution Evidence
```

このChainは、**Context + deterministic Scripts + general-purpose ChatGPT/LLM host**を組み合わせてApplication-like Runtimeを成立させようとした過程から自然に生じた。

Protocolはまだpreliminaryである。より強い主張を行う前に、別Executable、dependency handling、filesystem / user-data safety、scale、cross-host test、continued negative controlsが必要である。