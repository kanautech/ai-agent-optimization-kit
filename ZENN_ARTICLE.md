---
title: "Claude CodeのHooksで実装するTDDガバナンス：自律性を保ち、過剰検証を止める"
emoji: "🪝"
type: "tech"
topics: ["claudecode", "anthropic", "tdd", "agent", "testing"]
published: false
---

# Claude CodeのHooksで実装するTDDガバナンス：自律性を保ち、過剰検証を止める

AIコーディングエージェントを扱うとき、ルールをプロンプトに書けば統制できるという前提は脆い。特にClaude Codeは、プロジェクト内のファイルを読み書きし、Bashコマンドを実行し、テストやブラウザ操作までを自律タスクとして進められる。自然言語の依頼だけに依存するなら、どのテストを走らせるか、いつ止めるか、何を保護するかはLLMの判断に委ねられる。

Claude Codeには、この問題を解く公式の手段がある。**Hooks**である。HooksはClaude Codeのライフサイクル上の特定時点でユーザー定義のコマンドを実行し、LLMの任意判断ではなく決定論的に検証・ブロック・記録を行える [1]。

本稿では、Kanau Techが公開した [Claude Code TDD Guardrails Kit](https://github.com/kanautech/ai-agent-optimization-kit) の設計を通じて、Claude Codeの自律性とTDDガバナンスを両立させる方法を説明する。

## プロンプトとHooksを混同しない

| 層 | Claude Codeでの実装 | 向いている判断 |
|---|---|---|
| Intent Layer | `CLAUDE.md` | 目的、変更範囲、完了条件、テスト方針。 |
| Safety Layer | `.claude/settings.json` と `PreToolUse` Hook | 危険なコマンド、保護対象、NFRの開始条件。 |
| Feedback Layer | `PostToolUse` / `Stop` / `Notification` Hook | 実行証跡、失敗根拠、終了通知、後始末。 |

`CLAUDE.md` は「何を達成したいか」をClaudeに伝える。Hooksは「何を実行させないか」「何を必ず記録するか」を担保する。両者を混ぜると、重要な安全境界まで確率的な指示追従へ委ねることになる。

## NFRを実装ループから分離する

次のような依頼は判断境界が足りない。

> 「この機能を実装して、十分にテストして。」

十分とは何か。単体テストか、統合テストか、ブラウザE2Eか、負荷試験か。MVPのローカル環境でレースコンディションまで検証するのか。合格基準は何か。結果を誰が解釈するのか。

NFRは機能実装の自動的な副産物ではない。性能、負荷、ストレス、レース、セキュリティ検証を始めるには、少なくとも次の5項目が必要である。

1. 対象環境。
2. ワークロードまたは攻撃シナリオ。
3. 合格基準。
4. 時間・並列度・インフラの資源予算。
5. 結果を解釈し次の判断を行う人間の責任者。

## `PreToolUse` Hookで実行前に止める

Claude Codeの `PreToolUse` Hookは、Bash、Edit、Writeなどの実行前にコマンドを検査できる。キットの `pre_tool_guard.py` は、対象指定のないフルテスト、NFRテストツール、広範なブラウザテストを検出し、明示承認がない限りブロックする。

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

ブロックは絶対的な禁止ではない。対象環境、合格基準、予算、責任者が明確な場合に限り、単発の承認として `ALLOW_NFR_TESTS=1` を付けて実行する。恒久的な環境変数にしてはいけない。

## `PostToolUse` Hookで証拠を残す

実行後は、コマンドと結果を記録する。これは監視のためだけではない。連続失敗が起きたとき、同じコマンドを繰り返すのではなく、実行履歴とエラー証拠から根本原因を切り分けるためである。

さらに、プロジェクト固有のHookを追加して、Claude Codeが開始した開発サーバー、ワーカー、ブラウザの後始末を実装する。ただし、汎用的な `pkill` をHookへ入れてはならない。人間や他のタスクが開始したプロセスを誤って停止させるからである。

## 効果の評価は実測で行う

「Hooksを入れればコストが何%下がる」と約束するべきではない。測るべきは、初回フィードバック時間、テスト実行回数、同一失敗の連続回数、残留プロセス、PRでの回帰検出率である。代表タスクを固定した導入前後比較によって、チームの設定が自律性を壊さず、無駄な反復を減らしているかを判断する。

Codex、Cursor、Google Antigravityにも同じ原則は応用できる。しかし本キットはClaude Codeの `CLAUDE.md`、`.claude/settings.json`、Hooksを主対象に設計している。他の環境では、公式のルール・フック・CI機構に同じ境界を再実装すること。

## 参考資料

[1] [Claude Code: Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide)（取得日: 2026-08-17）  
[2] [Claude Code: Settings](https://code.claude.com/docs/en/settings)（取得日: 2026-08-17）
