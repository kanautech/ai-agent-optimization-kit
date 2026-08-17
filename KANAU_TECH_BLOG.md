---
title: "Claude Codeをチーム運用へ載せる：Hooksで実装するTDDガードレール"
description: "CLAUDE.mdとClaude Code Hooksを組み合わせ、過剰なNFRテストや盲目的なリトライを防ぎながら、AIエージェントの自律性を活かすための実装・運用ガイド。"
author: "Kanau Tech"
date: "2026-08-17"
tags: ["Claude Code", "Anthropic", "AI駆動開発", "TDD", "Developer Experience"]
---

# Claude Codeをチーム運用へ載せる：Hooksで実装するTDDガードレール

Claude Codeを開発フローに入れた組織が直面する論点は、モデルがコードを書けるかどうかではない。Claude Codeが、ファイル編集、ターミナル実行、テスト、ブラウザ操作までを一つのタスクとして扱えるとき、**どの操作を自律的に任せ、どの操作を明示的な人間判断へ戻すか**が開発速度と運用リスクを左右する。

Kanau Techが公開した [Claude Code TDD Guardrails Kit](https://github.com/kanautech/ai-agent-optimization-kit) は、この実行境界を実装するためのテンプレート集である。主対象はClaude Codeであり、`CLAUDE.md` に行動原則を、`.claude/settings.json` とHooksに決定論的な制約を置く。目的はClaude Codeを遅くすることでも、テストを減らすことでもない。**正しいテストを、正しい層で、正しいタイミングに実行すること**である。

## 問題の本質は「テスト量」ではなく「意思決定の未定義」

「実装して、テストして」という依頼は一見十分に見える。しかし、その中には複数の未定義な判断が含まれている。変更した関数の単体テストだけでよいのか。DBや外部APIの境界を跨ぐため統合テストが必要なのか。ブラウザE2Eまで必要なのか。性能、負荷、レースコンディションの検証を今このローカル環境で始める理由はあるのか。失敗が続いたら、Claude Codeはいつ止まり、誰が次の判断をするのか。

| 判断領域 | 境界がない場合の失敗モード | チームが定義すべきこと |
|---|---|---|
| 変更範囲 | 局所変更から無関係な統合・E2Eテストへ検証が拡張する。 | 変更モジュール、外部境界、対象ユーザーフロー。 |
| NFR | 負荷・ストレス・レース・セキュリティ検証が実装ループに混入する。 | 対象環境、シナリオ、合格基準、資源予算、責任者。 |
| 失敗時の停止 | 同じエラーに対する修正と再実行が反復する。 | リトライ上限、証拠保存、エスカレーション先。 |
| プロセス管理 | サーバー、ワーカー、ブラウザが残り、後続タスクを汚染する。 | 起動者、識別方法、後始末、タイムアウト。 |

これはClaude Code固有の欠陥を指摘するものではない。自律的な実行能力を持つエージェントへ、プロジェクト固有の判断境界を与えないことが問題である。

## `CLAUDE.md` とHooksを混同しない

Claude Codeにおける有効な統制は、自然言語の原則と決定論的な制約を分離することで実現する。

| 層 | Claude Codeでの実装 | 目的 |
|---|---|---|
| **Intent Layer** | `CLAUDE.md` | 目的、変更範囲、完了条件、最小関連テスト優先をClaude Codeへ伝える。 |
| **Safety Layer** | `.claude/settings.json`、`PreToolUse` Hook | 実行前に高コスト・高リスク操作を検査し、必要ならブロックする。 |
| **Feedback Layer** | `PostToolUse`、`Stop`、`Notification` Hooks、CI | 実行証跡、失敗根拠、通知、後始末を一貫して残す。 |

Claude CodeのHooksは、ライフサイクルの特定時点でユーザー定義コマンドを実行する公式機構である。ファイル編集後の整形、保護ファイルへの編集ブロック、コマンド検証、通知、コンテキスト再注入などを、LLMの任意判断に依存せず実装できる。[1]

> `CLAUDE.md` は「何を達成するか」を伝える。Hooksは「何を実行前に止めるか」「何を実行後に必ず残すか」を担保する。

## Kitが提供する最小構成

リポジトリには、次のClaude Code向けファイルを含めている。

```text
.
├── CLAUDE.md
└── .claude/
    ├── settings.json
    └── hooks/
        ├── pre_tool_guard.py
        └── post_tool_audit.sh
```

`CLAUDE.md` は、最小関連テストを先に実行すること、NFRテストをデフォルトで始めないこと、同じ失敗が連続したときは停止して証拠を提示することを定義する。`pre_tool_guard.py` は `PreToolUse` Hookとして働き、対象を指定しないフルテスト、負荷・ストレス・レーステスト、広範なブラウザテストを実行前に検査する。`post_tool_audit.sh` はBashコマンドの入力をJSONL形式で保存し、失敗が続いたときに根拠を追跡できるようにする。

以下は設定の最小例である。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre_tool_guard.py"
          }
        ]
      }
    ]
  }
}
```

このHookは「フルテストを永久に禁止する」ためのものではない。対象環境、ワークロード、合格基準、時間・並列度の予算、結果を解釈する責任者が明確な場合には、単発の承認として実行を許可する。重要なのは、例外を恒久的な抜け道に変えないことだ。

## 導入はPilotから始める

全リポジトリへの一括展開は、最も失敗しやすい導入方法である。まず、開発者がClaude Codeを日常利用しており、テスト構成が理解できる代表リポジトリを一つ選ぶ。そこへキットを配置し、既存コマンド・保護対象・NFR責任者をプロジェクトに合わせて調整する。

| 段階 | 実施内容 | 判定基準 |
|---|---|---|
| **Pilot** | `CLAUDE.md` とHooksを導入し、対象単体テストと対象なしフルテストの挙動を確認する。 | 正当なローカルテストを妨げず、未承認の広範テストを説明付きで止められる。 |
| **Measure** | 代表タスクを固定し、導入前後の実行履歴を比較する。 | 初回フィードバック時間、テスト回数、連続失敗、残留プロセス、回帰を記録する。 |
| **Standardize** | 例外パターンとプロジェクト設定をテンプレートへ反映する。 | 設定の理由を説明でき、チーム内で再利用できる。 |

特定の削減率や速度向上を先に約束してはいけない。効果はリポジトリ規模、テスト構成、Claude Codeの権限、CI、開発者の運用によって変わる。導入の成否は、代表タスクを使った再現可能な測定で判断する。

## 実装上の注意

Hookを強くしすぎると、正当な作業を止める。逆に緩すぎると、ガードレールの意味がない。最初は安全側の小さなパターンから始め、ブロック誤検知をIssueとして記録し、ルールをプロジェクト固有に調整する。

また、後始末Hookへ汎用的な `pkill` を入れてはいけない。他の開発者や別タスクが起動したプロセスを停止する危険がある。後始末は、Claude Codeが開始したプロセスだけを特定できるプロジェクト固有の方法で実装する。

## 他ツールとの関係

Codex、Cursor、Google Antigravityなどにも、最小関連テスト、NFRの明示承認、リトライ上限、資源予算という原則は応用できる。しかし、本キットの実装はClaude Codeの `CLAUDE.md`、`.claude/settings.json`、Hooksを中心に構成している。他の環境では、同じファイルやスクリプトをそのまま使うのではなく、公式のルール・フック・CI機構に原則を再実装する必要がある。

## 結論

Claude Codeをチーム開発で活かすために必要なのは、長大なプロンプトでも、無制限の自律実行でもない。目的と完了条件を明確にした `CLAUDE.md`、実行前後の重要な境界を担保するHooks、そして代表タスクでの実測である。

**Right Test. Right Layer. Right Time.**

- **GitHub**: [kanautech/ai-agent-optimization-kit](https://github.com/kanautech/ai-agent-optimization-kit)
- **導入ガイド**: [`CLAUDE_CODE_INTEGRATION.md`](https://github.com/kanautech/ai-agent-optimization-kit/blob/master/CLAUDE_CODE_INTEGRATION.md)

## 参考資料

[1] [Claude Code Docs: Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide)（取得日: 2026-08-17）  
[2] [Claude Code Docs: Settings](https://code.claude.com/docs/en/settings)（取得日: 2026-08-17）  
[3] [Claude Code Docs: How Claude remembers your project](https://code.claude.com/docs/en/memory)（取得日: 2026-08-17）
