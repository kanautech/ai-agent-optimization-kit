# SNS・コミュニティ拡散用告知文案

公開リンクを投稿直前に差し替えること。数値改善や特定ツールの挙動は、再現可能な自社測定結果がない限り断定しない。

## 日本語 — X / LinkedIn

> 【OSS公開】Claude Codeの自律性を活かしながら、過剰なフルE2E・負荷・レーステストや盲目的リトライを防ぐ **Claude Code TDD Guardrails Kit** を公開しました。
>
> `CLAUDE.md` で目的・テスト範囲・停止条件を定義し、`.claude/settings.json` とHooksで高リスク操作の実行境界を決定論的に制御します。
>
> 目標はテストを減らすことではありません。**正しいテストを、正しい層・タイミングで実行すること**です。
>
> GitHub: https://github.com/kanautech/ai-agent-optimization-kit
> Kanau Tech Blog: <公開URL>
>
> #ClaudeCode #Anthropic #TDD #AICoding #DeveloperExperience #KanauTech

## English — X / LinkedIn

> We have open-sourced the **Claude Code TDD Guardrails Kit**.
>
> It combines `CLAUDE.md` project instructions with deterministic Claude Code Hooks to prevent unscoped full E2E/load/race testing and blind retry loops—while preserving Claude Code’s autonomy for implementation and debugging.
>
> The goal is not fewer tests. It is **the right test, at the right layer, at the right time**.
>
> GitHub: https://github.com/kanautech/ai-agent-optimization-kit
> Kanau Tech Blog: <PUBLIC_URL>
>
> #ClaudeCode #Anthropic #TDD #AICoding #SoftwareEngineering

## Tiếng Việt — Facebook / LinkedIn

> Kanautech vừa phát hành mã nguồn mở **Claude Code TDD Guardrails Kit**.
>
> Bộ công cụ kết hợp `CLAUDE.md` với Hooks trong Claude Code để chặn việc tự chạy E2E, load, stress hoặc race test ngoài phạm vi yêu cầu, đồng thời hạn chế các vòng lặp retry mù quáng. AI vẫn được tự chủ trong việc triển khai và debug; các thao tác có rủi ro cao được kiểm soát bằng ranh giới thực thi rõ ràng.
>
> Mục tiêu không phải là giảm số lượng test, mà là chạy **đúng bài test, đúng tầng, đúng thời điểm**.
>
> GitHub: https://github.com/kanautech/ai-agent-optimization-kit
> Kanau Tech Blog: <PUBLIC_URL>
>
> #ClaudeCode #Anthropic #TDD #AICoding #KanauTech

## 注記

Codex、Cursor、Google Antigravityなどにも原則を応用できるが、本投稿・本キットの主対象はClaude Codeである。他ツールに適用する際は、それぞれの公式ルール・フック・CI設定へ移植する。
