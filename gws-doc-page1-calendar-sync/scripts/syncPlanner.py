#!/usr/bin/env python3
"""
Google Docs 1페이지 플래너를 Google Calendar + Google Tasks로 동기화한다.

핵심 규칙:
- 1페이지의 "오늘의 업무/일정" 섹션만 처리
- 시간 표기(HH:MM ~ HH:MM) 행은 Calendar 이벤트 생성
- 시간 미표기 행은 Tasks 할 일 생성
- 중복 생성 허용
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional
from zoneinfo import ZoneInfo


@dataclass
class TimedEntry:
    title: str
    startTime: str
    endTime: str


@dataclass
class UntimedEntry:
    title: str


def normalizeText(rawText: str) -> str:
    return " ".join((rawText or "").split())


def extractDocId(docInput: str) -> str:
    cleaned = (docInput or "").strip()
    if not cleaned:
        raise ValueError("문서 ID 또는 URL이 비어 있습니다.")

    if re.fullmatch(r"[A-Za-z0-9_-]{20,}", cleaned):
        return cleaned

    match = re.search(r"/document/d/([A-Za-z0-9_-]+)", cleaned)
    if match:
        return match.group(1)

    raise ValueError(f"문서 ID를 추출할 수 없습니다: {docInput}")


def resolveConfigPath(configPathArg: Optional[str]) -> Path:
    try:
        if configPathArg:
            return Path(configPathArg).expanduser().resolve()

        envConfigPath = os.getenv("GWS_DOC_SYNC_CONFIG", "").strip()
        if envConfigPath:
            return Path(envConfigPath).expanduser().resolve()

        codexHome = os.getenv("CODEX_HOME", "").strip()
        basePath = Path(codexHome).expanduser() if codexHome else (Path.home() / ".codex")
        return (basePath / "skills-data" / "gws-doc-page1-calendar-sync" / "config.json").resolve()
    except Exception as exc:
        raise RuntimeError(f"설정 파일 경로 확인 중 오류가 발생했습니다: {exc}") from exc


def loadConfig(configPath: Path) -> dict[str, Any]:
    try:
        if not configPath.exists():
            return {}

        text = configPath.read_text(encoding="utf-8")
        parsed = json.loads(text)
        if not isinstance(parsed, dict):
            raise ValueError("설정 파일 루트는 JSON object여야 합니다.")
        return parsed
    except Exception as exc:
        raise RuntimeError(f"설정 파일 로드 실패: {configPath} / {exc}") from exc


def saveConfig(configPath: Path, configData: dict[str, Any]) -> None:
    try:
        configPath.parent.mkdir(parents=True, exist_ok=True)
        configPath.write_text(
            json.dumps(configData, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as exc:
        raise RuntimeError(f"설정 파일 저장 실패: {configPath} / {exc}") from exc


def resolveSetting(
    cliValue: Optional[str],
    envVarName: str,
    configData: dict[str, Any],
    configKey: str,
    defaultValue: Optional[str] = None,
) -> Optional[str]:
    if cliValue is not None and str(cliValue).strip() != "":
        return str(cliValue).strip()

    envValue = os.getenv(envVarName, "").strip()
    if envValue:
        return envValue

    configValue = configData.get(configKey)
    if isinstance(configValue, str) and configValue.strip():
        return configValue.strip()

    return defaultValue


def setupConfigInteractively(configPath: Path, currentConfig: dict[str, Any]) -> dict[str, Any]:
    try:
        # 최초 설정/링크 변경 분기:
        # 사용자 입력을 받아 기본 문서 링크와 실행 기본값을 config.json에 저장한다.
        updatedConfig = dict(currentConfig)

        existingDoc = str(updatedConfig.get("doc", "")).strip()
        while True:
            docPrompt = "기본 문서 URL/ID를 입력하세요"
            if existingDoc:
                docPrompt += f" (Enter 시 기존 값 유지: {existingDoc})"
            docPrompt += ": "
            docInput = input(docPrompt).strip()

            if not docInput and existingDoc:
                docInput = existingDoc

            try:
                _ = extractDocId(docInput)
                updatedConfig["doc"] = docInput
                break
            except Exception as exc:
                print(f"[WARN] 유효한 문서 URL/ID가 아닙니다: {exc}")

        existingTimezone = str(updatedConfig.get("timezone", "Asia/Seoul")).strip() or "Asia/Seoul"
        timezoneInput = input(
            f"기본 timezone 입력 (Enter 시 {existingTimezone}): "
        ).strip()
        updatedConfig["timezone"] = timezoneInput if timezoneInput else existingTimezone

        existingCalendar = str(updatedConfig.get("calendarId", "primary")).strip() or "primary"
        calendarInput = input(
            f"기본 calendarId 입력 (Enter 시 {existingCalendar}): "
        ).strip()
        updatedConfig["calendarId"] = calendarInput if calendarInput else existingCalendar

        existingTasklist = str(updatedConfig.get("tasklistId", "")).strip()
        tasklistPrompt = "기본 tasklistId 입력 (Enter 시 자동 선택 유지)"
        if existingTasklist:
            tasklistPrompt = (
                f"기본 tasklistId 입력 (Enter 시 기존 값 유지: {existingTasklist})"
            )
        tasklistInput = input(tasklistPrompt + ": ").strip()
        if tasklistInput:
            updatedConfig["tasklistId"] = tasklistInput
        elif existingTasklist:
            updatedConfig["tasklistId"] = existingTasklist
        else:
            updatedConfig.pop("tasklistId", None)

        saveConfig(configPath, updatedConfig)
        return updatedConfig
    except Exception as exc:
        raise RuntimeError(f"초기 설정 처리 중 오류가 발생했습니다: {exc}") from exc


def resolveGwsPath(cliPathArg: Optional[str]) -> str:
    try:
        candidates: list[str] = []
        if cliPathArg:
            candidates.append(cliPathArg)

        envPath = os.getenv("GWS_CLI_PATH")
        if envPath:
            candidates.append(envPath)

        # Windows 환경에서는 gws.cmd를 우선 사용해야 subprocess에서 안정적으로 실행된다.
        candidates.extend(
            [
                "gws.cmd",
                "gws",
                r"C:\Program Files\nodejs\gws.cmd",
            ]
        )

        for candidate in candidates:
            candidatePath = Path(candidate)
            if candidatePath.is_file():
                return str(candidatePath)

            resolved = shutil.which(candidate)
            if resolved:
                return resolved

        raise FileNotFoundError(
            "gws 실행 파일을 찾을 수 없습니다. gws 설치 또는 --gws-path/GWS_CLI_PATH 설정이 필요합니다."
        )
    except Exception as exc:
        raise RuntimeError(f"gws 경로 확인 중 오류가 발생했습니다: {exc}") from exc


class GwsClient:
    def __init__(self, gwsPath: str) -> None:
        self.gwsPath = gwsPath

    def runJson(self, args: list[str]) -> dict[str, Any]:
        command = [self.gwsPath, *args]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        except Exception as exc:
            raise RuntimeError(f"gws 실행 실패: {' '.join(command)} / {exc}") from exc

        if result.returncode != 0:
            raise RuntimeError(
                "gws 호출 실패\n"
                f"command: {' '.join(command)}\n"
                f"stdout: {result.stdout.strip()}\n"
                f"stderr: {result.stderr.strip()}"
            )

        stdout = (result.stdout or "").strip()
        if not stdout:
            return {}

        try:
            return json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "gws 응답 JSON 파싱 실패\n"
                f"command: {' '.join(command)}\n"
                f"raw stdout: {stdout[:500]}"
            ) from exc


def extractCellText(tableCell: dict[str, Any]) -> str:
    textChunks: list[str] = []
    for contentItem in tableCell.get("content", []):
        paragraph = contentItem.get("paragraph")
        if not paragraph:
            continue

        for element in paragraph.get("elements", []):
            textRun = element.get("textRun")
            if textRun:
                textChunks.append(textRun.get("content", ""))

    return normalizeText("".join(textChunks))


def buildTableRows(table: dict[str, Any]) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in table.get("tableRows", []):
        cells: list[str] = []
        for cell in row.get("tableCells", []):
            cells.append(extractCellText(cell))
        rows.append(cells)
    return rows


def findFirstPagePlannerRows(document: dict[str, Any]) -> list[list[str]]:
    try:
        contentBlocks = document.get("body", {}).get("content", [])
        for block in contentBlocks:
            table = block.get("table")
            if not table:
                continue

            rows = buildTableRows(table)
            hasScheduleHeader = any(
                len(row) > 0 and row[0] == "오늘의 업무/일정" for row in rows
            )
            if hasScheduleHeader:
                return rows
    except Exception as exc:
        raise RuntimeError(f"문서 테이블 파싱 중 오류가 발생했습니다: {exc}") from exc

    raise ValueError("1페이지 플래너 테이블(오늘의 업무/일정)을 찾지 못했습니다.")


def parseFlexibleDate(rawText: str) -> Optional[date]:
    cleaned = normalizeText(rawText).replace(" ", "")
    match = re.search(r"(\d{4})[./-](\d{1,2})[./-](\d{1,2})", cleaned)
    if not match:
        return None

    year, month, day = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    try:
        return date(year, month, day)
    except ValueError:
        return None


def extractPlannerDate(rows: list[list[str]]) -> Optional[date]:
    for row in rows[:5]:
        for index, value in enumerate(row):
            if value == "날짜" and index + 1 < len(row):
                parsed = parseFlexibleDate(row[index + 1])
                if parsed:
                    return parsed
    return None


def extractScheduleEntries(rows: list[list[str]]) -> tuple[list[TimedEntry], list[UntimedEntry]]:
    headerIndex = -1
    for idx, row in enumerate(rows):
        if len(row) > 0 and row[0] == "오늘의 업무/일정":
            headerIndex = idx
            break

    if headerIndex < 0:
        raise ValueError("'오늘의 업무/일정' 헤더를 찾지 못했습니다.")

    timePattern = re.compile(r"^(\d{1,2}:\d{2})\s*~\s*(\d{1,2}:\d{2})$")
    timedEntries: list[TimedEntry] = []
    untimedEntries: list[UntimedEntry] = []

    for row in rows[headerIndex + 1 :]:
        title = row[0].strip() if len(row) > 0 and row[0] else ""
        if not title:
            continue

        if title in ("Memo", "메모"):
            break

        timeText = row[4].strip() if len(row) > 4 and row[4] else ""
        match = timePattern.match(timeText)
        if match:
            timedEntries.append(
                TimedEntry(
                    title=title,
                    startTime=match.group(1),
                    endTime=match.group(2),
                )
            )
        else:
            untimedEntries.append(UntimedEntry(title=title))

    if not timedEntries and not untimedEntries:
        raise ValueError("추출된 일정/할 일 항목이 없습니다.")

    return timedEntries, untimedEntries


def parseManualTimeAssignments(assignTimeArgs: list[str]) -> dict[str, tuple[str, str]]:
    try:
        # 수동 시간 할당 포맷: "업무제목=09:00~10:00"
        # 제목이 동일한 항목이 여러 개인 경우 같은 시간을 일괄 적용한다.
        parsed: dict[str, tuple[str, str]] = {}
        timePattern = re.compile(r"^(\d{1,2}:\d{2})\s*~\s*(\d{1,2}:\d{2})$")
        for rawItem in assignTimeArgs:
            item = (rawItem or "").strip()
            if "=" not in item:
                raise ValueError(
                    f"--assign-time 형식 오류: '{rawItem}'. 예시: --assign-time \"업무=09:00~10:00\""
                )

            title, timeRange = item.split("=", 1)
            title = normalizeText(title)
            timeRange = normalizeText(timeRange)
            if not title:
                raise ValueError(f"--assign-time 제목이 비어 있습니다: '{rawItem}'")

            matched = timePattern.match(timeRange)
            if not matched:
                raise ValueError(
                    f"--assign-time 시간 형식 오류: '{rawItem}'. HH:MM~HH:MM 형식이 필요합니다."
                )

            parsed[title] = (matched.group(1), matched.group(2))
        return parsed
    except Exception as exc:
        raise RuntimeError(f"수동 시간 할당값 파싱 중 오류가 발생했습니다: {exc}") from exc


def applyManualAssignments(
    untimedEntries: list[UntimedEntry],
    manualAssignments: dict[str, tuple[str, str]],
) -> tuple[list[TimedEntry], list[UntimedEntry]]:
    try:
        convertedEntries: list[TimedEntry] = []
        remainingEntries: list[UntimedEntry] = []
        for entry in untimedEntries:
            matched = manualAssignments.get(entry.title)
            if matched:
                convertedEntries.append(
                    TimedEntry(title=entry.title, startTime=matched[0], endTime=matched[1])
                )
            else:
                remainingEntries.append(entry)
        return convertedEntries, remainingEntries
    except Exception as exc:
        raise RuntimeError(f"수동 시간 매핑 적용 중 오류가 발생했습니다: {exc}") from exc


def promptManualAssignments(
    untimedEntries: list[UntimedEntry],
) -> tuple[list[TimedEntry], list[UntimedEntry]]:
    try:
        convertedEntries: list[TimedEntry] = []
        remainingEntries: list[UntimedEntry] = []
        timePattern = re.compile(r"^(\d{1,2}:\d{2})\s*~\s*(\d{1,2}:\d{2})$")

        # 시간 미기재 문서 분기:
        # Tasks로 넘기지 않고 사용자에게 직접 시간 입력을 받아 이벤트로 전환한다.
        print(
            "[INFO] 문서의 예상 업무 시간이 비어 있습니다. "
            "아래 항목별로 HH:MM~HH:MM 형식 시간을 입력하세요. (Enter 입력 시 건너뜀)"
        )
        for entry in untimedEntries:
            while True:
                rawInput = input(f"시간 입력 - {entry.title}: ").strip()
                if not rawInput:
                    remainingEntries.append(entry)
                    break

                matched = timePattern.match(normalizeText(rawInput))
                if not matched:
                    print("[WARN] 형식 오류입니다. 예: 09:00~10:30")
                    continue

                convertedEntries.append(
                    TimedEntry(
                        title=entry.title,
                        startTime=matched.group(1),
                        endTime=matched.group(2),
                    )
                )
                break

        return convertedEntries, remainingEntries
    except Exception as exc:
        raise RuntimeError(f"대화형 시간 입력 처리 중 오류가 발생했습니다: {exc}") from exc


def resolveTargetDate(
    inputDate: Optional[str], plannerDate: Optional[date], timezoneName: str
) -> date:
    if inputDate:
        try:
            return datetime.strptime(inputDate, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError("--date 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해 주세요.") from exc

    if plannerDate:
        return plannerDate

    timezoneInfo = ZoneInfo(timezoneName)
    return datetime.now(timezoneInfo).date()


def makeDateTimeIso(targetDate: date, hhmm: str, timezoneName: str) -> str:
    hour, minute = map(int, hhmm.split(":"))
    timezoneInfo = ZoneInfo(timezoneName)
    return datetime(
        targetDate.year,
        targetDate.month,
        targetDate.day,
        hour,
        minute,
        tzinfo=timezoneInfo,
    ).isoformat()


def resolveTasklistId(gwsClient: GwsClient, explicitTasklistId: Optional[str]) -> str:
    if explicitTasklistId:
        return explicitTasklistId

    listed = gwsClient.runJson(["tasks", "tasklists", "list"])
    items = listed.get("items", [])
    if not items:
        raise RuntimeError("사용 가능한 Google Tasks 목록이 없습니다.")

    return items[0]["id"]


def createCalendarEvent(
    gwsClient: GwsClient,
    calendarId: str,
    timezoneName: str,
    targetDate: date,
    entry: TimedEntry,
    description: str,
) -> dict[str, Any]:
    startIso = makeDateTimeIso(targetDate, entry.startTime, timezoneName)
    endIso = makeDateTimeIso(targetDate, entry.endTime, timezoneName)
    return gwsClient.runJson(
        [
            "calendar",
            "+insert",
            "--calendar",
            calendarId,
            "--summary",
            entry.title,
            "--start",
            startIso,
            "--end",
            endIso,
            "--description",
            description,
        ]
    )


def createTask(
    gwsClient: GwsClient,
    tasklistId: str,
    targetDate: date,
    entry: UntimedEntry,
    description: str,
) -> dict[str, Any]:
    payload = {
        "title": entry.title,
        "notes": f"{description} | 시간 미지정 항목",
        "due": f"{targetDate.isoformat()}T00:00:00Z",
        "status": "needsAction",
    }
    return gwsClient.runJson(
        [
            "tasks",
            "tasks",
            "insert",
            "--params",
            json.dumps({"tasklist": tasklistId}, ensure_ascii=False),
            "--json",
            json.dumps(payload, ensure_ascii=False),
        ]
    )


def parseArguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Google Docs 1페이지 플래너를 Calendar/Tasks로 동기화한다."
    )
    parser.add_argument(
        "--doc",
        default=None,
        help="Google Docs URL 또는 documentId (미지정 시 설정 파일/환경변수에서 로딩)",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="대상 날짜(YYYY-MM-DD). 미지정 시 문서 헤더 날짜를 사용",
    )
    parser.add_argument(
        "--timezone",
        default=None,
        help="이벤트 생성 타임존",
    )
    parser.add_argument(
        "--calendar-id",
        default=None,
        help="Google Calendar ID",
    )
    parser.add_argument(
        "--tasklist-id",
        default=None,
        help="Google Tasks list ID (미지정 시 첫 번째 목록 자동 선택)",
    )
    parser.add_argument(
        "--gws-path",
        default=None,
        help="gws 실행 파일 경로",
    )
    parser.add_argument(
        "--config-path",
        default=None,
        help="설정 파일 경로 (미지정 시 ~/.codex/skills-data/.../config.json)",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="최초 설정/변경 모드 (문서 링크 등 기본값 입력)",
    )
    parser.add_argument(
        "--set-doc",
        default=None,
        help="기본 문서 URL/ID를 즉시 변경하고 종료",
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="현재 설정 파일 내용을 출력하고 종료",
    )
    parser.add_argument(
        "--assign-time",
        action="append",
        default=[],
        help='시간 미기재 항목 수동 시간 지정. 형식: "업무제목=09:00~10:00" (반복 가능)',
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="쓰기 없이 파싱 결과와 생성 예정 항목만 출력",
    )
    return parser.parse_args()


def main() -> int:
    args = parseArguments()

    try:
        configPath = resolveConfigPath(args.config_path)
        configData = loadConfig(configPath)

        if args.setup:
            updated = setupConfigInteractively(configPath, configData)
            print(
                json.dumps(
                    {
                        "message": "설정이 저장되었습니다.",
                        "configPath": str(configPath),
                        "config": updated,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        if args.set_doc:
            _ = extractDocId(args.set_doc)
            configData["doc"] = args.set_doc.strip()
            saveConfig(configPath, configData)
            print(
                json.dumps(
                    {
                        "message": "기본 문서 링크가 저장되었습니다.",
                        "configPath": str(configPath),
                        "doc": configData["doc"],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        if args.show_config:
            print(
                json.dumps(
                    {
                        "configPath": str(configPath),
                        "config": configData,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        docInput = resolveSetting(args.doc, "GWS_DOC_SYNC_DOC", configData, "doc", None)
        if not docInput:
            raise ValueError(
                "문서 링크가 설정되지 않았습니다. "
                "`--setup` 또는 `--set-doc \"<URL 또는 ID>\"`로 먼저 설정해 주세요."
            )

        timezoneName = resolveSetting(
            args.timezone, "GWS_DOC_SYNC_TZ", configData, "timezone", "Asia/Seoul"
        )
        calendarId = resolveSetting(
            args.calendar_id, "GWS_DOC_SYNC_CALENDAR", configData, "calendarId", "primary"
        )
        tasklistIdFromSetting = resolveSetting(
            args.tasklist_id, "GWS_DOC_SYNC_TASKLIST", configData, "tasklistId", None
        )
        gwsPathHint = resolveSetting(args.gws_path, "GWS_CLI_PATH", configData, "gwsPath", None)

        docId = extractDocId(docInput)
        gwsPath = resolveGwsPath(gwsPathHint)
        gwsClient = GwsClient(gwsPath)

        document = gwsClient.runJson(
            [
                "docs",
                "documents",
                "get",
                "--params",
                json.dumps({"documentId": docId}, ensure_ascii=False),
            ]
        )

        plannerRows = findFirstPagePlannerRows(document)
        plannerDate = extractPlannerDate(plannerRows)
        targetDate = resolveTargetDate(args.date, plannerDate, str(timezoneName))
        timedEntries, untimedEntries = extractScheduleEntries(plannerRows)
        manualAssignments = parseManualTimeAssignments(args.assign_time)
        allRowsUntimed = len(timedEntries) == 0 and len(untimedEntries) > 0
        manualAssignedCount = 0
        pendingManualTimeTitles: list[str] = []

        if allRowsUntimed:
            convertedByArg, untimedEntries = applyManualAssignments(untimedEntries, manualAssignments)
            timedEntries.extend(convertedByArg)
            manualAssignedCount += len(convertedByArg)

            canPromptUser = (not args.dry_run) and sys.stdin.isatty() and sys.stdout.isatty()
            if untimedEntries and canPromptUser:
                convertedByPrompt, untimedEntries = promptManualAssignments(untimedEntries)
                timedEntries.extend(convertedByPrompt)
                manualAssignedCount += len(convertedByPrompt)

            if untimedEntries:
                pendingManualTimeTitles = [item.title for item in untimedEntries]

        description = (
            f"출처: Google Docs({docId}) 1페이지 오늘의 업무/일정 | "
            "실행 규칙: 1페이지 기준, 시간표시=일정, 시간미표시=할일(단, 전체 시간미기재 시 사용자 시간할당), 중복 허용"
        )

        summary: dict[str, Any] = {
            "docId": docId,
            "targetDate": targetDate.isoformat(),
            "timezone": timezoneName,
            "calendarId": calendarId,
            "configPath": str(configPath),
            "dryRun": args.dry_run,
            "allRowsUntimed": allRowsUntimed,
            "manualTimeAssignedCount": manualAssignedCount,
            "requiresManualTimeAssignment": len(pendingManualTimeTitles) > 0,
            "pendingManualTimeTitles": pendingManualTimeTitles,
            "timedCount": len(timedEntries),
            "untimedCount": len(untimedEntries),
            "events": [],
            "tasks": [],
        }

        if args.dry_run:
            for item in timedEntries:
                summary["events"].append(
                    {
                        "title": item.title,
                        "start": makeDateTimeIso(targetDate, item.startTime, str(timezoneName)),
                        "end": makeDateTimeIso(targetDate, item.endTime, str(timezoneName)),
                    }
                )
            # 전체 항목이 시간 미기재인 문서는 할 일을 만들지 않고 사용자 시간 할당을 우선한다.
            if allRowsUntimed:
                summary["message"] = (
                    "예상 업무 시간이 전부 비어 있어 할 일 자동 생성을 중지했습니다. "
                    "사용자에게 시간 할당을 받은 뒤 다시 실행하세요."
                )
            else:
                for item in untimedEntries:
                    summary["tasks"].append(
                        {
                            "title": item.title,
                            "due": f"{targetDate.isoformat()}T00:00:00Z",
                        }
                    )
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0

        if allRowsUntimed and not timedEntries and pendingManualTimeTitles:
            summary["message"] = (
                "예상 업무 시간이 전부 비어 있어 캘린더/할 일 생성을 보류했습니다. "
                "시간을 지정해 다시 실행하세요. "
                "예시: --assign-time \"업무=09:00~10:00\""
            )
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0

        for item in timedEntries:
            created = createCalendarEvent(
                gwsClient=gwsClient,
                calendarId=str(calendarId),
                timezoneName=str(timezoneName),
                targetDate=targetDate,
                entry=item,
                description=description,
            )
            summary["events"].append(
                {
                    "title": item.title,
                    "id": created.get("id"),
                    "htmlLink": created.get("htmlLink"),
                }
            )

        # 전체 항목이 시간 미기재였던 경우는 Tasks 자동 생성을 금지한다.
        if untimedEntries and (not allRowsUntimed):
            tasklistId = resolveTasklistId(gwsClient, tasklistIdFromSetting)
            summary["tasklistId"] = tasklistId
            for item in untimedEntries:
                createdTask = createTask(
                    gwsClient=gwsClient,
                    tasklistId=tasklistId,
                    targetDate=targetDate,
                    entry=item,
                    description=description,
                )
                summary["tasks"].append(
                    {
                        "title": item.title,
                        "id": createdTask.get("id"),
                        "webViewLink": createdTask.get("webViewLink"),
                    }
                )
        elif untimedEntries and allRowsUntimed:
            summary["message"] = (
                "일부 항목은 시간이 지정되지 않아 생성하지 않았습니다. "
                "시간을 지정해 재실행하면 이벤트로 등록됩니다."
            )

        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
