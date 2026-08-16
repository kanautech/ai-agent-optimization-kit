# Claude Code TDD Guardrails Kit：導入・検証・ロールバック手順

## 1. このガイドの対象

本ガイドはClaude Codeを主対象とする。Claude Codeでは、`CLAUDE.md` に行動原則を置き、`.claude/settings.json` にHooksを登録することで、LLMへの指示と決定論的な実行制約を分離できる。[Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)

Codex、Cursor、Google Antigravityに適用する場合は、末尾の「他ツールへの応用」を参照し、それぞれの公式設定機構へ同じ原則を移植する。

## 2. 導入前の準備

導入する前に、次の4点を確認する。

| 確認項目 | 確認内容 |
|---|---|
| テストコマンド | 対象単体テスト、統合テスト、フルスイート、E2E、負荷テストの実行コマンドを区別する。 |
| NFRの責任者 | 性能・負荷・レース・セキュリティ結果を解釈できる人を決める。 |
| 保護対象 | `.env`、本番設定、ロックファイル、インフラ設定など、Claude Codeが通常は変更してはいけないファイルを列挙する。 |
| ベースライン | 代表タスクを選び、初回フィードバック時間、テスト回数、連続失敗回数、残留プロセスを記録する。 |

## 3. ファイルを配置する

キットから以下のファイルをコピーする。

```bash
mkdir -p .claude/hooks
cp /path/to/kit/CLAUDE.md ./CLAUDE.md
cp /path/to/kit/.claude/settings.json ./.claude/settings.json
cp /path/to/kit/.claude/hooks/pre_tool_guard.py ./.claude/hooks/pre_tool_guard.py
cp /path/to/kit/.claude/hooks/post_tool_audit.sh ./.claude/hooks/post_tool_audit.sh
chmod +x .claude/hooks/pre_tool_guard.py .claude/hooks/post_tool_audit.sh
```

`settings.json` に既存の `hooks` がある場合は、ファイル全体を置換しない。`PreToolUse` と `PostToolUse` を既存の `hooks` オブジェクトへ追加する。Claude Codeの `/hooks` で登録状況を確認する。

## 4. プロジェクト固有に調整する

### 4.1 `CLAUDE.md`

次の値をプロジェクトに合わせる。

- 標準のlint、型検査、対象単体テストのコマンド。
- 統合テストに上げる境界。
- フルスイートを実行してよいPR／リリースゲート。
- NFRテストを承認する担当者と合格基準。
- 保護すべきファイルとサービス。

### 4.2 `pre_tool_guard.py`

初期パターンは安全側である。プロジェクトに不要なツール名は削除し、実際に使う負荷・E2Eツールを追加する。`ALLOW_NFR_TESTS=1` は恒久設定にせず、承認済みの単発コマンドにだけ付与する。

```bash
# 明示承認済みの単発NFRテストだけを実行する例
ALLOW_NFR_TESTS=1 k6 run --vus 10 --duration 30s tests/load/smoke.js
```

この実行前に、対象環境、ワークロード、合格基準、上限時間、責任者をIssue、PR、または運用チケットへ残す。

## 5. Hooksの動作を確認する

### 5.1 ブロードなテストのブロック

Claude Codeに、対象を指定しないフルテストの実行を依頼する。`pre_tool_guard.py` が実行前にブロックし、最小関連テストまたは明示承認を求めるメッセージを返すことを確認する。

### 5.2 対象単体テストの許可

対象ファイルまたはテスト名を指定した単体テストを実行する。Hookにブロックされず、`.claude/audit/bash-commands.jsonl` にコマンド証跡が追加されることを確認する。

### 5.3 保護対象の追加

`PreToolUse` Hookを別途追加して、`.env`、本番設定、ロックファイルなどへの編集をブロックする。Claude Code公式の「Block edits to protected files」パターンを基礎にする。

## 6. 段階導入

| フェーズ | 対象 | 目的 | 判定 |
|---|---|---|---|
| Pilot | 1リポジトリ・代表タスク | Hookが開発を不必要に妨げないかを見る。 | ブロック誤検知、手動解除、テスト時間を記録する。 |
| Expand | 類似する2〜3リポジトリ | プロジェクト差を吸収する。 | ルールの例外が明文化できるかを見る。 |
| Standardize | チーム標準 | テンプレートの既定値を固定する。 | KPIと開発者フィードバックを月次で確認する。 |

## 7. ロールバック

Hookが正当なコマンドを過剰にブロックした場合、まずパターンを狭める。緊急時には `.claude/settings.json` の該当Hookをコメントアウトまたは削除してClaude Codeを再起動する。恒久的に `ALLOW_NFR_TESTS=1` を設定して回避してはいけない。

## 8. 他ツールへの応用

Codex、Cursor、Google AntigravityはClaude Codeと異なる製品であり、Hooks、設定形式、権限・承認モデルも異なる。`CLAUDE.md` とHookスクリプトをそのまま使用するのではなく、以下の原則を各製品の公式ルール・フック・CI設定へ移植する。

1. 最小関連テストから始める。
2. NFRを明示承認にする。
3. 同一失敗の反復を停止する。
4. 並列実行に資源予算を置く。
5. 実行したプロセスの証跡と後始末を残す。

## 参考資料

- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)（取得日: 2026-08-17）
- [Claude Code Settings](https://code.claude.com/docs/en/settings)（取得日: 2026-08-17）
- [Claude Code Memory / CLAUDE.md](https://code.claude.com/docs/en/memory)（取得日: 2026-08-17）
