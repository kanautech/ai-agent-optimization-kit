# AI駆動開発のガバナンス：Codex・Cursor・Google Antigravityで「正しいテスト」を実行する

> **著者**: Kanau Tech  
> **公開日**: 2026-08-17  
> **OSS**: [kanautech/ai-agent-optimization-kit](https://github.com/kanautech/ai-agent-optimization-kit)

## AIコーディングの次の論点は「実行境界」である

AIコーディングは、補完やチャットの段階を超えた。OpenAI CodexはChatGPT、IDE、CLIで利用できるソフトウェアエンジニアリング向けコーディングエージェントである [1]。CursorはDesktopやCLIを含むエージェント型コーディング環境であり [2]、Google AntigravityはIDE、CLI、SDK、複数エージェント管理を備えるエージェントファーストの開発プラットフォームである [3] [4]。

これらの環境で重要なのは、どのモデルが最も強いかという表層的な比較ではない。コード生成、テスト、コマンド実行、ブラウザ操作、バックグラウンド作業まで可能なエージェントに対し、**どの権限で、どの検証を、どの終了条件まで実行させるか**を設計することである。

Kanau Techは、この実行境界を定義するための [AI-Driven Development Optimization Kit](https://github.com/kanautech/ai-agent-optimization-kit) を公開した。本キットは特定のAIモデルや特定製品の性能を主張するものではない。Codex、Cursor、Google Antigravity、Claude Codeなど、複数のエージェント型開発環境で使える運用原則とテンプレートを提供する。

## 問題は「テストが多いこと」ではない

テストは品質の根幹である。問題は、機能変更に対してどこまで検証を広げるか、NFRをいつ始めるか、失敗時にいつ停止するかが未定義なことである。

| 未定義の事項 | 起こり得る問題 | 必要な判断 |
|---|---|---|
| 変更の影響範囲 | 局所的変更から、無関係な統合・E2Eへ検証が拡張する。 | 変更モジュール、外部境界、対象ユーザーフローを定義する。 |
| NFRテストの開始条件 | 負荷・ストレス・レース検証が実装ループに混入する。 | 対象環境、ワークロード、合格基準、資源予算を定める。 |
| 失敗時の終了条件 | 同じ障害への修正・再試行を反復する。 | リトライ上限、ログ保存、エスカレーションを定める。 |
| 並列実行条件 | CPU・メモリ・ポート・テストデータが競合する。 | タスクの独立性と資源予算を確認してから並列化する。 |

この問題は、製品固有の欠陥と決めつけるべきではない。高い自律性と広い実行権限を持つエージェントに、プロジェクト文脈に沿った判断境界が必要だという設計課題である。

## Kanau Techの3層ガードレール

### Intent Layer：目的・範囲・完了条件を短く明確にする

エージェントには「どの設計を採用するか」「どのファイルを読むか」まで過度に固定せず、何を変更し、何を完了とするかを明記する。目的が明確であれば、実装・調査・局所デバッグには自律性を残せる。

### Safety Layer：NFRと資源使用を明示承認にする

負荷、ストレス、レース、セキュリティ、フルE2E検証は、対象・合格基準・予算が指定されたときに開始する。最大リトライ、並列度、タイムアウト、ネットワークアクセス、本番アクセス、プロセス後始末もここで定義する。

### Feedback Layer：盲目的な再試行を証拠ベースの判断へ変える

同じ障害が連続する場合、エージェントは止まり、失敗コマンド、ログ、環境の観測事実、原因仮説、判断が必要な点を提示する。人間は、リスク受容と次の方針を決める。

## 導入方法

```bash
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/AGENTS.md -o AGENTS.md
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/GUARDRAILS.md -o GUARDRAILS.md
```

使用中のエージェント環境がこれらのファイルを読み込むか確認し、認識しない場合は公式ルール機構へ内容を移植する。最初は代表リポジトリの代表タスクで導入し、全社標準化は測定後に行う。

## 効果は約束せず、測る

本キットは「何%の速度向上」や「何%のコスト削減」を保証しない。効果はモデル、リポジトリ規模、テスト構成、実行権限、チーム運用に依存する。導入前後で、初回フィードバック時間、テスト実行回数、同一障害の連続失敗回数、残留プロセス、PRでの回帰検出率を比較し、ルールを改善していく。

> 目的はテストを減らすことではない。**正しいテストを、正しい層で、正しいタイミングに実行すること**である。

## Tiếng Việt — Tóm tắt

Các môi trường phát triển có tác tử AI như Codex, Cursor, Google Antigravity và Claude Code có thể lập trình, chạy test, thực thi CLI và xử lý tác vụ nền. Vì thế, vấn đề quan trọng không phải là chọn “model mạnh nhất”, mà là thiết kế ranh giới thực thi: AI được chạy kiểm thử nào, trong điều kiện nào, với điểm dừng nào.

**AI-Driven Development Optimization Kit** của Kanau Tech cung cấp các nguyên tắc trung lập theo nhà cung cấp: bắt đầu từ test nhỏ nhất liên quan trực tiếp đến thay đổi, chỉ chạy NFR khi con người đã xác định mục tiêu và tiêu chí chấp nhận, giới hạn retry, và luôn lưu bằng chứng trước khi yêu cầu quyết định tiếp theo.

## 参考資料

[1] [OpenAI: Codex](https://openai.com/codex/)（取得日: 2026-08-17）  
[2] [Cursor: AI Coding Agent](https://cursor.com/)（取得日: 2026-08-17）  
[3] [Google Antigravity](https://antigravity.google/)（取得日: 2026-08-17）  
[4] [Google Antigravity: Introducing Google Antigravity](https://antigravity.google/blog/introducing-google-antigravity)（取得日: 2026-08-17）
