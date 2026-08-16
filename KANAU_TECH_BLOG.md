# 【Kanau Tech ブログ】Claude Codeを安全かつ高速に使うためのTDDガードレール設計

## Claude Codeの導入課題は「能力」ではなく「実行境界」

Claude Codeは、コードの編集、テスト、CLI、ブラウザ操作を組み合わせてソフトウェアタスクを進められる。導入価値は大きいが、運用をプロンプトだけで統制しようとすると、テストの範囲、NFRの開始条件、失敗時の停止条件が曖昧になる。

Kanau Techでは、この問題を解くために **Claude Code TDD Guardrails Kit** を公開した。主対象はClaude Codeであり、`CLAUDE.md`、`.claude/settings.json`、Claude Code Hooksを組み合わせて、自然言語の行動原則と決定論的な実行制約を分離する。

## 課題：テストの量ではなく、判断の欠落

| 判断項目 | 定義されていない場合 | Kanau Techの標準 |
|---|---|---|
| 変更範囲 | 局所変更でも統合・E2Eへ検証が拡張し得る。 | 対象関数・モジュールの最小テストから始める。 |
| NFRの開始条件 | 負荷・ストレス・レース検証が実装ループへ混入する。 | 対象、シナリオ、合格基準、予算、責任者を決めてから開始する。 |
| 失敗時の終了条件 | 同一失敗への再試行が反復する。 | 連続失敗に上限を置き、ログと仮説を出して人間が判断する。 |
| プロセス後始末 | サーバー、ワーカー、ブラウザが残留する。 | Claude Codeが開始したプロセスを記録し、プロジェクト固有の後始末を実装する。 |

## 実装：`CLAUDE.md` とHooksの役割分担

`CLAUDE.md` は、Claude Codeが常に参照するプロジェクトの意思決定文書として使う。ここには、目的、変更範囲、完了条件、最小テスト優先、NFRの明示承認、失敗時の報告形式を記載する。

一方、Hooksは決定論的な統制に使う。Claude Code公式のHooksは、ライフサイクル上のイベントでユーザー定義コマンドを実行できる [1]。Kanau Techのキットでは、`PreToolUse` Hookで広範なテストや未承認NFR操作を実行前に検査し、`PostToolUse` HookでBashコマンドの証跡を保存する。

> LLMに「気を付けて」と依頼するだけでは、重要な安全境界を担保できない。判断を必要としないルールは、HookやCIで決定論的に実装する。

## 導入の進め方

まず、1つの代表リポジトリで導入する。既存のテストコマンドと保護対象を整理し、キットの `CLAUDE.md` と `.claude` ディレクトリをコピーする。次に、対象を指定しないフルテストがブロックされ、対象単体テストは通ることを確認する。

全社展開の前に、代表タスクを固定し、初回フィードバック時間、テスト実行回数、連続失敗回数、残留プロセス、回帰検出率を導入前後で比較する。改善率を先に約束せず、実測で設定を調整することが重要である。

## 他ツールとの関係

Codex、Cursor、Google Antigravityなどにも、最小関連テスト、NFRの明示承認、停止条件、資源上限という考え方は応用できる。しかし、本キットの実装はClaude CodeのHooksを中心に構成されている。他ツールでは、それぞれの公式ルール・フック・CI機構で同じ原則を再実装する。

- **GitHub**: [kanautech/ai-agent-optimization-kit](https://github.com/kanautech/ai-agent-optimization-kit)
- **導入手順**: [`CLAUDE_CODE_INTEGRATION.md`](https://github.com/kanautech/ai-agent-optimization-kit/blob/master/CLAUDE_CODE_INTEGRATION.md)

## 参考資料

[1] [Claude Code: Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide)（取得日: 2026-08-17）
