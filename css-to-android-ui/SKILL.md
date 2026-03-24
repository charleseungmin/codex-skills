---
name: css-to-android-ui
description: Convert CSS-driven UI definitions into Android View XML or Jetpack Compose code. Use when Codex receives CSS, HTML/CSS snippets, design tokens, styled web components, or requests to explain how web styling maps to Android UI primitives, especially when layout, spacing, typography, borders, shadows, or responsive behavior must be recreated in Android.
---

# CSS to Android UI

## Overview

Translate web-style UI definitions into Android-native implementations without copying web patterns blindly. Pick XML for View-based screens or explicit XML requests, and pick Compose for Compose-first codebases or explicit Compose requests.

## Workflow

1. Inspect the source input.
   - Separate structure from style.
   - Extract CSS variables, repeated tokens, state variants, and responsive rules.
   - Note assets, gradients, shadows, transforms, and pseudo-elements.
2. Choose the Android target first.
   - Use Android XML when the surrounding code uses `View`, `Fragment`, `RecyclerView`, or existing layout resources.
   - Use Compose when the surrounding code already uses Compose or the user explicitly asks for Compose.
   - If there is no project context and the user does not choose, prefer Compose for new isolated UI and state that assumption.
3. Rebuild layout intent before fine styling.
   - Convert flex and grid intent into Android layout primitives first.
   - Match hierarchy, spacing, alignment, and sizing before colors, borders, and shadows.
4. Translate styles with Android-native mechanisms.
   - Read [android-mapping.md](./references/android-mapping.md) for property mapping and fallback rules.
   - In XML, emit extra resources only when needed: `shape` drawables, selectors, colors, dimens, and styles.
   - In Compose, prefer `Modifier`, `TextStyle`, `Shape`, `Brush`, and small helper composables instead of duplicating inline values everywhere.
5. Resolve unsupported web behavior explicitly.
   - Replace pseudo-elements with explicit child views or composables.
   - Replace CSS-only behavior such as `position: sticky`, `backdrop-filter`, complex blend modes, or grid auto-placement with the closest Android-native behavior.
   - Call out any fidelity gaps instead of pretending they are fully supported.
6. Return complete Android output.
   - For XML, include the layout and any required supporting XML snippets.
   - For Compose, include the composable and any supporting constants or helper code needed to compile.
7. Verify the result.
   - Check padding, alignment, type scale, corner radius, shadow treatment, clipping, and state handling.
   - Mention assumptions about assets, fonts, and responsive behavior.

## Conversion Rules

- Treat CSS `px` values as Android `dp` for layout and `sp` for text unless the input already defines another scale. Keep the same numeric value as the starting point, then adjust only when the source context clearly implies a different base.
- Convert `rem` and `em` only after identifying the relevant base font size.
- Prefer `ConstraintLayout` or Compose `ConstraintLayout`/`BoxWithConstraints` when the CSS relies on percentages, overlap, or complex positioning.
- Prefer `LinearLayout` or Compose `Row`/`Column` when the CSS is simple flex layout in a single direction.
- Preserve semantic grouping. Do not flatten important nested structure just because Android can technically draw it with fewer nodes.
- Keep XML resource names in `snake_case`.
- Use `sp` for text sizes, `dp` for layout dimensions, and resource colors instead of hardcoding repeated values in XML outputs.
- When CSS includes interaction states such as hover, focus, or active, map them to Android pressed, focused, selected, enabled, or interaction-driven Compose states where practical.

## Output Expectations

- Emit compilable code rather than partial fragments when the user asks for a full conversion.
- Include supporting XML resources when the main layout depends on them.
- Keep comments short and only explain non-obvious fallbacks.
- State any lossy conversions clearly, especially for CSS grid, filters, sticky/fixed positioning, and browser-specific behavior.

## Reference

- Read [android-mapping.md](./references/android-mapping.md) whenever the request includes non-trivial CSS properties, flex/grid behavior, gradients, shadows, or responsive rules.
