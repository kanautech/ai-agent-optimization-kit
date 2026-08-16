# Claude Codeの自律性を活かしながら、過剰テストを止める：TDD Guardrails Kitを公開

> **著者**: Kanau Tech  
> **公開日**: 2026-08-17  
> **GitHub**: [kanautech/ai-agent-optimization-kit](https://github.com/kanautech/ai-agent-optimization-kit)

Claude Codeは、コードを書くだけの補助ツールではない。ファイル編集、ターミナル実行、テスト、ブラウザ操作、バックグラウンド作業までをタスクとして扱えるAIコーディングエージェントである。だからこそ、チームが設計すべき対象は「どのモデルが賢いか」ではなく、**Claude Codeにどの検証を、どの権限で、どの終了条件まで実行させるか**である。

Kanau Techは、この実行境界をClaude Codeで実装するための **Claude Code TDD Guardrails Kit** を公開した。`CLAUDE.md` で行動原則を定義し、`.claude/settings.json` とHooksで決定論的な制約を実装する構成である。

## なぜClaude Codeにガードレールが必要なのか

Claude CodeのHooksは、ファイル編集、タスク完了、入力待ちなどのライフサイクルイベントでユーザー定義のコマンドを実行できる。これは、LLMが「ルールを守るべきだ」と判断することに依存せず、特定の操作を必ず検証・ブロック・記録するための公式機構である。[Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)

テスト戦略でもこの区別が重要になる。次のような依頼は危険である。

> 「この機能を実装して、全部テストして。」

この一文には、変更の範囲、統合テストへ上げる条件、NFRの開始条件、失敗時の停止条件がない。Claude Codeが利用可能なテストやブラウザ操作を広く探索したとしても、それは「AIの暴走」と決めつけるべきではない。人間が実行境界を定義していないことが問題である。

## キットの3層構造

| 層 | Claude Codeでの実装 | 役割 |
|---|---|---|
| Intent Layer | `CLAUDE.md` | 目的、変更範囲、完了条件、最小テスト優先を定義する。 |
| Safety Layer | `.claude/settings.json` と `PreToolUse` Hook | 負荷・ストレス・フルE2Eなどの高コストな実行を、明示承認なしに開始させない。 |
| Feedback Layer | `PostToolUse` / `Stop` / `Notification` Hook、CI | 実行証跡、失敗根拠、プロセス後始末、停止・通知を整える。 |

## 何をブロックするのか

キットのHookは、テストを止めるためのものではない。以下を制御する。

1. 対象を指定しないリポジトリ全体テスト。
2. ワークロード、合格基準、資源予算のない負荷・ストレス・レーステスト。
3. 根拠を追加しない同一失敗の反復。
4. タスク終了後に残るサーバー、ワーカー、ブラウザ。

一方で、変更に直接関係する単体テスト、型検査、lintは最初に実行する。統合テストはモジュール・永続化・ネットワークなどの境界を跨ぐときに拡張し、フルスイートはPR・リリースゲートに予約する。

## 導入方法

```bash
mkdir -p .claude/hooks
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/CLAUDE.md -o CLAUDE.md
curl -L https://raw.githubusercontent.com/kanautech/ai-agent-optimization-kit/master/.claude/settings.json -o .claude/settings.json
```

その後、プロジェクトのテストコマンド、保護対象、NFRの承認者、実行予算を調整する。詳しくは [Claude Code導入ガイド](https://github.com/kanautech/ai-agent-optimization-kit/blob/master/CLAUDE_CODE_INTEGRATION.md) を参照されたい。

## 効果は数値で約束せず、実タスクで測る

本キットは、CPU、トークン、開発時間、品質の改善率を保証しない。モデル、リポジトリ、テスト構成、チームのワークフローで結果は変わる。代表タスクを固定し、導入前後の初回フィードバック時間、テスト実行回数、連続失敗回数、残留プロセス、回帰検出率を測定して採用判断を行う。

> 目的はテストを減らすことではない。**正しいテストを、正しい層で、正しいタイミングに実行すること**である。

## 他の環境への応用

Codex、Cursor、Google Antigravityなどにも、最小関連テスト、NFRの明示承認、リトライ上限、資源上限という原則は応用できる。ただし、本キットの主対象はClaude Codeであり、Hooksと `CLAUDE.md` をそのまま他製品へ移植できるとは限らない。各製品の公式ルール・フック機構で再実装すること。

## Tiếng Việt — Tóm tắt

Bộ công cụ này tập trung vào **Claude Code**. `CLAUDE.md` định nghĩa mục tiêu, phạm vi thay đổi và chiến lược test; còn Hooks trong `.claude/settings.json` tạo ra các ràng buộc mang tính quyết định để chặn việc chạy test NFR hoặc test toàn bộ repository khi chưa có phê duyệt rõ ràng.

Mục tiêu không phải là giảm số lượng test. Mục tiêu là chạy **đúng bài test, đúng tầng, đúng thời điểm**. Codex, Cursor và Google Antigravity có thể áp dụng cùng nguyên tắc, nhưng cần chuyển đổi theo cơ chế rules/hook chính thức của từng sản phẩm.

## 参考資料

- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)（取得日: 2026-08-17）
- [Claude Code Settings](https://code.claude.com/docs/en/settings)（取得日: 2026-08-17）
