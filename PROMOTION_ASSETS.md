# プロモーション用アセット案（Claude Code主対象）

## 1. アイキャッチ画像構成

### 案A：Qiita / Zenn向け — Claude Code Hooksの技術性を強調

| 要素 | 構成 |
|---|---|
| コンセプト | `CLAUDE.md` とHooksで、AIの自律性と実行境界を両立する。 |
| ビジュアル | 左に `CLAUDE.md`、中央に `PreToolUse Hook`、右に `PostToolUse Hook` を置き、オレンジの矢印で `PLAN → GUARD → EVIDENCE` を接続する。 |
| メインコピー | `Claude Codeを縛らず、過剰テストを止める。` |
| サブコピー | `CLAUDE.md + Hooks = Deterministic TDD Guardrails` |
| 配色 | 背景 `#1A1A1A`、文字 `#FFFFFF`、アクセント `#F26D21`。 |
| 推奨サイズ | 1200 × 630 px（OGP / X / LinkedIn）。 |

### 案B：Kanau Techブログ向け — 開発ガバナンスを強調

| 要素 | 構成 |
|---|---|
| コンセプト | テストを減らすのではなく、実行の意思決定を設計する。 |
| ビジュアル | 左にClaude Codeのタスクフロー、中央に「Human Decision Gate」、右にテストピラミッドを配置する。 |
| メインコピー | `Right Test. Right Layer. Right Time.` |
| サブコピー | `Claude Code TDD Guardrails Kit by Kanau Tech` |
| 配色 | 背景 `#E8F4F1`、メイン `#0A4731`、アクセント `#F26D21`。 |
| 推奨サイズ | 1600 × 900 px（ブログヒーロー・社内スライド）。 |

### 表記ルール

Claude Codeを主対象として表示する。Codex、Cursor、Google Antigravityのロゴ・名称は互換・応用先を説明する必要がある場合だけ、各ベンダーのブランドガイドラインに従って記載する。再現可能なKanau Tech固有の測定値がない限り、削減率やCPU使用率などの数値を画像に載せない。

## 2. チーム共有メッセージ案（Slack / Discord / Teams）

> **件名：Claude Code TDD Guardrails Kit の試験導入とフィードバック募集**
>
> チーム各位
>
> Claude Codeでの開発において、変更と無関係なフルE2E・負荷・レーステストや、同一障害の盲目的な再試行を防ぐため、**Claude Code TDD Guardrails Kit** を公開しました。
>
> このキットは、`CLAUDE.md` で目的・変更範囲・完了条件を明確にし、`.claude/settings.json` とHooksで高リスク操作を実行前に検査するものです。AIの実装・調査・デバッグ能力を抑えることが目的ではありません。人間が決めるべきNFR・資源・停止条件を明文化することが目的です。
>
> **Pilot導入手順**
> 1. 代表リポジトリに `CLAUDE.md` と `.claude` ディレクトリをコピーする。
> 2. 対象を指定しないフルテストがブロックされ、対象単体テストが許可されることを確認する。
> 3. 代表タスクで、初回フィードバック時間・テスト回数・連続失敗回数・残留プロセスを記録する。
>
> - **GitHub**: https://github.com/kanautech/ai-agent-optimization-kit
> - **導入手順**: `CLAUDE_CODE_INTEGRATION.md`
> - **Kanau Tech Blog**: <公開URL>
>
> Hookの誤検知や、プロジェクト固有のテスト運用に合わない点は、Issueで具体的なコマンド・ログ・期待動作とともに報告してください。
