# Android Mapping

## Contents
- Units
- Layout
- Typography
- Visual styling
- State and responsive behavior
- Unsupported or partial mappings

## Units
- `px`: map to `dp` for layout and `sp` for text as the starting heuristic.
- `rem`, `em`: resolve from the source font context before converting.
- `%`: map to constraints, `layout_weight`, guidelines, or `BoxWithConstraints`.
- `vw`, `vh`: approximate with screen/window constraints; avoid pretending Android has a direct equivalent.

## Layout
- `display: flex`: use `LinearLayout`, `ConstraintLayout`, or Compose `Row`/`Column`/`Box`.
- `flex-direction: row|column`: use horizontal or vertical layout direction.
- `justify-content`: map to gravity, chains, weights, or Compose `Arrangement`.
- `align-items`, `align-self`: map to gravity, layout gravity, alignment lines, or Compose `Alignment`.
- `gap`: use margins in XML or `Arrangement.spacedBy(...)` in Compose.
- `flex-wrap`: approximate with `FlexboxLayout`, Flow helpers, or a lazy grid when needed.
- `display: grid`: use `ConstraintLayout`, `GridLayout`, or Compose lazy grids; do not claim full CSS grid parity.
- `position: relative`: default Android layout behavior.
- `position: absolute`: use `FrameLayout`, `ConstraintLayout`, or Compose `Box` plus `offset`.
- `position: fixed`, `position: sticky`: no direct equivalent; redesign with app bars, nested scrolling, or anchored containers.
- `top`, `right`, `bottom`, `left`: map to constraints, margins, offsets, or paddings depending on context.
- `z-index`: map to elevation, child order, or Compose `zIndex`.
- `overflow: hidden`: use clipping or rounded clipping.
- `overflow: scroll`: use `ScrollView`, `NestedScrollView`, `RecyclerView`, `LazyColumn`, or `LazyRow`.

## Typography
- `font-size`: map to `sp`.
- `font-family`: use Android font resources or Compose `FontFamily`; mention if the font asset is missing.
- `font-weight`: map to available Android font weights or bold style.
- `line-height`: map to `android:lineSpacingExtra`, text appearance, or Compose `lineHeight`.
- `letter-spacing`: map to `android:letterSpacing` or Compose `letterSpacing`.
- `text-align`: map to gravity, text alignment, or Compose `TextAlign`.
- `text-transform`: pre-transform the string or use helper logic; Android has no general XML-only equivalent.
- `text-decoration`: map to underline or strike-through flags.
- `white-space`: approximate with line limits, `ellipsize`, and wrapping behavior.

## Visual styling
- `color`: map to `@color/...` or Compose `Color(...)`.
- `background-color`: use `android:background`, drawable shapes, or Compose `background(...)`.
- `background-image`: use `ImageView`, layered drawables, or Compose `Image` plus overlays.
- `linear-gradient`, `radial-gradient`: use gradient drawables or Compose `Brush`.
- `border`: use `shape` drawables in XML or `border(...)` in Compose.
- `border-radius`: use rounded shape drawables or `RoundedCornerShape`.
- `opacity`: use `alpha`.
- `box-shadow`: approximate with elevation, shadow layers, or Compose shadow modifiers; exact CSS blur/spread parity is limited.
- `filter`, `backdrop-filter`: limited support; use blur APIs only when clearly available and acceptable.
- `transform`: use rotation, scale, translation, and Compose `graphicsLayer`; complex transform stacks may need approximation.

## State and responsive behavior
- `:hover`: usually ignore on touch UI unless mouse or TV input matters.
- `:active`, `:pressed`: map to pressed selectors or interaction states.
- `:focus`: map to focused state and focusable behavior.
- `:disabled`: map to enabled/disabled state.
- `:before`, `:after`: replace with explicit child nodes or drawables.
- Media queries: use resource qualifiers, window size classes, or Compose window-aware branching.
- CSS variables: map to theme colors, dimens, typography tokens, or local constants.

## Unsupported or partial mappings
- CSS grid auto-placement is not a one-to-one Android feature.
- Browser layout features tied to inline formatting context do not map directly.
- Blend modes and complex masking often need custom drawing.
- Fixed viewport behavior, sticky positioning, and backdrop effects usually require Android-specific redesign.
- If exact parity is impossible, explain the closest Android-native alternative instead of hiding the limitation.
