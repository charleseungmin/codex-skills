# Sheet Format

## Default Columns
- `시나리오 ID`: 각 테스트 시나리오를 구별하기 위한 ID.
- `테스트 구분`: `UI` 또는 `기능`.
- `연관 개발사항`: 요구사항 ID, 개발 티켓 ID, 변경 요청 ID.
- `설명`: 무엇을 테스트하는지에 대한 간단한 설명.
- `화면명`: 테스트 대상 화면의 국문 이름.
- `조건`: `입력` 시점에 기대한 `출력`이 발생하려면 반드시 충족되어 있어야 하는 상태.
- `입력`: 현재 화면에서 수행하는 사용자 행동 또는 이벤트.
- `출력`: 해당 입력으로 인해 기대되는 UI 결과 또는 화면 이동 결과.

## Test Category Rules
- Use `UI` for layout, text, visibility, style, enabled state, or rendering checks.
- Use `기능` for behavior, logic, transition, validation, save, retry, playback, counting, or side-effect checks.

## Output Wording Rules
- `[Flow, 디바이스 및 외부 앱 화면]` -> `표시`
- `{화면, 바텀시트, Dialog}` -> `표시`, `숨김`
- `"Toast"` -> `"Toast" 표시`
- `` `버튼` `` -> `활성화`, `비활성화`
- Apply these symbols to both `입력` and `출력` whenever possible.

## Classification Rules
- Put output-gating state in `Condition`.
  - 기준값 측정 완료 상태
  - 운동시간 50분 달성 상태
  - 처방된 운동 모두 수행 완료 상태
  - account linked
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
- Reuse one scenario ID when the requirement, screen, and test category are the same.
- Split only `조건 | 입력 | 출력` rows when one input produces different outputs under different conditions.
- Split only `조건 | 입력 | 출력` rows when a screen supports different entry points or modes but still belongs to the same requirement, screen, and test category.
- Split rows for success and failure paths.
- Split rows for initial load, retry, empty state, and permission state when those are meaningful to QA.
- Create a new scenario ID only when the requirement changes, the screen changes, or `UI/기능` changes.

## Recommended Output Shape
```md
## 화면명 정리

| 화면 영문명 | 화면 국문명 | 테스트 시나리오 ID |
| --- | --- | --- |
| DeviceLinkFragment | 연동 기기 화면 | TEST-UI-001, TEST-FUNC-001 |
| DisconnectConfirmDialog | 연결 해제 확인 다이얼로그 | TEST-FUNC-002, TEST-FUNC-003 |

## 요구사항 정리

| 개발 ID | 개발사항 | 분기 구분 | 테스트 구분 | 테스트 시나리오 |
| --- | --- | --- | --- | --- |
| RD-01-01 | 연동 기기 표시 | 연동 기기 정보 표시 | UI | TEST-UI-001 |
| RD-01-02 | 연결 해제 | 연결 해제 처리 | 기능 | TEST-FUNC-001 |
| RD-01-03 | 빈 상태 | 빈 상태 표시 | UI | TEST-UI-002 |

### Requirement: RD-01-01 연동 기기 표시

| 시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명 | 조건 | 입력 | 출력 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-UI-001 | UI | RD-01-01 | 연동 기기 정보 표시 테스트 | 연동 기기 화면 | 연동된 기기가 존재함 | 화면 진입 | `{연동 기기 정보 영역} 표시` |

### Requirement: RD-01-02 연결 해제

| 시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명 | 조건 | 입력 | 출력 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-FUNC-001 | 기능 | RD-01-02 | 연결 해제 진입 테스트 | 연동 기기 화면 | 연동된 기기가 존재함 | `연결 해제` 클릭 | `{연결 해제 확인 Dialog} 표시` |

### Requirement: RD-01-03 빈 상태

| 시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명 | 조건 | 입력 | 출력 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-UI-002 | UI | RD-01-03 | 빈 상태 표시 테스트 | 연동 기기 화면 | 연동된 기기가 없음 | 화면 진입 | `{빈 상태 안내 영역} 표시` |
```

## Condition Example
```md
### Requirement: ED-SDS-260414-999 정리 운동 진입

| 시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명 | 조건 | 입력 | 출력 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-FUNC-010 | 기능 | ED-SDS-260414-999 | 운동 완료 분기 테스트 | 운동 진행 화면 | 운동시간 50분 달성, 처방된 운동 모두 수행 완료 | 운동 완료 | [정리 운동 화면] 표시 |
|  |  |  |  |  | 운동시간 50분 미달성 | 운동 완료 | [운동 진행 화면] 표시 |
```

