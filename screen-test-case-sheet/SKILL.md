---
name: screen-test-case-sheet
description: Organize QA test cases into a spreadsheet-style sheet grouped by requirements, with screen units used only as supporting analysis. Use when Codex needs to derive or rewrite test cases from Android UI flows, requirements, screen specs, code, or bug reports, especially when each case should be written in Korean QA-sheet form with scenario ID, test category, related development item, description, condition, input, and output, plus standardized visibility and enablement wording using the required symbols.
---

# Screen Test Case Sheet

## Overview

Produce test cases in a sheet format centered on individual requirements. Screens are used to derive cases, but the final result should be grouped by requirement ID or development item first. When requirements are present, add two short summary tables above the test cases: first a screen-name mapping table that aligns English implementation names with Korean labels and related scenario IDs, then a requirement summary table that maps development IDs to development items, branch names, test category, and scenario IDs. For each row, write a scenario ID, test category, related development item, short description, screen name in Korean, prerequisite condition, user input, and expected output. Write the final sheet in Korean by default unless the user explicitly asks for another language.

## Workflow

1. Identify the requirement boundary first.
   - Group the final output by requirement ID, development item, or requested change item.
   - If one requirement affects multiple screens, keep those cases under the same requirement section.
   - If requirements are explicitly given, add summary tables above the test cases in this order:
     1. `화면 영문명 | 화면 국문명 | 테스트 시나리오 ID`
     2. `개발 ID | 개발사항 | 분기 구분 | 테스트 구분 | 테스트 시나리오`
   - In the second summary table, use one row per `테스트 시나리오` row.
   - If one `테스트 시나리오` covers several detailed `조건 | 입력 | 출력` rows, summarize them under one representative `분기 구분`.
   - If several rows belong to the same `개발 ID` or `개발사항`, repeated cells may be left blank to match spreadsheet-style grouping.
2. Identify the supporting screen boundary.
   - Split cases by `Fragment`, `Dialog`, `BottomSheetDialogFragment`, `Activity`, or other visible screen unit.
   - Do not mix multiple screens into one row unless the user explicitly asks for end-to-end flow cases.
3. Map each row to a scenario record.
   - Fill these columns in order: `시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명 | 조건 | 입력 | 출력`.
   - Generate `시나리오 ID` when the user does not provide one. Use a stable form such as `TEST-UI-001`, `TEST-FUNC-001`.
   - When rows belong to the same requirement, the same screen, and the same `테스트 구분`, reuse one `시나리오 ID`.
   - Separate `UI` and `기능` even on the same screen. They must not share one `시나리오 ID`.
   - If one scenario ID covers multiple verification lines, merge `시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명` and split only `조건 | 입력 | 출력` into multiple rows.
   - Set `테스트 구분` to `UI` when the row primarily checks visible layout, copy, state, or rendering.
   - Set `테스트 구분` to `기능` when the row primarily checks behavior, processing, branching, saving, validation, navigation, or media/action execution.
   - Put requirement IDs, ticket IDs, or 개발사항 IDs into `연관 개발사항`. If multiple items apply, join them with `, `.
   - Write `화면명` in Korean only. Do not leave English fragment or activity names in the case rows.
   - If implementation names matter, show them only in the top screen-name mapping table.
   - In the top screen-name mapping table, list the related scenario IDs for that screen. If there are multiple IDs, join them like `TEST-UI-001, TEST-FUNC-001`.
   - Example: `운동 준비 화면`, `운동 상세보기 화면`, `운동 중지 다이얼로그`.
4. Derive the condition as the state that must be true when the input is performed.
   - Write only conditions that must already be satisfied at the moment of `입력` so that the expected `출력` can occur.
   - Include accumulated progress, saved values, threshold reach state, previously completed steps, permission state, network state, feature flag state, or screen mode when they change the result.
   - Do not write the user's action itself in `조건`.
   - If the same input produces a different result depending on whether a state has been reached, split the rows by that state and write it in `조건`.
5. Derive the input from actions on the current screen.
   - Use concrete user actions such as screen entry, button tap, toggle change, text entry, item selection, swipe, back press, or system event received while the screen is visible.
   - Keep one dominant action per row when possible.
6. Derive the output as the observable result of that input.
   - Focus on UI changes, navigation results, enabled or disabled states, messages, dialogs, toasts, loading indicators, and rendered values.
   - Include validation errors and blocked states when the input should fail.
7. Split rows by branch.
   - If the same input leads to different outcomes depending on condition, create separate rows under the same scenario when requirement, screen, and test category are unchanged.
   - If one screen has multiple important entry modes, write separate rows for each mode. Reuse the same scenario ID when they are still the same requirement, screen, and test category.
   - Only issue a new scenario ID when requirement changes, screen changes, or `UI/기능` changes.
8. Return the result in sheet form.
   - Default to a markdown table unless the user asks for CSV, TSV, or spreadsheet-friendly plain text.
   - Keep the core columns in this order: `시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명 | 조건 | 입력 | 출력`.
   - Write column names and cell contents in Korean by default.

## Writing Rules

