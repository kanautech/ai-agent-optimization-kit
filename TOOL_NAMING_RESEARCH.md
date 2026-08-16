# AIコーディング環境の公式表記メモ

取得日: 2026-08-17 (JST)

| 製品・環境 | 公式上の位置付け | 公開物で推奨する表記 |
|---|---|---|
| OpenAI Codex | OpenAIはCodexをソフトウェアエンジニアリング向けのAI coding agentとして案内し、ChatGPT、IDE、CLIで利用できるとしている。 | `CodexなどのAIコーディングエージェント` |
| Cursor | Cursorは自社を「ambitious softwareを構築するためのcoding agent」と位置付け、Desktop、CLI、エージェント機能を提供している。 | `Cursorなどのエージェント型開発環境` |
| Google Antigravity | GoogleはAntigravityを、複数のローカルエージェントを管理できるagentic development platformとして案内している。 | `Google Antigravityなどのエージェント型開発プラットフォーム` |

公開文書の注意点:

1. Codex、Cursor、Antigravityは製品・サービス・開発環境の名称であり、特定の単一モデルの同義語として書かない。
2. 各製品で利用可能なモデル、ツール、権限、実行環境、設定ファイルの解釈は変わる。従って、キットは`AI coding agents`向けの汎用ガードレールとして説明する。
3. `CPU使用率99%`、`トークン消費量50%削減`、`80%削除`は一般化された製品性能ではない。個別環境で測定する仮説・目標・事例として分離する。

## 公式ソース

- OpenAI, Codex: https://openai.com/codex/
- Cursor, AI Coding Agent: https://cursor.com/
- Google Antigravity: https://antigravity.google/

## ソースメモ

OpenAIのCodex公式ページとCursor公式ページをブラウザで確認した。Google Antigravityについては公式ドメインを検索結果で確認し、公式説明が「agentic development platform」であることを確認した。
