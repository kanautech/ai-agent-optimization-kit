---
title: "Codex・Cursor・Antigravity時代のTDD：AIエージェントを縛らず過剰検証を止める設計"
emoji: "🧭"
type: "tech"
topics: ["codex", "cursor", "ai", "tdd", "agent"]
published: false
---

# Codex・Cursor・Antigravity時代のTDD：AIエージェントを縛らず過剰検証を止める設計

AIコーディングの論点は、もはや「コード補完が速いか」ではない。Codex、Cursor、Google Antigravityなどのエージェント型開発環境では、コード編集だけでなく、テスト、ターミナル、ブラウザ、バックグラウンド作業までが一つの自律タスクに統合されている [1] [2] [3]。そのため、設計すべき対象はモデル単体ではなく、**エージェントがどの権限で、どの終了条件まで、どの検証を実行するか**という実行系全体である。

本稿は、AIエージェントの知能を過剰な手順指示で窒息させず、同時にNFR（非機能要件）の過剰検証を防ぐための実装可能なガードレールを整理する。

## 製品を混同しない

Codex、Cursor、Google Antigravityは同じものではない。CodexはOpenAIが提供するコーディングエージェントで、ChatGPT、IDE、CLIで利用できる [1]。Cursorはエージェント型のコーディング環境で、DesktopおよびCLIを提供する [2]。Google Antigravityは、IDE、CLI、SDK、複数ローカルエージェントの管理を備えるエージェント型開発プラットフォームである [3] [4]。

この違いは重要である。指示ファイル、実行権限、利用モデル、並列実行、ネットワークアクセス、プロセス管理は製品ごとに異なる。したがって「ある製品・モデルが必ず過剰にテストする」と断定するのは技術的に雑である。正しい主張は、**高い自律性と広い実行権限を持つエージェントには、プロジェクト文脈に応じた検証境界が必要である**ということだ。

## 問題の正体：テスト量ではなく検証の意思決定が未定義

AIエージェントに「この機能を実装して、テストもして」と指示すると、どこまでをテストするかは、指示・リポジトリ文脈・利用可能なツール・モデルの推論に委ねられる。そこで以下の境界が明示されていなければ、テストの拡張は合理的に見えても、プロジェクトには不合理になり得る。

| 未定義の境界 | 起き得る挙動 | 本来決めるべきこと |
|---|---|---|
| 変更の影響範囲 | 無関係なE2Eや統合テストへ拡大。 | 変更したモジュール・外部境界・ユーザーフロー。 |
| NFRの対象 | 負荷・レース・性能テストを実装ループで開始。 | 対象環境、ワークロード、合格基準、実施時期。 |
| 失敗時の終了条件 | 同一障害の修正・再試行を繰り返す。 | リトライ回数、停止条件、エスカレーション先。 |
| 並列性 | ワーカー、ポート、DBデータの競合。 | 並列化を許可するタスクと資源予算。 |

## 「引き算」はルール削除ではなく、判断境界の最小化である

AIエージェント向けの指示を短くすること自体には価値がない。価値があるのは、重複・矛盾・抽象的な命令を減らし、エージェントが守るべき重要な境界を明確にすることである。

悪い指示は「高品質に、網羅的に、すべてテストして」である。これでは品質の定義もテスト範囲も終了条件もない。良い指示は次のように具体的である。

```markdown
- Run the smallest test directly related to the change first.
- Do not start load, stress, race, security, or full E2E tests unless a human supplies the target, acceptance criteria, and budget.
- After three identical failures, stop, preserve evidence, and request a decision.
- Run sequentially by default; parallelize only independent tests with an explicit resource budget.
```

これは自由度を奪うためのルールではない。設計・実装・デバッグといったエージェントが得意な仕事に裁量を残し、リスク受容や資源配分のような人間が決めるべき判断を切り分ける構造である。

## 3層のガードレール

### Intent Layer

目的、変更範囲、完了条件を記述する。特定の実装手順まで書き込みすぎない。

### Safety Layer

NFRテストの開始条件、最大リトライ、タイムアウト、並列度、ネットワークや本番環境へのアクセスを定義する。ここは自然言語の指示だけでなく、CI設定やサンドボックスなど技術的な制約でも担保する。

### Feedback Layer

失敗時にエージェントを再試行させるのではなく、観測事実・ログ・仮説・次の判断を返させる。これにより、人間は不確実性を抱えたままコストを燃やすのではなく、証拠に基づいて方針を決められる。

## 導入後に測るべきもの

特定の削減率を約束するのではなく、各リポジトリで導入前後を測る。代表タスクを固定し、最初の有効なフィードバックまでの時間、テストコマンド数、連続失敗回数、残留プロセス数、PRで検出された回帰を測定する。これが、ガードレールが「抑制」なのか「最適化」なのかを判断する唯一の方法である。

テンプレートと検証プロトコルは、[Kanau Tech / AI-Driven Development Optimization Kit](https://github.com/kanautech/ai-agent-optimization-kit) で公開している。

## 参考資料

[1] [OpenAI: Codex](https://openai.com/codex/)（取得日: 2026-08-17）  
[2] [Cursor: AI Coding Agent](https://cursor.com/)（取得日: 2026-08-17）  
[3] [Google Antigravity](https://antigravity.google/)（取得日: 2026-08-17）  
[4] [Google Antigravity: Introducing Google Antigravity](https://antigravity.google/blog/introducing-google-antigravity)（取得日: 2026-08-17）
