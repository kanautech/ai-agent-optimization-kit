# Claude Code中心の情報設計方針

## 主対象

本キットの**主対象はClaude Code**である。理由は、Claude Codeがプロジェクト指示（`CLAUDE.md`）、設定ファイル（`.claude/settings.json`）、およびHooksを通じて、自然言語の行動原則と決定論的な実行制約を組み合わせられるためである。

Claude Code公式ドキュメントによれば、HooksはClaude Codeのライフサイクル上の特定ポイントでユーザー定義のコマンドを実行し、LLMの選択に依存せずに特定のアクションを必ず実行させるための機構である。ファイル編集後の整形、保護ファイルへの編集のブロック、コマンド検証、通知、コンテキスト再注入などに利用できる。[Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)（取得日: 2026-08-17）

## 推奨する構成

| 層 | Claude Codeでの主な実装場所 | 役割 |
|---|---|---|
| Intent Layer | `CLAUDE.md` | 目的、変更範囲、完了条件、テスト方針を短く定義する。 |
| Safety Layer | `.claude/settings.json` と `PreToolUse` Hooks | NFRテストの開始条件、保護対象、危険なコマンド、並列実行、実行予算を決定論的に制約する。 |
| Feedback Layer | `PostToolUse` / `Stop` / `Notification` Hooks とCI | 失敗証拠、プロセス後始末、停止・通知、レポートを一貫して行う。 |

## 補助的な適用先

Codex、Cursor、Google Antigravityは**互換・応用先**として扱う。製品ごとにルールの検出方法、フック、権限、モデル選択、実行環境が異なるため、`CLAUDE.md` やClaude Code Hooksの設定をそのまま移植できるとは限らない。導入時には各製品の公式ルール・設定・フック機構に、同じ原則を再実装する。

## 表記ルール

1. タイトル、導入手順、サンプルコード、検証プロトコルはClaude Codeを主語にする。
2. Codex、Cursor、Google Antigravityは「同様の原則を移植できるエージェント型環境」として注記する。
3. 特定ツールやモデルが特定の失敗モードを必ず起こすとは断定しない。
4. 性能改善は保証しない。各プロジェクトで測定するKPIとして扱う。
