---
title: "Codex・Cursor・Antigravityで使う：AIエージェントの過剰テストを防ぐTDDガードレール"
tags: AI, Codex, Cursor, TDD, 生産性向上
---

# Codex・Cursor・Antigravityで使う：AIエージェントの過剰テストを防ぐTDDガードレール

AIコーディングエージェントは、実装、テスト、CLI実行、ブラウザ操作までを一連のタスクとして扱えるようになった。OpenAI CodexはChatGPT・IDE・CLIで利用できるコーディングエージェントであり、CursorはDesktop・CLIを含むエージェント型開発環境、Google AntigravityはIDE・CLI・複数エージェント管理を備える開発プラットフォームである [1] [2] [3]。

この能力は有益だが、プロジェクトのスコープを明示しないと、AIエージェントが変更と無関係なテストまで拡張する。例えば、ユーティリティ関数の変更に対してフルE2E、負荷、並行性テストまで始めるなら、品質向上ではなく開発ループを遅くする。問題は「AIがテストをすること」ではない。**どのテストを、どの変更に対して、いつ実行するかが未定義なこと**である。

本稿では、Kanau Techが公開した [AI-Driven Development Optimization Kit](https://github.com/kanautech/ai-agent-optimization-kit) を用いて、AIエージェントの自律性を潰さずに過剰検証を抑える方法を説明する。

## 対象ツールと前提

| ツール | 公式上の位置付け | 本稿での扱い |
|---|---|---|
| Codex | OpenAIのソフトウェアエンジニアリング向けAIコーディングエージェント。 | エディタ・CLI・クラウド実行でのテスト範囲を制御する。 |
| Cursor | エージェント型コーディング環境。 | プロジェクト指示とエージェント実行の境界を定義する。 |
| Google Antigravity | エージェントファーストの開発プラットフォーム。 | 複数エージェントやバックグラウンド作業の資源上限を定義する。 |

各製品は別のサービスであり、同一モデルや同一の設定機構ではない。そのため、以下のテンプレートは**汎用原則**であり、各製品の公式ルール機構に合わせて移植する。

## まず実装するべき5つのガードレール

### 1. Smallest Test First

変更した関数・モジュールに直接関連する単体テスト、型検査、lintから始める。統合テストへ広げるのは、モジュール境界・永続化・外部APIなどを実際に跨いだときだけにする。

```markdown
- Start with linting, type-checking, and the smallest test directly related to the change.
- Expand to integration tests only when the change crosses a module or service boundary.
- Reserve the full test suite for PR merge or release gates.
```

### 2. NFRは明示的な人間判断で開始する

性能・負荷・ストレス・レースコンディション・侵入テストは、機能実装の副産物として自動開始してはいけない。開始前に、対象環境、シナリオ、合格基準、許容資源を人間が決める。

```markdown
- Do not start load, stress, race, or full E2E tests by default.
- Require an explicit request specifying target environment, workload, acceptance criteria, and budget.
```

### 3. 同一失敗のリトライに上限を設ける

同じテストが連続失敗しているなら、追加の再試行は証拠を増やさない。3回を上限に止め、ログ、再現手順、仮説を提示させる。

```markdown
- After 3 consecutive failures of the same test, stop.
- Report the failing command, error output, environment facts, and root-cause hypothesis.
- Do not modify assertions merely to make the suite green.
```

### 4. 並列化は許可制にする

複数のエージェントやテストワーカーを利用できる環境では、並列化がCPU・メモリ・ポート競合・テストデータ競合を引き起こす。初期値を逐次実行にし、独立性が確認できるときだけ並列化する。

### 5. 終了時のプロセス後始末をルール化する

ブラウザ、開発サーバー、ワーカー、コンテナが残ると、後続タスクの失敗原因になる。実行したプロセスを記録し、成功・失敗のどちらでも終了確認を行う。

## 導入手順

リポジトリのルートにテンプレートを配置する。

```bash
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/AGENTS.md -o AGENTS.md
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/GUARDRAILS.md -o GUARDRAILS.md
```

次に、使用中のCodex、Cursor、Antigravity、Claude Code等がプロジェクト内の指示ファイルを認識するかを確認する。認識しない場合は、各製品の公式ルール設定へ内容を移植する。テンプレートの数値上限（例：リトライ3回、最大並列数2）は初期値であり、CIの所要時間、CPU、失敗率、開発者体験を測定して調整する。

## 数字の扱いを間違えない

「プロンプトを何%削除すれば速くなる」「CPUを何%削減できる」といった数字は、製品横断の保証値ではない。モデル、リポジトリ規模、依存関係、テスト構成、実行権限によって結果が変わる。導入効果は、代表タスクを使い、導入前後で次の値を測って判断する。

| 指標 | 測定方法 |
|---|---|
| 変更から最初の有効なフィードバックまでの時間 | lint・型検査・対象単体テストの完了時間を記録する。 |
| 1タスクあたりのテスト実行回数 | テストコマンド履歴から集計する。 |
| 同一障害の連続リトライ数 | 同じ失敗シグネチャの連続回数を数える。 |
| 残留プロセス数 | タスク終了時にワーカー・ブラウザ・サーバーを確認する。 |

本キットはAIの能力を制限するためではなく、テストを**正しい層、正しいタイミング、正しい範囲**に戻すためのテンプレートである。

## リンク

- [Kanau Tech / AI-Driven Development Optimization Kit](https://github.com/kanautech/ai-agent-optimization-kit)

## 参考資料

[1] [OpenAI: Codex](https://openai.com/codex/)（取得日: 2026-08-17）  
[2] [Cursor: AI Coding Agent](https://cursor.com/)（取得日: 2026-08-17）  
[3] [Google Antigravity](https://antigravity.google/)（取得日: 2026-08-17）
