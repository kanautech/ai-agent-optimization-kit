---
title: "Claude CodeのHooksで『対象なしフルテスト』を止める：TDDガードレール実装ガイド"
tags: ClaudeCode, Anthropic, TDD, Testing, AIAgent
private: false
updated_at: "2026-08-17"
---

# Claude CodeのHooksで「対象なしフルテスト」を止める：TDDガードレール実装ガイド

Claude Codeに「実装してテストして」と頼んだとき、対象の単体テストで止まるか、リポジトリ全体のテストやブラウザE2Eまで広がるかは、依頼文、プロジェクト文脈、利用可能なコマンドに左右される。ここで必要なのは、AIに「慎重に」と頼むことではない。**どの操作をClaude Codeが自律的に実行してよいかを、プロジェクト側で決めること**である。

Claude Codeには、ライフサイクル上の特定時点でユーザー定義コマンドを実行するHooksがある。`PreToolUse` Hookを使えば、Bash実行の直前にコマンドを検査し、対象なしのフルテストや未承認の負荷テストをブロックできる。[1]

この記事では、Kanau Techの [Claude Code TDD Guardrails Kit](https://github.com/kanautech/ai-agent-optimization-kit) を基に、`CLAUDE.md` とHooksで「最小関連テストから始める」ルールを実装する。

## 結論：プロンプトとHooksを役割分担させる

| 役割 | 実装場所 | 例 |
|---|---|---|
| Claude Codeに判断を伝える | `CLAUDE.md` | 「変更に直接関係する最小テストから開始する」 |
| 実行前に機械的に止める | `PreToolUse` Hook | `npm test`、`k6 run`、広範なE2Eを検出してブロックする。 |
| 実行後の証拠を残す | `PostToolUse` Hook | 実行されたBashコマンドをJSONLへ記録する。 |
| 品質を最終判定する | CI | PR・リリースゲートでフルスイートを実行する。 |

`CLAUDE.md` は指示であり、Hooksは強制力を持つ実行境界である。この二つを混同すると、「止めたい操作」をLLMの確率的な判断に委ねることになる。

## 1. `CLAUDE.md` にテスト方針と停止条件を書く

リポジトリルートに `CLAUDE.md` を置き、まず以下のような原則を定義する。

```markdown
## Default Test Strategy

1. Read the affected code and existing tests before modifying files.
2. Start with linting, type-checking, and the smallest test directly related to the change.
3. Expand to integration tests only when the change crosses a module, persistence, network, or service boundary.
4. Reserve the full suite for an explicit PR, release, or CI gate request.

## Failure Handling

- Never retry the same failing test blindly.
- After three consecutive failures with the same failure signature, stop execution.
- Preserve the failing command, error output, relevant environment facts, and a root-cause hypothesis.
```

ここでの目的は、Claude Codeの実装やデバッグ手順を過剰に固定することではない。目的、変更範囲、テストの拡張条件、停止条件だけを明示する。

## 2. Hookを登録する

プロジェクトに `.claude/settings.json` を作成する。既存の `hooks` 設定がある場合は、オブジェクト全体を置換せず、`PreToolUse` と `PostToolUse` を追加する。

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
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/post_tool_audit.sh"
          }
        ]
      }
    ]
  }
}
```

Claude Codeでは `/hooks` により、設定済みHookの登録状況を確認できる。[1]

## 3. `PreToolUse` Hookで広範なテストを判定する

次のPythonスクリプトは、Hookから標準入力として渡されるJSONを読み、Bashコマンドを判定する最小例である。

```python
#!/usr/bin/env python3
import json
import os
import re
import sys

payload = json.load(sys.stdin)
command = payload.get("tool_input", {}).get("command", "")
normalized = command.lower()

nfr_patterns = [
    r"\bk6\b", r"\blocat\b", r"\blocust\b", r"\bartillery\b",
    r"\bwrk\b", r"\bvegeta\b", r"--race\b",
    r"playwright\s+test(?!\s+[^\n]*--grep)",
    r"cypress\s+run(?!\s+[^\n]*--spec)",
]
broad_test_patterns = [
    r"\bnpm\s+test\s*$", r"\bpnpm\s+test\s*$",
    r"\byarn\s+test\s*$", r"\bpytest\s*$",
]

