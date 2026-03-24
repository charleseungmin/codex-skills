# Mermaid Guidelines

## Default Style
- Use `flowchart LR` by default.
- Put all node text in double quotes.
- Keep labels short enough to scan quickly.
- Write the final explanation and labels in Korean by default unless another language is requested.

## Recommended Node Patterns
- Start or entry: `A["화면 진입"]`
- Action: `B["초기화 실행"]`
- Decision: `C{"필수값 입력 완료?"}`
- Navigation: `D["측정 화면 이동"]`
- Dialog or bottom sheet: `E["설정 불러오기 다이얼로그 오픈"]`
- State update: `F["ViewModel 상태 업데이트"]`

## Edge Rules
- Put branch conditions on the edge.
- Example:
```mermaid
flowchart LR
    A["완료 버튼 탭"] --> B{"canComplete() 통과?"}
    B -->|"아니오"| C["토스트 노출"]
    B -->|"예"| D["측정 화면 이동"]
```

## Android Fragment Patterns

### 1. Fragment 초기화 흐름
```mermaid
flowchart LR
    A["onViewCreated"] --> B["뷰 초기화"]
    B --> C["초기 상태 렌더링"]
    C --> D["리스너 등록"]
    D --> E["옵저버 등록"]
    E --> F["초기 데이터 로드"]
```

### 2. 화면 내 버튼 분기
```mermaid
flowchart LR
    A["건너뛰기 버튼 탭"] --> B{"운동명 입력됨?"}
    B -->|"아니오"| C["운동명 필수 다이얼로그"]
    B -->|"예"| D["스킵 안내 다이얼로그"]
```

### 3. ViewModel 핵심 로직
```mermaid
flowchart LR
    A["initialize 호출"] --> B{"프로필/멤버 ID 유효?"}
    B -->|"아니오"| C["종료"]
    B -->|"예"| D["로딩 상태 true"]
    D --> E["데이터 로드"]
    E --> F["상태 업데이트"]
```

## Splitting Strategy
- One diagram for lifecycle and initialization.
- One diagram for major user actions.
- One diagram for ViewModel or UseCase branching if the UI calls into meaningful business logic.
- Split when a single diagram exceeds roughly 12 to 15 nodes or mixes unrelated concerns.

## What to Omit
- Trivial setter calls with no branch impact.
- Pure formatting helpers unless they affect business-visible branches.
- Boilerplate lifecycle cleanup unless the user asked for it.

## Output Template
```md
### Fragment 초기화 플로우

```mermaid
flowchart LR
    A["onViewCreated"] --> B["초기화"]
    B --> C["옵저버 등록"]
    C --> D["데이터 로드"]
```

### 완료 버튼 플로우

```mermaid
flowchart LR
    A["완료 버튼 탭"] --> B{"필수값 충족?"}
    B -->|"아니오"| C["토스트 노출"]
    B -->|"예"| D["다음 화면 이동"]
```
```
