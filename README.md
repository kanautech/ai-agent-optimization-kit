# Claude Code TDD Guardrails Kit

> **Claude Codeを主対象に、AIエージェントの自律性を保ちながら、NFR（非機能要件）の過剰検証、無制限リトライ、不要なプロセス残留を防ぐ設定・Hookテンプレート集。**

## 何を解決するか

Claude Codeは、プロジェクト指示、ターミナル、ファイル編集、テスト、ブラウザ操作を組み合わせてタスクを実行できる。この自律性を活かすには、テストを少なくするのではなく、**正しいテストを、正しい層で、正しいタイミングに実行する**ための境界が必要である。

本キットは以下の失敗モードを対象にする。

- 局所的な変更から、無関係なフルE2E・負荷・レースコンディション検証へ拡張すること。
- 同じ失敗に対して修正・再テストを無制限に繰り返すこと。
- テストワーカー、開発サーバー、ブラウザがタスク後に残留すること。
- MVP・社内ツールの段階で、スコープを超えるNFR検証を自動開始すること。

## Claude Codeでの構成

Claude Codeでは、自然言語の原則と決定論的な制約を分ける。

| 層 | 実装場所 | 役割 |
|---|---|---|
| Intent Layer | `CLAUDE.md` | 目的、変更範囲、完了条件、最小テスト優先の原則を定義する。 |
| Safety Layer | `.claude/settings.json` と `PreToolUse` Hooks | 実行前に保護対象や高リスク操作をブロックし、NFRの開始条件を定義する。 |
| Feedback Layer | `PostToolUse` / `Stop` / `Notification` Hooks、CI | 失敗証拠、整形、プロセス後始末、停止・通知を一貫して実行する。 |

Claude CodeのHooksは、ライフサイクル上の特定ポイントでユーザー定義コマンドを実行する公式機構であり、LLMに「守ってほしい」と依頼するだけでは担保できない決定論的な制約を実装できる。[公式Hooksガイド](https://code.claude.com/docs/en/hooks-guide)

## 最短の導入方法

```bash
mkdir -p .claude/hooks
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/CLAUDE.md -o CLAUDE.md
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/.claude/settings.json -o .claude/settings.json
```

次に、プロジェクトのテストコマンド・パッケージマネージャ・保護すべきファイル・NFRテストの開始条件に合わせてテンプレートを編集する。詳細は [`CLAUDE_CODE_INTEGRATION.md`](./CLAUDE_CODE_INTEGRATION.md) を参照する。

## ファイル一覧

| ファイル | 用途 |
|---|---|
| [`CLAUDE.md`](./CLAUDE.md) | Claude Codeに渡す、目的・テスト範囲・停止条件のプロジェクト指示。 |
| [`.claude/settings.json`](./.claude/settings.json) | Claude Code Hooksを登録するプロジェクト設定。 |
| [`.claude/hooks/pre_tool_guard.py`](./.claude/hooks/pre_tool_guard.py) | NFRテスト、危険な並列実行、保護対象への操作を実行前に判定するHook。 |
| [`.claude/hooks/post_tool_cleanup.sh`](./.claude/hooks/post_tool_cleanup.sh) | タスク後の基本的な後始末と証拠記録を支援するHook。 |
| [`CLAUDE_CODE_INTEGRATION.md`](./CLAUDE_CODE_INTEGRATION.md) | Claude Codeへの導入・検証・ロールバック手順。 |
| [`AGENTS.md`](./AGENTS.md) / [`GUARDRAILS.md`](./GUARDRAILS.md) | 他のエージェント型環境へ原則を移植する際の汎用リファレンス。 |

## NFRテストの開始条件

性能、負荷、ストレス、レース、セキュリティ、フルE2Eは、実装タスクの標準手順として自動開始しない。開始するには、少なくとも以下を明示する。

1. **対象環境**: ローカル、ステージング、本番相当など。
2. **シナリオ**: どの操作、トラフィック、並列性を検証するか。
3. **合格基準**: レイテンシ、エラー率、整合性、セキュリティ要件など。
4. **資源予算**: 所要時間、並列数、使用可能な環境・認証情報。
5. **実行責任者**: 誰が結果を解釈し、次の判断を行うか。

## 効果の評価

本キットは、速度・トークン・CPU・品質の改善率を保証しない。効果は、モデル、リポジトリ、テスト構成、権限、チームのワークフローに依存する。採用判断では、代表タスクを選び、導入前後で以下を測定する。

| KPI | 定義 |
|---|---|
| 初回フィードバック時間 | 変更開始から、lint・型検査・対象単体テストが完了するまでの時間。 |
| テスト実行回数 | 1タスクにおけるテストコマンドの実行回数。 |
| 同一失敗の連続回数 | 同じエラーシグネチャに対する反復数。 |
| 残留プロセス数 | タスク後に残ったテストワーカー、サーバー、ブラウザ。 |
| 回帰検出率 | PR・リリースゲートで検出された回帰の割合。 |

## 他ツールへの応用

Codex、Cursor、Google Antigravityなどでも、最小関連テスト、NFRの明示承認、失敗時の停止条件、資源上限という原則を応用できる。ただし、これらはClaude Codeとは異なる製品であり、`CLAUDE.md` やHooksの設定をそのまま認識することは保証されない。各製品の公式ルール・設定・フック機構に同じ原則を移植すること。

## ライセンス

ライセンスを選定・追加するまでは、外部利用者に対する権利許諾は明示されない。公開OSSとして配布する前に、Kanau Techの方針に合うライセンス（例：MITまたはApache-2.0）を選定して `LICENSE` を追加すること。

## 公式資料

- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)（取得日: 2026-08-17）
- [Claude Code Settings](https://code.claude.com/docs/en/settings)（取得日: 2026-08-17）
- [OpenAI Codex](https://openai.com/codex/)（補助的適用先）
- [Cursor](https://cursor.com/)（補助的適用先）
- [Google Antigravity](https://antigravity.google/)（補助的適用先）