- Use the requested test-item meanings.
  - `시나리오 ID`: 각 테스트 시나리오를 구별하기 위한 ID.
  - `테스트 구분`: 해당 시나리오에서 중점적으로 확인할 부분.
  - `설명`: 무엇을 테스트하는지에 대한 간단한 설명.
  - `화면명`: 테스트 대상 화면의 국문 이름.
  - `조건`: `입력`을 수행했을 때 기대한 `출력`이 발생하려면 반드시 충족되어 있어야 하는 상태.
  - `입력`: 시험 항목에서 시험자가 취해야 하는 행위.
  - `출력`: 시험 항목에서 시험자가 확인해야 하는 내용.
- Keep `Condition` state-based.
  - Example: 기준값 측정 완료 상태, 운동시간 50분 달성 상태, 처방 운동 모두 수행 완료 상태, 권한 허용 상태, 네트워크 연결 상태.
- Keep `Input` action-oriented.
  - Example: enter screen, tap save, input invalid email, select list item, dismiss dialog.
- Keep `Output` user-visible.
  - Example: button enabled, error text shown, dialog closes, next fragment opens, value updated on screen.
- Write `조건` so QA can judge whether the output should or should not happen after the input.
  - Example: `조건: 운동시간 50분 달성, 처방된 운동 모두 수행 완료 / 입력: 운동 완료 / 출력: [정리 운동 화면] 표시`
- Apply the symbol and wording rules consistently.
  - `입력`과 `출력` 모두 가능한 한 아래 기호 규칙을 적용해 쓴다.
  - `[Flow, 디바이스 및 외부 앱 화면]`에는 `표시`를 사용한다.
  - `{화면, 바텀시트, Dialog}`에는 `숨김` 또는 `표시`를 사용한다.
  - `"Toast"`에는 `활성화` 대신 노출 여부를 분명히 적고, 필요 시 `"Toast" 표시`처럼 쓴다.
  - `` `버튼` `` 상태는 `활성화`, `비활성화`로 표현한다.
- Convert screen references in case rows to Korean labels.
  - Example: `ExercisePrepareFragment` -> `운동 준비 화면`
  - Example: `PrescriptionDetailActivity` -> `운동 상세보기 화면`
  - Example: `CalibrationCompleteDialogFragment` -> `기준값 측정 완료 다이얼로그`
- Prefer symbol-applied wording in `Input`.
  - Example: `` `저장` 클릭 ``
  - Example: `{권한 안내 Dialog}에서 `확인` 클릭`
  - Example: `[외부 인증 앱 화면] 표시 상태에서 뒤로가기 수행`
- Write outputs in QA-ready phrasing.
  - Example: `{로그아웃 확인 Dialog} 표시`
  - Example: `\`저장\` 버튼 비활성화`
  - Example: `[카메라 권한 설정 화면] 표시`
  - Example: `"네트워크 오류" Toast 표시`
- Avoid implementation details unless they explain a user-visible branch.
- Prefer short noun phrases for `Condition` and short verb phrases for `Input` and `Output`.
- When one scenario needs sequential outputs, continue the output cell with line breaks instead of creating prose outside the row.
- When one scenario includes multiple condition or entry variations on the same screen, keep one scenario ID and repeat only `조건 | 입력 | 출력` as additional rows.
- When the user gives only a flow summary, infer the likely screen cases and mark assumptions briefly outside the table if needed.

## Output Expectations

- If requirements are present, place summary tables before the detailed cases in this order:
  1. `화면 영문명 | 화면 국문명 | 테스트 시나리오 ID`
  2. `개발 ID | 개발사항 | 분기 구분 | 테스트 구분 | 테스트 시나리오`
- In the requirement summary table:
  - `개발 ID`에는 요구사항 ID를 그대로 넣는다.
  - `개발사항`에는 요구사항명 또는 변경 항목명을 넣는다.
  - `분기 구분`에는 해당 `테스트 시나리오` 전체를 대표하는 검증 주제나 흐름을 짧게 적는다.
  - 같은 `테스트 시나리오` 아래 여러 `조건 | 입력 | 출력` 행이 있더라도 `요구사항 정리`에서는 한 줄만 쓴다.
  - `테스트 구분`에는 `UI` 또는 `기능`을 적는다.
  - `테스트 시나리오`에는 연결된 시나리오 ID를 적는다.
- Group the sheet by requirement name or requirement ID.
- Inside each requirement section, list cases derived from the relevant screens.
- Reuse one scenario ID for the same requirement + same screen + same test category combination.
- Under that scenario, use one row per distinct `조건 | 입력 | 출력` combination.
- Cover normal cases, validation failures, empty states, disabled states, permission states, and retry cases when they are relevant.
- If the user asks for exhaustive QA coverage, include success, failure, boundary, and recovery paths for each requirement.
- If the source is incomplete, say which conditions or outputs were inferred.
- Use natural Korean phrasing suitable for QA sheets. Keep English screen identifiers only in the screen-name mapping table, not in the case rows.
- Do not add `비고 (예외사항)` unless the user explicitly asks for that column, but preserve the concept by mentioning inferred exceptions above the table when needed.

## Reference

- Read [sheet-format.md](./references/sheet-format.md) for the default table shape, classification rules, and examples before drafting a large case list.
