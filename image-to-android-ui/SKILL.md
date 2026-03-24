---
name: image-to-android-ui
description: Implement UI images as Android View XML or Jetpack Compose code. Use when Codex receives screenshots, mockups, wireframes, design captures, exported image assets, or requests to recreate a visual UI from an image in Android, especially when layout hierarchy, spacing, typography, colors, shapes, and visible states must be translated into production-ready Android UI.
---

# Image to Android UI

## Overview

Analyze an image, infer the UI hierarchy and styling, and turn it into Android-native code instead of describing it vaguely. Choose XML for View-based screens or explicit XML requests, and choose Compose for Compose-first codebases or explicit Compose requests.

## Workflow

1. Inspect the image before writing code.
   - Identify the screen boundary, safe areas, top bars, cards, lists, buttons, fields, tabs, chips, and overlays.
   - Note likely layout grouping, alignment lines, repeated spacing, typography scale, icon usage, and image assets.
   - Distinguish actual UI from decorative background or capture artifacts.
2. Determine the Android target.
   - Use Android XML when the surrounding project uses Views, `Fragment` layouts, adapters, or XML resources.
   - Use Compose when the surrounding project already uses Compose or the user explicitly asks for Compose.
   - If the target is unspecified and there is no project context, prefer Compose for new isolated screens and state that assumption.
3. Reconstruct hierarchy first.
   - Build the container structure before styling details.
   - Convert the image into a small number of meaningful layout groups rather than pixel-by-pixel wrappers.
4. Translate visual details into Android primitives.
   - Read [image-analysis-guidelines.md](./references/image-analysis-guidelines.md) for mapping rules.
   - Use drawables, shapes, text appearances, color resources, and dimensions in XML when the UI depends on reusable styling.
   - Use `Modifier`, `TextStyle`, `Shape`, `Brush`, and helper composables in Compose when the UI is Compose-based.
5. Handle uncertainty explicitly.
   - If the image does not expose exact values, infer a reasonable Android implementation and say which values were estimated.
   - If icons, fonts, or assets are missing, keep placeholders or resource references instead of inventing binaries.
6. Return complete Android output.
   - For XML, include the layout and any required drawable or resource snippets.
   - For Compose, include the composable and supporting styles or helper code needed to compile.
7. Validate fidelity.
   - Compare hierarchy, spacing rhythm, text emphasis, corner radius, shadows, and visible states against the image.

## Implementation Rules

- Preserve the visible grouping from the image.
- Prefer `ConstraintLayout` or Compose `Box`/`ConstraintLayout` for overlapping or tightly aligned layouts.
- Prefer `LinearLayout` or Compose `Row`/`Column` for simple stacked sections.
- Use `dp` for layout size, `sp` for text, and estimate values from visual proportions when exact specs are not available.
- Keep XML resource names in `snake_case`.
- Use Korean explanations by default unless the user asks for another language.
- Keep comments short and only explain non-obvious approximations.

## Output Expectations

- Emit code that is directly usable, not only a prose description.
- Include supporting resources when the visual result depends on them.
- Mention which parts were estimated from the image.
- Do not claim interactive behavior that the image does not show unless it is an obvious control pattern such as a back button or text input.

## Reference

- Read [image-analysis-guidelines.md](./references/image-analysis-guidelines.md) whenever the task starts from a screenshot, mockup, or image-only visual reference.