if os.getenv("ALLOW_NFR_TESTS") == "1":
    sys.exit(0)

if any(re.search(p, normalized) for p in nfr_patterns + broad_test_patterns):
    print(
        "Blocked: run the smallest relevant test first. "
        "NFR/full-suite runs require explicit approval.",
        file=sys.stderr,
    )
    sys.exit(2)

sys.exit(0)
```

`exit 2` はHookのブロックに使う。ブロックのメッセージはClaude Codeへ返されるため、「何が足りないか」を具体的に説明する。プロジェクトごとに利用しているテストツールへパターンを調整すること。

## 4. NFRテストは「明示承認」の単発例外にする

負荷、ストレス、レース、セキュリティ、フルE2Eを禁止するわけではない。問題は、対象や合格基準がないまま実装タスクの副産物として始めることである。

NFRを実行する前に、次の項目をIssue、PR、または運用チケットへ残す。

| 項目 | 例 |
|---|---|
| 対象環境 | staging、固定データセット、隔離DB。 |
| シナリオ | 10 VUで30秒、特定APIへ一定割合の書込み。 |
| 合格基準 | p95、エラー率、データ整合性、許容リソース。 |
| 実行予算 | 最大5分、並列数、利用可能な環境。 |
| 責任者 | 結果を解釈し、次の改善を決める担当者。 |

条件が満たされた単発の実行にだけ、`ALLOW_NFR_TESTS=1` を付与する。

```bash
ALLOW_NFR_TESTS=1 k6 run --vus 10 --duration 30s tests/load/smoke.js
```

これは恒久的な環境変数にしてはいけない。例外が既定値になれば、ガードレールは消える。

## 5. `PostToolUse` Hookで実行証跡を残す

連続失敗が起きたときに必要なのは、もう一度同じコマンドを走らせることではない。何を実行したか、どのエラーが出たか、環境がどうだったかという証拠である。

```bash
#!/usr/bin/env bash
set -euo pipefail

AUDIT_DIR="${CLAUDE_PROJECT_DIR}/.claude/audit"
mkdir -p "${AUDIT_DIR}"
cat >> "${AUDIT_DIR}/bash-commands.jsonl"
```

汎用的な `pkill` を後始末Hookに入れるのは避ける。他の開発者や別タスクが開始したプロセスまで停止するおそれがある。後始末は、Claude Codeが開始したプロセスだけを識別できるプロジェクト固有の仕組みで実装する。

## 6. 導入後に測るもの

「Hooksでトークンが何%減る」といった数字を先に約束するのは誤りである。モデル、リポジトリ規模、CI、テスト構成、作業内容で結果は変わる。代表タスクを固定し、導入前後を比較する。

| KPI | 見るもの |
|---|---|
| 初回フィードバック時間 | lint・型検査・対象単体テストが完了するまでの時間。 |
| テスト実行回数 | 1タスクあたりに実行されたコマンド数。 |
| 同一失敗の連続回数 | 同じエラーシグネチャの反復数。 |
| 残留プロセス | サーバー、ワーカー、ブラウザの残存数。 |
| 回帰検出率 | PR・リリースゲートで発見された回帰。 |

## まとめ

Claude Codeの自律性を活かすには、実装・調査・局所デバッグの裁量を残し、NFR、広範テスト、資源予算、停止条件のようなリスク受容を明示する必要がある。

**`CLAUDE.md` で意図を伝え、Hooksで重要な境界を実装する。**

- [Claude Code TDD Guardrails Kit](https://github.com/kanautech/ai-agent-optimization-kit)
- [詳細導入ガイド](https://github.com/kanautech/ai-agent-optimization-kit/blob/master/CLAUDE_CODE_INTEGRATION.md)

## 参考資料

[1] [Claude Code Docs: Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide)（取得日: 2026-08-17）  
[2] [Claude Code Docs: Settings](https://code.claude.com/docs/en/settings)（取得日: 2026-08-17）
