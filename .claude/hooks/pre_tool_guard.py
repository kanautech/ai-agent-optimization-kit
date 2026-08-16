#!/usr/bin/env python3
"""Claude Code PreToolUse hook for scoped test execution.

Blocks commands that look like unapproved NFR test runs or dangerous broad test
commands. Set ALLOW_NFR_TESTS=1 only after documenting the target environment,
workload, acceptance criteria, budget, and responsible owner.
"""

import json
import os
import re
import sys

payload = json.load(sys.stdin)
command = payload.get("tool_input", {}).get("command", "")
normalized = command.lower()

# Customize these patterns for the project. They are intentionally conservative.
NFR_PATTERNS = [
    r"\bk6\b",
    r"\blocat\b",
    r"\blocust\b",
    r"\bartillery\b",
    r"\bwrk\b",
    r"\bvegeta\b",
    r"\bhey\b",
    r"\bab\s+https?://",
    r"--race\b",
    r"playwright\s+test(?!\s+[^\n]*--grep)",
    r"cypress\s+run(?!\s+[^\n]*--spec)",
]

BROAD_TEST_PATTERNS = [
    r"\bnpm\s+test\s*$",
    r"\bpnpm\s+test\s*$",
    r"\byarn\s+test\s*$",
    r"\bpytest\s*$",
]

# Explicit human authorization is the escape hatch. Keep the authorization in
# the task/request history and export it only for that approved execution.
if os.getenv("ALLOW_NFR_TESTS") == "1":
    sys.exit(0)

for pattern in NFR_PATTERNS:
    if re.search(pattern, normalized):
        print(
            "Blocked by TDD Guardrails: this command appears to run an NFR or broad browser test. "
            "Before running it, document target environment, workload/scenario, acceptance criteria, "
            "time/parallelism budget, and the human owner. Then rerun only with explicit authorization "
            "(for example, ALLOW_NFR_TESTS=1 for that one approved command).",
            file=sys.stderr,
        )
        sys.exit(2)

for pattern in BROAD_TEST_PATTERNS:
    if re.search(pattern, normalized):
        print(
            "Blocked by TDD Guardrails: a repository-wide test command was requested without a scoped target. "
            "Run the smallest relevant test first, or use ALLOW_NFR_TESTS=1 only when a full-suite gate is explicitly approved.",
            file=sys.stderr,
        )
        sys.exit(2)

sys.exit(0)
