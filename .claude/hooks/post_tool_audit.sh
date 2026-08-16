#!/usr/bin/env bash
# Claude Code PostToolUse hook: append Bash command evidence for review.
# This hook never kills processes automatically. Cleanup must be project-specific
# and must only target processes that the agent started.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
AUDIT_DIR="${PROJECT_DIR}/.claude/audit"
AUDIT_FILE="${AUDIT_DIR}/bash-commands.jsonl"
mkdir -p "${AUDIT_DIR}"

# Claude Code passes hook input as JSON on stdin. Retain it locally so a human
# can inspect commands after a failed loop or unexpected test expansion.
INPUT="$(cat)"
printf '%s\n' "${INPUT}" >> "${AUDIT_FILE}"

exit 0
