# Claude Code 導入手順と NFR ガードレール詳細設定ガイド

## 1. Claude Code / AI エージェントへの具体的導入手順

既存のプロジェクトや新規プロジェクトにおいて、AIエージェント（Claude Code、Codex、Sol等）のポテンシャルを最大限に引き出しつつ、暴走やリソース浪費を防ぐための導入手順を以下に示す。

### ステップ 1: リポジトリの現状把握とプロンプトの「大掃除」（Ablation）
1. プロジェクトのルートディレクトリを確認する。既に `CLAUDE.md` や `AGENTS.md` が存在する場合、その内容を精査する。
2. 過去のモデル向けに書かれた「1行ずつの細かい手順指定」や「過剰な制約（例：すべての関数に必ずコメントを書き、かつ厳格な型アサーションを要求する等）」の80%を削除する [6]。
3. AIに求める「最終的なゴール（Intent）」のみを残し、指示を徹底的に簡素化する。

### ステップ 2: キットファイルの配置
本キットに含まれる以下のファイルをプロジェクトのルートディレクトリにコピーする。
- `AGENTS.md` （行動階層：Unhobbling と最小限のテスト原則）
- `GUARDRAILS.md` （安全階層：NFR過剰検証の禁止とリソース制限）

### ステップ 3: エージェントへの初回プロンプト投入
初めて Claude Code を起動する際、または設定ファイルを更新した直後は、以下のプロンプトを入力してエージェントにルールを認識させる。

> **プロンプト例**:
> `"ルートディレクトリにある AGENTS.md および GUARDRAILS.md の内容を読み込み、理解してください。今後はこのガイドラインに従って、最小限のテストファーストと、NFR過剰検証の回避を厳守して開発を進めてください。準備ができたら『了解しました。』とだけ答えてください。"`

---

## 2. NFR（非機能要件）過剰検証を防ぐための詳細ガードレール設定

AIモデルが勝手に高負荷なストレステストや過剰なE2Eテストを実行するのを防ぐため、`GUARDRAILS.md` に記述する具体的なルールと設定例を以下に提示する。

### 2.1. 禁止すべき「AIの過剰テスト」パターン
AIエージェントは「完璧にしようとする」あまり、以下のような不要なテストを自律生成しがちである。これらを明示的に禁止する。

- **UUID衝突・並行処理の過剰テスト**:
  - *禁止事項*: 数十個のワーカーを同時に立ち上げてUUIDの競合やデータベースのアイソレーションレベル（Level 3等）をローカルで検証すること。
  - *理由*: PoCやMVP段階ではオーバーエンジニアリングであり、リソースを不必要に消費する。
- **ローカル環境での極端な P99 レイテンシ検証**:
  - *禁止事項*: ローカルのモック環境に対して、到達困難なミリ秒単位のP99スループット目標を課してループに陥ること。
- **微小な変更に対するフルE2Eブラウザテスト**:
  - *禁止事項*: バックエンドのユーティリティ関数を1行変更しただけで、ヘッドレスブラウザを起動して全画面のE2Eテストを実行すること。

### 2.2. `GUARDRAILS.md` の実務設定スニペット

以下をプロジェクトの `GUARDRAILS.md` にそのまま組み込むことで、物理的な暴走を防ぐことができる。

```markdown
# Strict NFR & Resource Guardrails

## 1. Testing Scope Boundaries
- **Unit Tests Only by Default**: For any feature request, write and run ONLY unit tests directly related to the changed functions.
- **Integration Tests on Demand**: Expand to integration tests ONLY when explicitly instructed or when crossing module boundaries.
- **Release Gates Only for NFRs**: Performance, load, stress, and security penetration tests are reserved exclusively for CI/CD release pipelines. Never execute them during iterative coding loops.

## 2. Resource & Process Caps
- **Max Retries**: If a test fails 3 consecutive times, terminate the attempt immediately, output the error evidence, and prompt the human developer.
- **Process Cleanup**: Ensure all test worker processes, background servers, and browser instances are forcefully killed (`kill -9`) immediately upon test completion or failure.
- **Concurrency Control**: Run test suites sequentially unless explicit parallel flags are provided.
```

---

## 参考文献
[6] Boris Cherny. (2026). *We Cut 80% of Claude Code's Prompt*. YouTube / Y Combinator.
