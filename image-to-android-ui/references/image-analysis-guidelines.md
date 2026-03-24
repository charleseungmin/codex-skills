# Image Analysis Guidelines

## What to Extract from the Image
- Screen structure: app bar, body, bottom bar, modal, floating button.
- Primary groups: cards, sections, lists, forms, tabs, chips, banners.
- Repeated patterns: list items, buttons, badges, statistics blocks.
- Typography: headline, body, caption, emphasis.
- Visual styling: corner radius, border, fill color, shadow, divider, gradient.
- Assets: icons, avatars, illustrations, chart images.

## Android Target Selection
- Choose XML when the existing screen stack is View-based.
- Choose Compose when the screen or module already uses Compose.
- If the user does not specify and there is no surrounding code, default to Compose and state that choice.

## Layout Mapping Heuristics
- Vertical page sections: `LinearLayout` or Compose `Column`.
- Horizontal aligned controls: `LinearLayout` or Compose `Row`.
- Precise alignment or overlap: `ConstraintLayout` or Compose `Box`/`ConstraintLayout`.
- Scrollable content: `NestedScrollView`, `RecyclerView`, `LazyColumn`, or `LazyRow`.
- Repeated list cells: build an item layout or item composable instead of duplicating nodes.

## Styling Heuristics
- Rounded surfaces: shape drawable or `RoundedCornerShape`.
- Outlined controls: stroke drawable or `border(...)`.
- Elevated cards: `MaterialCardView` or Compose `shadow/elevation`.
- Gradient background: gradient drawable or Compose `Brush`.
- Dimmed or disabled state: alpha plus state-aware color.

## Uncertainty Rules
- Estimate spacing and sizing from relative proportions when exact values are not visible.
- Keep placeholder resource names for missing icons or illustrations.
- Do not guess hidden interactions that are not visually implied.
- Mention assumptions about typography, colors, and spacing when they are inferred.

## Output Pattern
```md
가정:
- 아이콘 리소스는 실제 프로젝트 자산으로 교체 필요
- 폰트는 프로젝트 기본 폰트를 사용한다고 가정

구현 방식:
- Compose 기준

```kotlin
// composable code
```
```
