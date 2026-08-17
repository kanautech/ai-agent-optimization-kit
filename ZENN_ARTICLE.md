---
title: "Claude Codeの自律性を壊さないTDDガバナンス：CLAUDE.mdとHooksの設計原則"
emoji: "🧭"
type: "tech"
topics: ["claudecode", "anthropic", "aiagent", "testing", "devex"]
published: false
---

# Claude Codeの自律性を壊さないTDDガバナンス：CLAUDE.mdとHooksの設計原則

Claude Codeの価値は、コード補完の精度だけではない。リポジトリを読み、変更を計画し、ファイルを編集し、テストを実行し、必要に応じてブラウザやCLIを使う。この一連の実行能力があるからこそ、AIコーディングの設計対象は「プロンプト」から**実行ガバナンス**へ移る。

本稿が扱う問いは単純である。

> Claude Codeに実装・調査・局所デバッグの裁量を残しながら、負荷試験、フルE2E、無制限リトライ、プロセス残留のような高コスト操作を、どう統制するか。

Kanau Techの [Claude Code TDD Guardrails Kit](https://github.com/kanautech/ai-agent-optimization-kit) は、この問いに対して `CLAUDE.md` とClaude Code Hooksを役割分担させる。

## 自然言語のルールだけでは統制できない理由

次の依頼を考える。

```text
この機能を実装して、必要なテストをして。
```

この文は目的を伝えているが、実行境界を伝えていない。「必要なテスト」は、対象単体テスト、統合テスト、ブラウザE2E、性能試験、負荷試験のどこまでを含むのか。失敗が続いた場合に、何回まで再試行してよいのか。外部サービスや本番相当データへ触れてよいのか。

Claude Codeの振る舞いを個別モデルの性質として語るのは不正確である。問題は、実行可能なツールと権限が与えられたエージェントへ、プロジェクト固有のリスク境界を与えないことにある。

| 境界がない判断 | 起こり得る実行 | 失われるもの |
|---|---|---|
| テスト範囲 | 局所変更から広範な統合・E2Eへ拡張する。 | 初回フィードバックの速度。 |
| NFR開始条件 | 負荷・レース・ストレス検証を開始する。 | 実行資源と結果の解釈可能性。 |
| 停止条件 | 同じ失敗を反復する。 | 時間と原因分析の質。 |
| 後始末 | サーバー、ワーカー、ブラウザが残る。 | 後続タスクの再現性。 |

## 3層アーキテクチャ：Intent / Safety / Feedback

本キットは、意思決定を3層に分ける。

### Intent Layer：`CLAUDE.md`

Intent Layerは、Claude Codeに解法を細かく指定する場所ではない。何を変更するか、何を完了とするか、どのテスト層から始めるかを高シグナルに記述する。

```markdown
## Default Test Strategy

1. Start with linting, type-checking, and the smallest test directly related to the change.
2. Expand to integration tests only when the change crosses a module, persistence, network, or service boundary.
3. Reserve the full suite for an explicit PR, release, or CI gate request.
```

このルールが与えるのは、手順書ではなく判断の優先順位である。Claude Codeは実装・調査・局所デバッグの方法を選べるが、検証を広げる条件は明確になる。

### Safety Layer：`PreToolUse` Hook

Safety Layerは、曖昧さを残してはいけない操作を扱う。Claude CodeのHooksは、ライフサイクルの特定時点でユーザー定義コマンドを実行できるため、LLMの任意判断に依存せずにコマンド検査やブロックを実装できる。[1]

`PreToolUse` HookをBashに設定し、次のような操作を実行前に判定する。

- 対象を指定しない `npm test`、`pytest` などのフルテスト。
- `k6`、`locust`、`artillery`、`wrk` などを用いた負荷テスト。
- 絞り込みのないブラウザE2E。
- プロジェクトで定義した危険な削除、デプロイ、本番アクセス。

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

ここでの原則は「広範テストは悪」ではない。NFRやフルスイートには、対象環境、ワークロード、合格基準、資源予算、責任者という人間の判断が必要である、ということだ。

### Feedback Layer：`PostToolUse`、Stop、CI

Feedback Layerでは、実行後の事実を残す。連続失敗が発生したとき、価値があるのは再試行の回数ではなく、失敗コマンド、標準エラー、環境情報、根本原因仮説である。

`PostToolUse` HookでBash実行のJSON入力をJSONLへ追記すれば、どのコマンドがいつ使われたかを追跡できる。さらに、プロジェクト固有のStop HookやCIで、残留プロセスの確認、テスト要約、失敗エビデンスの保存を実装する。

> 重要な制約はLLMへの依頼ではなく、Hook・CI・サンドボックスという決定論的な層で実装する。

## NFRの明示承認は「例外」ではなく責任分界

負荷・性能・セキュリティの検証を行わない、という主張ではない。むしろ、それらは重要だからこそ、機能実装の副産物として無目的に実行してはいけない。

| 必要な情報 | なぜ必要か |
|---|---|
| 対象環境 | 本番影響、データ、ネットワーク条件を明確にする。 |
| シナリオ | 何を再現し、何を検証するかを固定する。 |
| 合格基準 | p95、エラー率、整合性など、結果を判定可能にする。 |
| 資源予算 | 実行時間、並列数、インフラ費用を制御する。 |
| 責任者 | 失敗・成功後の意思決定を担う人を明確にする。 |

これらが満たされた場合だけ、`ALLOW_NFR_TESTS=1` のような単発許可でHookを通す。恒久的な許可に変えれば、設計したSafety Layerは形骸化する。

## ガードレールの評価は、削減率ではなく品質と再現性で行う

「Hookを入れればトークンやCPUが何%減る」といった数字を一般化してはいけない。効果は、リポジトリ規模、テスト構成、Claude Codeの設定、CI、チームの運用で変わる。

導入の評価には、代表タスクを固定した前後比較が必要である。

| KPI | 目的 |
|---|---|
| 初回フィードバック時間 | 最小テスト戦略が開発ループを妨げていないかを見る。 |
| テスト実行回数 | 失敗に対する無目的な反復を検出する。 |
| 同一エラーの連続回数 | サーキットブレーカーの妥当性を確認する。 |
| 残留プロセス | 後続タスクを汚染していないかを見る。 |
| PR・リリース時の回帰 | テスト範囲を絞っても品質を毀損していないかを確認する。 |

## Claude Code以外への適用

Codex、Cursor、Google Antigravityなどにも、この設計原則は応用できる。しかし、このキットはClaude Codeの `CLAUDE.md`、`.claude/settings.json`、Hooksを主対象に実装している。他の環境では、ファイルをコピーするのではなく、各製品が提供する公式のルール、Hook、権限、CI機構へ同じ判断境界を移植するべきである。

## 結論

Claude Codeの自律性を活かすことと、実行を統制することは対立しない。実装・調査・局所デバッグには裁量を残す。NFR、広範テスト、資源予算、停止条件には明示的な人間判断を置く。その役割分担を `CLAUDE.md` とHooksで実装する。

**Right Test. Right Layer. Right Time.**

- [Claude Code TDD Guardrails Kit](https://github.com/kanautech/ai-agent-optimization-kit)
- [導入・検証・ロールバック手順](https://github.com/kanautech/ai-agent-optimization-kit/blob/master/CLAUDE_CODE_INTEGRATION.md)

## 参考資料

[1] [Claude Code Docs: Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide)（取得日: 2026-08-17）  
[2] [Claude Code Docs: Settings](https://code.claude.com/docs/en/settings)（取得日: 2026-08-17）  
[3] [Claude Code Docs: How Claude remembers your project](https://code.claude.com/docs/en/memory)（取得日: 2026-08-17）
