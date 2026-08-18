---
name: gws-doc-page1-calendar-sync
description: Sync a Google Docs daily planner to Google Calendar and Google Tasks using gws CLI. Use when the user asks to run phrases like "실행", "문서 일정 등록", or "1페이지 기준으로 캘린더/할 일 반영". This skill reads only page 1 planner rows in "오늘의 업무/일정", creates Calendar events for timed rows, creates Tasks for untimed rows, and allows duplicate creation. If the section has no time values at all, stop task creation and request manual time assignment from the user.
---

# GWS Doc Page1 Calendar Sync

## Overview

Google Docs 플래너 문서의 1페이지를 기준으로 `오늘의 업무/일정` 항목을 읽어 일정과 할 일을 자동 생성한다.
시간이 있는 항목(`HH:MM ~ HH:MM`)은 Google Calendar 이벤트로, 시간이 없는 항목은 Google Tasks 항목으로 등록한다.
단, `오늘의 업무/일정`에서 시간이 전부 비어 있으면 Tasks를 만들지 않고 사용자 시간 할당을 먼저 받는다.

## Workflow

1. 문서 ID 또는 URL을 입력받아 Google Docs 본문을 조회한다.
2. 문서의 첫 번째 플래너 테이블(1페이지 기준)에서 `오늘의 업무/일정` 섹션을 찾는다.
3. 시간 범위가 있는 행은 캘린더 이벤트로 생성한다.
4. 시간 범위가 없는 행은 Tasks 할 일로 생성한다.
5. 단, 섹션 전체가 시간 미기재면 할 일 생성을 멈추고 사용자에게 시간 입력을 요청한다.
6. 중복은 허용하고, 생성된 리소스 링크를 결과로 반환한다.

## Conversation Mapping

- 사용자가 `실행`이라고 말하면 기본 실행(`python scripts/syncPlanner.py`)을 수행한다.
- 사용자가 `실행 YYYY-MM-DD` 형식으로 말하면 `--date`를 적용해 실행한다.
- 사용자가 `실행 점검만`이라고 말하면 `--dry-run`으로 실행한다.
- 사용자가 링크 변경을 요청하면 `--set-doc`로 기본 문서 링크를 갱신한다.
- 사용자가 초기 설정을 요청하면 `--setup`으로 설정 모드를 실행한다.

## Run Script

최초 설정(링크 저장):

```powershell
python scripts/syncPlanner.py --setup
```

기본 링크 변경:

```powershell
python scripts/syncPlanner.py --set-doc "https://docs.google.com/document/d/<DOC_ID>/edit"
```

기본 실행:

```powershell
python scripts/syncPlanner.py
```

날짜 지정 실행:

```powershell
python scripts/syncPlanner.py --date 2026-04-21
```

시간 미기재 항목 수동 시간 지정 후 실행:

```powershell
python scripts/syncPlanner.py --assign-time "큐랩 실무 담당 선생님 연락=09:00~09:30" --assign-time "씨어스 회의록 작성=16:00~16:30"
```

사전 점검(쓰기 없이 파싱 결과만 확인):

```powershell
python scripts/syncPlanner.py --doc "<DOC_ID>" --dry-run
```

## Defaults

- timezone: `Asia/Seoul`
- calendar: `primary`
- tasklist: 첫 번째 TaskList 자동 선택
- doc link: 최초 `--setup` 또는 `--set-doc`로 저장한 값 사용
- date: `--date` 미지정 시 문서 헤더의 `날짜` 값 사용, 없으면 오늘 날짜 사용
- duplicates: 항상 허용
- 예외 규칙: `오늘의 업무/일정`이 전부 시간 미기재면 Tasks 생성 금지, 사용자 시간 할당 필요

## 설정 우선순위

- `CLI 인자` > `환경변수` > `설정 파일(config.json)` > `기본값`
- 설정 파일 기본 경로: `~/.codex/skills-data/gws-doc-page1-calendar-sync/config.json`
- 경로 변경: `--config-path` 또는 `GWS_DOC_SYNC_CONFIG`

## Environment Variables (Optional)

- `GWS_DOC_SYNC_DOC`: 기본 문서 URL/ID
- `GWS_DOC_SYNC_TZ`: 기본 타임존
- `GWS_DOC_SYNC_CALENDAR`: 기본 캘린더 ID
- `GWS_DOC_SYNC_TASKLIST`: 기본 TaskList ID
- `GWS_CLI_PATH`: gws 실행 파일 경로
- `GWS_DOC_SYNC_CONFIG`: 설정 파일 경로

## Notes

- 우선순위 컬럼은 문서 폰트 특성상 아이콘 문자로 읽힐 수 있어 저장에 사용하지 않는다.
- 문서 형식이 크게 바뀌면 `references/format-notes.md`를 참고해 파서 규칙을 조정한다.
