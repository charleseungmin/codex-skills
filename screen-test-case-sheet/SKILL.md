---
name: screen-test-case-sheet
description: Organize QA test cases into a spreadsheet-style sheet grouped by screen units such as fragments, dialogs, bottom sheets, activities, or full pages. Use when Codex needs to derive or rewrite test cases from Android UI flows, requirements, screen specs, code, or bug reports, especially when each case must be expressed as condition, input, and output with conditions defined as prerequisites set before entering the current screen.
---

# Screen Test Case Sheet

## Overview

Produce test cases in a sheet format centered on individual screens. For each row, describe the prerequisite condition that already exists before the screen, the user input performed on the screen, and the expected visible output caused by that input. Write the final sheet in Korean by default unless the user explicitly asks for another language.

## Workflow

1. Identify the screen boundary first.
   - Split cases by `Fragment`, `Dialog`, `BottomSheetDialogFragment`, `Activity`, or other visible screen unit.
   - Do not mix multiple screens into one row unless the user explicitly asks for end-to-end flow cases.
2. Derive the condition from outside the current screen.
   - Write only prerequisites that were established before entering the current screen.
   - Include prior settings, account state, permissions, feature flags, network state, or previously completed steps.
   - Do not put actions performed on the current screen into `Condition`.
3. Derive the input from actions on the current screen.
   - Use concrete user actions such as screen entry, button tap, toggle change, text entry, item selection, swipe, back press, or system event received while the screen is visible.
   - Keep one dominant action per row when possible.
4. Derive the output as the observable result of that input.
   - Focus on UI changes, navigation results, enabled or disabled states, messages, dialogs, toasts, loading indicators, and rendered values.
   - Include validation errors and blocked states when the input should fail.
5. Split rows by branch.
   - If the same input leads to different outcomes depending on condition, create separate rows.
   - If one screen has multiple important entry modes, write separate rows for each mode.
6. Return the result in sheet form.
   - Default to a markdown table unless the user asks for CSV, TSV, or spreadsheet-friendly plain text.
   - Keep the core columns in this order: `Screen | Condition | Input | Output`.
   - Write column names and cell contents in Korean by default.

## Writing Rules

- Keep `Condition` outside-in.
  - Example: prior user type, device binding status, permission denied state, server response mode, previous toggle value.
- Keep `Input` action-oriented.
  - Example: enter screen, tap save, input invalid email, select list item, dismiss dialog.
- Keep `Output` user-visible.
  - Example: button enabled, error text shown, dialog closes, next fragment opens, value updated on screen.
- Avoid implementation details unless they explain a user-visible branch.
- Prefer short noun phrases for `Condition` and short verb phrases for `Input` and `Output`.
- When the user gives only a flow summary, infer the likely screen cases and mark assumptions briefly outside the table if needed.

## Output Expectations

- Group the sheet by screen name.
- Use one row per distinct condition-input-output combination.
- Cover normal cases, validation failures, empty states, disabled states, permission states, and retry cases when they are relevant.
- If the user asks for exhaustive QA coverage, include success, failure, boundary, and recovery paths for each screen.
- If the source is incomplete, say which conditions or outputs were inferred.
- Use natural Korean phrasing suitable for QA sheets. Keep screen identifiers such as `LoginFragment` or `ConfirmDialog` as-is when they are code names.

## Reference

- Read [sheet-format.md](./references/sheet-format.md) for the default table shape, classification rules, and examples before drafting a large case list.
