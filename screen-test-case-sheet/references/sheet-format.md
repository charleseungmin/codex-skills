# Sheet Format

## Default Columns
- `화면`: 현재 테스트 대상 화면 단위.
- `조건`: 현재 화면 진입 전에 이미 성립해 있어야 하는 선행 조건.
- `입력`: 현재 화면에서 수행하는 사용자 행동 또는 이벤트.
- `출력`: 해당 입력으로 인해 기대되는 UI 결과 또는 화면 이동 결과.

## Classification Rules
- Put previous app state in `Condition`.
  - account linked
  - required permission denied earlier
  - previous screen saved draft
  - server returned maintenance mode
- Put current-screen action in `Input`.
  - enter screen
  - tap confirm
  - input invalid value
  - clear text field
  - select item
  - dismiss dialog
- Put visible consequence in `Output`.
  - error message shown
  - save button enabled
  - dialog closed
  - next fragment opened
  - loading spinner displayed
  - entered value reflected on summary card

## Case Splitting Rules
- Split rows when one input produces different outputs under different conditions.
- Split rows when a screen supports different entry points or modes.
- Split rows for success and failure paths.
- Split rows for initial load, retry, empty state, and permission state when those are meaningful to QA.

## Recommended Output Shape
```md
### Screen: ExampleFragment

| 화면 | 조건 | 입력 | 출력 |
| --- | --- | --- | --- |
| ExampleFragment | 연동된 기기가 존재함 | 화면 진입 | 연동된 기기 정보가 노출됨 |
| ExampleFragment | 연동된 기기가 존재함 | 연결 해제 버튼 탭 | 확인 다이얼로그가 노출됨 |
| ExampleFragment | 연동된 기기가 없음 | 화면 진입 | 빈 상태 UI가 노출됨 |
```

## Dialog Example
```md
### Screen: ConfirmDialog

| 화면 | 조건 | 입력 | 출력 |
| --- | --- | --- | --- |
| ConfirmDialog | 다이얼로그 호출 전 저장되지 않은 변경사항이 존재함 | 확인 버튼 탭 | 다이얼로그가 닫히고 저장이 수행됨 |
| ConfirmDialog | 다이얼로그 호출 전 저장되지 않은 변경사항이 존재함 | 취소 버튼 탭 | 다이얼로그가 닫히고 현재 화면은 유지됨 |
```

## Notes
- Keep wording short enough to paste into a spreadsheet without cleanup.
- If the user asks for sheet export, keep the same column order unless they specify another one.
- If assumptions are necessary, list them above the table instead of mixing them into cells.
- Write the final sheet in Korean by default unless the user explicitly requests another language.
