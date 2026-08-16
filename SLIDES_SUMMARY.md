# プレゼンテーションスライド構成サマリー（Claude Code版）

**デッキ**: Claude Code TDD Guardrails — 自律性を保ち、過剰検証を止める  
**主対象**: Claude Code  
**補助的適用先**: Codex、Cursor、Google Antigravity等。設定・Hook機構が異なるため、原則のみを移植する。

| # | スライド | 主張 |
|---:|---|---|
| 1 | Claude Code TDD Guardrails | `CLAUDE.md` とHooksを組み合わせ、Claude Codeの実行を統制する。 |
| 2 | CLAUDE.mdだけでは実行境界を担保できない | 自然言語の行動原則と、Hooksによる決定論的な実行制約を分離する。 |
| 3 | Claude CodeでNFR過剰検証を防ぐ判断境界 | Scope、NFR、Stopを `CLAUDE.md`、PreToolUse、PostToolUseへ対応付ける。 |
| 4 | ルールの量ではなく、判断境界 | 目的・検証・停止条件を明確にし、曖昧な抽象命令を減らす。 |
| 5 | ルールの棚卸し | 各ルールを失敗モード、適用範囲、例外、測定方法で審査する。 |
| 6 | Unhobbling：裁量と統制の分離 | 実装・調査・デバッグはClaude Codeへ、NFR・リスク受容は人間へ分離する。 |
| 7 | ベストプラクティス | Smallest Test First、NFRの明示承認、停止条件、モックの活用。 |
| 8 | 階層的ガードレール・モデル | Intent / Safety / FeedbackをCLAUDE.md、Hooks、CIへ実装する。 |
| 9 | 段階導入と測定設計 | 代表タスクを使い、初回フィードバック時間、反復、回帰を測る。 |
| 10 | 結論 | Right Test, Right Layer, Right Time。Claude Codeの自律性と統制を両立する。 |

## 注記

本デッキはClaude Codeの公式機能・性能比較ではない。Claude Codeの `CLAUDE.md` とHooksを使い、各チームが実行境界を設計するための資料である。効果は代表タスクによる導入前後の測定で確認する。
