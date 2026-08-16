# Safety Guardrails: Resource & Policy Constraints

## 1. Prohibited Anti-Patterns (NFR Over-testing)
The following testing behaviors are strictly prohibited unless a `FORCE_COMPLIANCE` flag is provided:
- **UUID/Collision Testing**: Do not spawn multiple workers to test theoretical ID collisions.
- **Extreme P99 Targets**: Do not attempt to optimize for P99 < 5ms in local development or PoC environments.
- **Full E2E for Minor Changes**: Do not launch a browser-based E2E suite for non-UI logic changes.
- **Deep Transaction Testing**: Do not perform isolation level 3 / serializable transaction tests on local SQLite or mock databases.

## 2. Resource Limits
- **Retry Limit**: Maximum 3 attempts per specific test case.
- **Concurrency Limit**: Maximum 2 parallel test processes.
- **Timeout Limit**: Any test taking longer than 60 seconds must be aborted and reported.

## 3. Environment Protection
- **Process Cleanup**: All child processes must be tracked and killed on error or completion.
- **File System**: Do not create temporary files outside of the designated `/tmp` or `build/` directories.
- **Network**: Do not attempt outbound calls to non-whitelisted production APIs during testing.

## 4. Human Intervention Triggers
Immediately stop and prompt the user if:
1. The model detects a "Product Overhang" (a tool limitation blocking a simple model-driven solution).
2. The system environment is inconsistent (e.g., missing dependencies, locked ports).
3. The proposed NFR validation exceeds the current project scope (PoC/MVP vs Enterprise).
