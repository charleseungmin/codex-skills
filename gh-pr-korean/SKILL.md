---
name: gh-pr-korean
description: GitHub CLI로 현재 브랜치를 push하고, 한글 제목과 본문을 포함한 PR을 생성하거나 갱신한다. 사용자가 PR 생성, Draft 또는 Ready 판단, PR 템플릿 반영, Mermaid 플로우차트 포함, 한글 인코딩 안전 처리까지 함께 요청할 때 사용한다.
---

# Gh PR Korean

## Overview

이 스킬은 현재 브랜치를 원격에 push하고, 한글 제목과 본문이 깨지지 않도록 UTF-8 파일 기반으로 GitHub PR을 생성하거나 갱신한다.
PR 템플릿 채우기, Draft 또는 Ready 판단, Mermaid 플로우차트 포함, 생성 후 URL 검증까지 한 번에 처리한다.

## Trigger

- 사용자가 PR 생성, PR 갱신, 브랜치 push 후 PR 생성, Draft PR 생성, PR 본문 작성 중 하나를 요청한 경우
- PR 제목 또는 본문을 한글로 작성해야 하는 경우
- PR 본문에 테스트 결과, 리뷰 포인트, Mermaid 플로우차트를 넣어야 하는 경우
- Windows 또는 PowerShell 환경에서 한글 인코딩 깨짐을 피해야 하는 경우

## Workflow

1. 현재 상태를 확인한다.
- `git branch --show-current`
- `git status --short`
- `git remote -v`
- `git ls-remote --symref origin HEAD`
- `gh auth status`
- 저장소에 PR 템플릿이 있으면 먼저 읽고 섹션 구조를 유지한다.

2. push 대상을 정리한다.
- 사용자가 요청한 변경만 커밋돼 있는지 확인한다.
- 원격 추적 브랜치가 없으면 `git push -u origin <branch>`를 사용한다.
- 이미 추적 중이면 `git push origin <branch>`를 사용한다.

3. PR 상태를 결정한다.
- 아래 조건 중 하나라도 있으면 기본값은 Draft다.
- 게이트 미수행
- 테스트 실패
- 리뷰 차단 사항 존재
- 구현 또는 문서가 아직 미완
- 위 조건이 없고 사용자가 별도로 원하면 Ready PR로 생성할 수 있다.

4. PR 본문을 한국어로 작성한다.
- 저장소 템플릿이 있으면 그 섹션 순서를 우선한다.
- 템플릿이 없으면 최소한 `Summary`, `Changes`, `How to test`, `Docs`, `Gate&Review status`를 포함한다.
- 이슈 번호는 확인된 경우에만 넣는다. 추정해서 쓰지 않는다.
- 플로우차트 요청이 있으면 Mermaid 코드 블록을 포함하고, 노드 라벨은 기본적으로 한국어로 쓴다.

5. 인코딩이 깨지지 않도록 파일 기반으로 작성한다.
- 한글이 들어가는 본문이나 JSON payload는 인라인 셸 인수로 직접 넘기지 않는다.
- `scripts/write_utf8.py`로 `body.md` 또는 `payload.json`을 UTF-8로 저장한다.
- 저장 후에는 `Get-Content -Raw -Encoding UTF8 <file>`로 다시 읽어 한글이 정상인지 확인한다.
- Windows 환경에서는 `gh pr create --body`보다 `--body-file` 또는 `gh api --input`을 우선한다.

6. 기존 PR 존재 여부를 확인한다.
- `gh pr list --head <branch> --json number,url,isDraft,title`
- 같은 head 브랜치의 open PR이 있으면 새로 만들지 말고 갱신한다.
- 없으면 새 PR을 생성한다.

7. PR을 생성하거나 갱신한다.
- 새 PR 생성은 `gh api repos/<owner>/<repo>/pulls --method POST --input payload.json`을 우선 사용한다.
- 기존 PR 갱신은 `gh api repos/<owner>/<repo>/pulls/<number> --method PATCH --input payload.json`을 사용한다.
- 새 PR에서만 `draft` 값을 명시한다.
- 기존 PR은 사용자가 명시적으로 원하지 않는 한 Draft 또는 Ready 상태를 함부로 바꾸지 않는다.
- Ready 전환이 필요하면 `gh pr ready <number>`를 사용한다.

8. 생성 결과를 검증한다.
- `gh pr view <number> --json url,title,isDraft,baseRefName,headRefName`
- 터미널 출력이 깨져 보여도 JSON 결과 기준으로 제목과 URL을 다시 확인한다.

## Encoding Rules

- 이 스킬이 만드는 Markdown과 JSON 파일은 모두 UTF-8이어야 한다.
- CP949 또는 EUC-KR을 전제로 처리하지 않는다.
- 한글 본문은 `--body` 인라인 옵션보다 파일 기반 옵션을 우선한다.
- 인코딩이 의심되면 파일을 다시 UTF-8로 저장하고 재확인한 뒤에만 PR 생성 또는 갱신을 진행한다.
- 제목이 콘솔에서 깨져 보여도 PR 생성 직후 `gh pr view --json title,url`로 실제 저장값을 확인한다.

## Command Pattern

### 본문 파일 저장

```powershell
$body = @'
## Summary
- 요약

## Changes
- 변경 사항
'@
$body | python C:\Users\lenovo\.codex\skills\gh-pr-korean\scripts\write_utf8.py body.md
Get-Content -Raw -Encoding UTF8 .\body.md
```

### 새 PR payload 저장

```powershell
$payload = @{
  title = "한글 PR 제목"
  head = $branch
  base = $base
  body = Get-Content -Raw -Encoding UTF8 .\body.md
  draft = $true
} | ConvertTo-Json -Depth 5
$payload | python C:\Users\lenovo\.codex\skills\gh-pr-korean\scripts\write_utf8.py payload.json
gh api repos/$owner/$repo/pulls --method POST --input payload.json
```

### 기존 PR 갱신

```powershell
$payload = @{
  title = "수정된 한글 PR 제목"
  body = Get-Content -Raw -Encoding UTF8 .\body.md
} | ConvertTo-Json -Depth 5
$payload | python C:\Users\lenovo\.codex\skills\gh-pr-korean\scripts\write_utf8.py payload.json
gh api repos/$owner/$repo/pulls/$number --method PATCH --input payload.json
```

## Notes

- `gh`가 PATH에 없으면 전체 경로를 사용하거나 먼저 실행 가능 상태를 만든다.
- PR 본문에 코드 플로우차트가 필요하면 관련 코드부터 읽고 Mermaid를 실제 흐름 기준으로 작성한다.
- 사용자가 명시하지 않은 검증 결과는 PASS로 쓰지 않는다.
- PR 생성이 실패하면 인증, base 브랜치, head 브랜치, 권한, payload 인코딩 순서로 원인을 확인한다.
