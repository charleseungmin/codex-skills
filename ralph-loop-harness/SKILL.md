---
name: ralph-loop-harness
description: Use when the user mentions Ralph Loop, 랄프 루프, harness, 하네스, run loop, task loop, T99, or asks to keep looping through a repo plan until the target is complete. This skill makes Codex prefer the repository-local harness runner instead of merely describing Plan / Execute / Verify steps.
---

# Ralph Loop Harness

## Core Rule

Run the repository-local Ralph Loop harness when it exists. Do not simulate the loop in prose if a runner script is available.

Stop only when one of these is true:
- The requested target is complete.
- A real external blocker prevents progress.
- The user explicitly pauses or changes scope.

## Workflow

1. Inspect the repo instructions first: `AGENTS.md`, current plan files, and task-state files such as `docs/exec-plans/current-task.md`.
2. Detect the harness runner from the repo root. On Windows prefer `scripts/run_loop.ps1`; otherwise use `scripts/run_loop.sh`.
3. Check the repo verification contract before running. Look for scripts such as `scripts/verify.ps1`, `scripts/check_done.ps1`, `scripts/verify.sh`, or `scripts/check_done.sh`.
4. If the current target is not reflected in the task-state file, update or seed the task state before running the loop.
5. Check runner options with `scripts/run_loop.ps1 --help` on Windows or `scripts/run_loop.sh --help` elsewhere when the user asks for a larger target.
6. If the runner supports target execution and the user asks for a larger target such as `T99`, “전체 완료”, or “남은 task 전부”, run target mode instead of single-task mode.
7. If target mode is unavailable and the runner completes only one task, advance the task state to the next incomplete task and rerun manually.
8. Repeat until the target is complete or a blocker is recorded.

## Runner Execution

Use the repo-local runner from the repo root.

- Single current task only:
  - Windows: `.\scripts\run_loop.ps1 --once`
  - Bash: `scripts/run_loop.sh --once`
- Continue to an explicit target:
  - Windows: `.\scripts\run_loop.ps1 --target T99`
  - Bash: `scripts/run_loop.sh --target T99`
- Continue through the remaining plan toward `T99`:
  - Windows: `.\scripts\run_loop.ps1 --continue`
  - Bash: `scripts/run_loop.sh --continue`

When `--target` or `--continue` is available, do not stop after the first task-level `DONE CHECK PASSED`. Let the runner call its advancer, seed the next task into `docs/exec-plans/current-task.md`, and continue. Stop only when the runner reports target completion, a real blocker, or the user pauses the work.

If a repository has an older runner without `--target` or `--continue`, use the older behavior: after a one-task success, update `docs/exec-plans/current-task.md` to the next executable task and rerun the runner.

## Fallback Loop

Use this only when the external runner is missing or unusable.

For each task:
- Plan: define the smallest independent task, affected files, expected dependency direction, and completion criteria.
- Execute: implement only that task. Do not widen scope.
- Verify: run the repo-approved verification command. If the repo policy says build-only verify, do not add lint or tests.
- Replan: if verification fails, record the failure reason, make the smallest corrective plan, and rerun the same task.
- Complete: mark the task complete only after verification passes.

## Verification Policy

Read the repository's current policy from its plan, task-state, or scripts. Do not assume lint or test gates are required.

If the current project says verification is build-only, use only the build command specified by the repo or task plan. In the exoFit Android repo, this commonly means validating app build targets such as `:app:main:assembleInternalDebug` and `:app:test:assembleInternalDebug`.

## Commit Policy

Follow the repository instructions. If the plan or user requires one commit per completed task, commit only after the task passes verification.

Keep staging narrow:
- Stage files changed for the current task only.
- Do not stage `.codex/**`, local logs, secrets, or unrelated user changes unless explicitly requested.
- Use the repo language and commit-message convention.

## Reporting

Report concise loop status:
- Target requested.
- Runner used or fallback reason.
- Tasks completed, failed, or blocked.
- Verification command and result.
- Commit hash when a task commit was created.

If blocked, include the exact blocker and the next runnable step.