## Same Screen Merge Example
```md
## 요구사항 정리

| 개발 ID | 개발사항 | 분기 구분 | 테스트 구분 | 테스트 시나리오 |
| --- | --- | --- | --- | --- |
| ED-SDS-260414-001 | 운동 시작 전 카운트 시간 증가 | 운동 시작 카운트 화면 UI 표시 | UI | TEST-UI-001 |

### Requirement: ED-SDS-260414-001 운동 시작 전 카운트 시간 증가

| 시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명 | 조건 | 입력 | 출력 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-UI-001 | UI | ED-SDS-260414-001 | 운동 시작 카운트 화면 UI 표시 테스트 | 운동 시작 카운트 화면 | 운동 준비 단계 완료 상태 | `{운동 시작 카운트 화면} 표시` | `10초 후` 문구 표시 |
|  |  |  |  |  | 운동 시작 카운트가 시작되지 않은 초기 상태 | `{운동 시작 카운트 화면} 표시` | `{카운트 진행바} 표시`<br>`10` 초 기준으로 초기값 표시 |
```

## Dialog Example
```md
### Requirement: RD-02-01 저장 확인

| 시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명 | 조건 | 입력 | 출력 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-FUNC-002 | 기능 | RD-02-01 | 확인 동작 테스트 | 저장 확인 다이얼로그 | 다이얼로그 호출 전 저장되지 않은 변경사항이 존재함 | `확인` 클릭 | `{ConfirmDialog} 숨김` |
| TEST-FUNC-003 | 기능 | RD-02-01 | 취소 동작 테스트 | 저장 확인 다이얼로그 | 다이얼로그 호출 전 저장되지 않은 변경사항이 존재함 | `취소` 클릭 | `{ConfirmDialog} 숨김` |

### Requirement: RD-02-02 오류 안내

| 시나리오 ID | 테스트 구분 | 연관 개발사항 | 설명 | 화면명 | 조건 | 입력 | 출력 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TEST-UI-003 | UI | RD-02-02 | 오류 토스트 표시 테스트 | 저장 확인 다이얼로그 | 네트워크 오류가 발생한 상태임 | `재시도` 클릭 | `"네트워크 오류" Toast 표시` |
```

## Provided Example Shape
```text
시나리오 ID	테스트 구분	연관 개발사항	설명	화면명	조건	입력	출력
TEST-FUNC-001	기능	RD-01-04	캘리브레이션 시작 안내 표시 테스트	실시간 근육/움직임 모니터링 화면	"실시간 근육/움직임 모니터링 화면인 경우
모듈 2개가 모두 연결된 경우"	`시작` 클릭	{캘리브레이션 안내 Dialog} 표시
							"`바른자세로 서서 5초간 멈춰주세요` 표시
`이전으로` 버튼 활성화"
TEST-FUNC-002	기능	RD-01-04	캘리브레이션 완료 후 준비 상태 전환 테스트	실시간 근육/움직임 모니터링 화면	"실시간 근육/움직임 모니터링 화면인 경우
모듈 2개가 모두 연결된 경우"	`시작` 클릭	{캘리브레이션 안내 Dialog} 표시
							`바른자세로 서서 5초간 멈춰주세요` 문구 표시
					-	바른 자세를 유지한 채 5초간 정지한다.	`평가 받을 준비가 되었어요!` 문구 표시
							`확인` 버튼 활성화
					-	`확인` 클릭	{캘리브레이션 안내 Dialog} 숨김
```

## Notes
- Keep wording short enough to paste into a spreadsheet without cleanup.
- If the user asks for sheet export, keep the same column order unless they specify another one.
- If assumptions are necessary, list them above the table instead of mixing them into cells.
- Write the final sheet in Korean by default unless the user explicitly requests another language.
- Default to requirement-first grouping even when the source material is organized by screen.
- Keep screen names in Korean in the case rows, even if the implementation source uses English identifiers.
- In the screen-name mapping table, include all related scenario IDs for that screen in one cell when needed.
- Do not limit `조건` to pre-entry setup. If the output depends on progress or status accumulated on the same screen, write that status in `조건` as long as it is not the action itself.
- In `요구사항 정리`, `개발 ID` is the same value as the requirement ID.
- In `요구사항 정리`, write one row per `테스트 시나리오`. Do not split the summary table further when one scenario has multiple detailed `조건 | 입력 | 출력` rows.
- In the detailed test-case table, merge common cells for the same requirement + same screen + same test category, and vary only `조건 | 입력 | 출력`.
