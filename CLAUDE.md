# Claude Code Project Instructions: TDD Guardrails

## Mission

Implement the requested change with the smallest safe change set. Optimize for clear evidence of correctness, not for the largest possible test suite.

## Default Test Strategy

1. Read the affected code and existing tests before modifying files.
2. Start with linting, type-checking, and the smallest test directly related to the change.
3. Expand to integration tests only when the change crosses a module, persistence, network, or service boundary.
4. Reserve the full suite for an explicit PR, release, or CI gate request.
5. Run tests sequentially unless the task explicitly identifies independent tests and a resource budget.

## NFR Decision Boundary

Do **not** start load, stress, race, performance, security, or full browser E2E tests by default.

Before running an NFR test, ask for or locate all of the following:

- Target environment.
- Workload or attack scenario.
- Acceptance criteria.
- Time, parallelism, and infrastructure budget.
- Owner who will interpret the result.

If any item is missing, report the missing decision and continue with the functional test layer that is in scope.

## Failure Handling

- Never retry the same failing test blindly.
- After three consecutive failures with the same failure signature, stop execution.
- Preserve the failing command, error output, relevant environment facts, and a root-cause hypothesis.
- Do not weaken assertions, delete tests, or change timeouts solely to make a test pass.

## Process Hygiene

- Track every server, worker, browser, and background process you start.
- Stop processes you started after a test completes or fails.
- Do not modify `.env`, secrets, lockfiles, CI configuration, production infrastructure, or protected paths unless the task explicitly authorizes it.

## Final Report Format

When completing a task, report:

1. The code and tests changed.
2. Commands run and their results.
3. Tests intentionally not run, with the reason.
4. Any NFR decision that remains for a human owner.
5. Any residual risk or follow-up action.
