# AI-Driven Development Optimization Kit

> **AIコーディングエージェントの自律性を活かしながら、NFR（非機能要件）の過剰検証、無制限のリトライ、不要なリソース消費を抑制するための、ベンダー中立な設定テンプレート集。**

## 対象とする開発環境

本キットは、**OpenAI Codex**、**Cursor**、**Google Antigravity**、Claude Codeなど、コードの生成・編集・テスト・コマンド実行を支援するエージェント型開発環境を想定している。これらは同一のモデルではなく、IDE・CLI・エージェントオーケストレーションを含む異なる製品である。製品ごとに設定ファイルの検出方法、実行権限、モデル、並列性、サンドボックスの実装が異なるため、導入時には当該製品の公式ドキュメントを確認すること。

| 環境 | 公式上の位置付け | 本キットで扱う論点 |
|---|---|---|
| [OpenAI Codex](https://openai.com/codex/) | ソフトウェアエンジニアリング向けAIコーディングエージェント。ChatGPT、IDE、CLIで利用可能。 | ターミナル／IDE実行時のテスト範囲、リトライ、プロセス管理。 |
| [Cursor](https://cursor.com/) | エージェント型コーディング環境。Desktop、CLI、エージェント機能を提供。 | Rulesやプロジェクト指示における最小限の行動制約。 |
| [Google Antigravity](https://antigravity.google/) | エージェントファーストの開発プラットフォーム。CLI、IDE、複数エージェント管理を提供。 | 並列エージェント、バックグラウンド作業、検証タスクの資源上限。 |

## キットの目的

本キットは、AIエージェントのテストを減らすこと自体を目的にしない。**変更に対して適切なテストを、適切な層で、適切なタイミングに実行する**ための判断境界を定義する。

次の問題を対象とする。

- 機能変更と無関係なフルE2E、負荷、レースコンディション検証の自動開始。
- 同一障害に対する無制限の修正・再テストループ。
- バックグラウンドプロセスやブラウザの残留。
- MVPや社内ツールのスコープを超えるNFRテストの実行。

## コンポーネント

| ファイル | 役割 |
|---|---|
| [`AGENTS.md`](./AGENTS.md) | 目的優先、最小テスト優先、根本原因優先という行動原則。 |
| [`GUARDRAILS.md`](./GUARDRAILS.md) | NFRテストの開始条件、リトライ回数、並列度、タイムアウト、プロセス後始末を定義する安全境界。 |
| [`INTEGRATION_AND_GUARDRAILS.md`](./INTEGRATION_AND_GUARDRAILS.md) | Claude Codeを例にした導入手順とNFRガードレールの設定例。 |
| [`TDD_OPTIMIZATION_KIT.md`](./TDD_OPTIMIZATION_KIT.md) | 運用ルールとプロンプト例。 |
| [`VERIFICATION_REPORT.md`](./VERIFICATION_REPORT.md) | 最小のサンドボックス検証の記録と限界。 |

## 導入方法

プロジェクトの規模とリスクに合わせて、テンプレートをコピーしてから調整する。

```bash
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/AGENTS.md -o AGENTS.md
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/GUARDRAILS.md -o GUARDRAILS.md
```

その後、対象のAIコーディング環境がプロジェクト内の指示ファイルを認識することを確認する。認識しない製品では、内容をその製品の公式ルール機構へ移植する。

> 導入後は、トークン、CPU、テスト時間、失敗回数を**導入前後で実測**すること。特定の削減率やCPU使用率は環境・プロジェクト・モデル・実行権限に依存するため、本キットは数値改善を保証しない。

## 設計原則

1. **Intent first**: 「何を達成するか」を明確にし、細かな手順は必要な場合だけ加える。
2. **Smallest test first**: 変更に直接関係する単体テスト、型検査、lintから開始する。
3. **NFR by explicit decision**: 負荷、ストレス、セキュリティ、並行性テストは、リスク、対象環境、合格基準を人間が明示して開始する。
4. **Root cause over retries**: 失敗を盲目的に再試行せず、証拠を読み、原因を切り分ける。
5. **Hard operational bounds**: リトライ、並列実行、タイムアウト、残留プロセスに明確な上限を設ける。

## 検証上の注意

`VERIFICATION_REPORT.md` は、最小のNode.js単体テストを使った**設定方針のスモークテスト**である。Codex、Cursor、Google Antigravity、Claude Codeの実行器・モデル・ハーネスの性能比較や、リソース削減を実証するベンチマークではない。採用判断には、各チームの代表タスクを用いた再現可能なA/B測定を追加すること。

## ライセンス

ライセンスを選定・追加するまでは、外部利用者に対する権利許諾は明示されない。公開OSSとして配布する前に、Kanau Techの方針に合うライセンス（例：MITまたはApache-2.0）を選定して `LICENSE` を追加すること。

## 参考資料

- [OpenAI Codex](https://openai.com/codex/)
- [Cursor](https://cursor.com/)
- [Google Antigravity](https://antigravity.google/)
- [Google Antigravity: Introducing Google Antigravity](https://antigravity.google/blog/introducing-google-antigravity)

**確信度**: 高。製品の位置付けは公式ページに基づく。一方、個別プロジェクトにおけるコスト・速度・品質の改善度は測定なしに断定しない。
