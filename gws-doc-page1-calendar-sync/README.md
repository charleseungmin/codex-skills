# gws-doc-page1-calendar-sync

Google Docs 플래너(1페이지 기준)의 `오늘의 업무/일정`을 읽어서  
Google Calendar 이벤트 + Google Tasks 할 일로 동기화하는 스킬입니다.

## 1. 준비사항

- Codex 환경
- `gws` CLI 설치 및 로그인 완료
  - 예: `gws auth login`
- Python 3.9+

## 2. 설치(동료 PC)

아래 폴더를 **통째로** 동료 PC의 `~/.codex/skills/` 아래로 복사하세요.

```text
gws-doc-page1-calendar-sync/
  SKILL.md
  README.md
  scripts/syncPlanner.py
  references/format-notes.md
  agents/openai.yaml
```

## 3. 최초 설정

최초 1회:

```powershell
python scripts/syncPlanner.py --setup
```

입력 항목:
- 기본 문서 URL/ID
- timezone (기본: `Asia/Seoul`)
- calendarId (기본: `primary`)
- tasklistId (미입력 시 자동 선택)

설정은 아래 파일에 저장됩니다.

```text
~/.codex/skills-data/gws-doc-page1-calendar-sync/config.json
```

## 4. 기본 사용

일반 실행:

```powershell
python scripts/syncPlanner.py
```

날짜 지정 실행:

```powershell
python scripts/syncPlanner.py --date 2026-04-21
```

미리보기(쓰기 없음):

```powershell
python scripts/syncPlanner.py --dry-run
```

기본 문서 링크 변경:

```powershell
python scripts/syncPlanner.py --set-doc "https://docs.google.com/document/d/<DOC_ID>/edit"
```

현재 설정 확인:

```powershell
python scripts/syncPlanner.py --show-config
```

## 4-1. 사용자 명령(대화) 매핑

Codex 채팅에서 사용자가 아래처럼 말하면, 에이전트는 오른쪽 명령으로 실행하면 됩니다.

| 사용자 입력 | 내부 실행 동작 |
|---|---|
| `실행` | `python scripts/syncPlanner.py` |
| `실행 2026-04-21` | `python scripts/syncPlanner.py --date 2026-04-21` |
| `실행 점검만` | `python scripts/syncPlanner.py --dry-run` |
| `링크 변경 <URL 또는 ID>` | `python scripts/syncPlanner.py --set-doc "<URL 또는 ID>"` |
| `초기 설정` | `python scripts/syncPlanner.py --setup` |
| `설정 확인` | `python scripts/syncPlanner.py --show-config` |

시간이 전부 비어 있는 문서에서 사용자가 시간을 직접 준 경우:

```powershell
python scripts/syncPlanner.py --assign-time "업무A=09:00~10:00" --assign-time "업무B=16:00~16:30"
```

## 5. 동기화 규칙

- 문서의 **1페이지 플래너 테이블**만 처리
- `오늘의 업무/일정` 섹션에서:
  - `HH:MM ~ HH:MM` 형식 시간 있음: Calendar 이벤트 생성
  - 시간 없음: Tasks 할 일 생성
- 중복 생성 허용

## 6. 예외 규칙(중요)

`오늘의 업무/일정` 항목의 **예상 업무 시간이 전부 비어 있는 경우**:

- Tasks 자동 생성을 하지 않음
- 사용자에게 시간 할당을 요청하는 분기로 처리

수동 시간 지정 후 실행 예시:

```powershell
python scripts/syncPlanner.py --assign-time "큐랩 실무 담당 선생님 연락=09:00~09:30" --assign-time "씨어스 회의록 작성=16:00~16:30"
```

## 7. 우선순위

값 적용 우선순위:

1. CLI 인자
2. 환경변수
3. 설정 파일(config.json)
4. 기본값

## 8. 환경변수(선택)

- `GWS_DOC_SYNC_DOC`
- `GWS_DOC_SYNC_TZ`
- `GWS_DOC_SYNC_CALENDAR`
- `GWS_DOC_SYNC_TASKLIST`
- `GWS_CLI_PATH`
- `GWS_DOC_SYNC_CONFIG`

## 9. 공유 시 주의사항

- 스킬 폴더 전체를 공유하세요 (`SKILL.md`만 공유하면 동작 불가)
- 개인 인증/토큰 파일은 공유하지 마세요
- `config.json`은 개인 설정값이라 보통 공유하지 않는 것을 권장합니다
