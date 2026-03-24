---
name: exofit-android-conventions
description: Apply the exoFit repository's Android coding conventions, layout rules, architecture boundaries, and delivery process when making changes in this project. Use when Codex is asked to implement, refactor, review, or extend code inside the exoFit repo and must match its existing package structure, Fragment/ViewModel patterns, XML layout style, domain layering, build commands, and docs expectations.
---

# exoFit Android Conventions

## Overview

Follow the real patterns already used in the exoFit codebase instead of applying generic Android style. Start from repository docs, then mirror the closest nearby implementation for file placement, naming, UI structure, and dependency direction.

## Workflow

1. Read the repository rules first.
   - Read `AGENTS.md`.
   - Read `docs/architecture.md`, `docs/app-development.md`, and `docs/important-checklist.md`.
   - Use [repo-rules.md](./references/repo-rules.md) as the compact summary and entry point.
2. Find the closest existing example before editing.
   - Match by feature area such as `view/measure`, `view/report`, `view/profile`, or `view/setting`.
   - Reuse the surrounding package and class structure instead of introducing a new pattern.
3. Keep the layer boundary intact.
   - UI stays in `view/`.
   - Screen state and event handling stay in `viewmodel/`.
   - Business rules go to `domain/usecase/`.
   - Repository contracts stay in `domain/repository/`, implementations in `data/repository/`.
   - Do not move Android framework types into the domain layer.
4. Match the local UI implementation style.
   - For View-based screens, prefer Fragment + XML + ViewBinding patterns already used in the module.
   - Use listener setup, observer setup, and render methods in the same style as nearby fragments.
   - Keep navigation through existing Navigation component patterns and Safe Args where applicable.
5. Keep scope tight.
   - Implement only the requested feature or fix.
   - Do not introduce opportunistic refactors, migrations, or architectural detours.
6. Update docs only when the structure or flow actually changes.
   - If architecture, dependency flow, or module responsibility changes, update `docs/architecture.md`.
7. Validate with the repo's commands.
   - Use the Gradle commands defined in `AGENTS.md` for assemble, unit tests, and lint.

## Coding Rules

- Languages are Kotlin-first, with some Java and C/C++.
- Use 4-space indentation and Android Studio formatting.
- Keep package names lowercase under `com.exosystems.fit` and `com.exosystems.exoLib`.
- Use `PascalCase` for classes, `camelCase` for methods and fields, `UPPER_SNAKE_CASE` for constants.
- Use `snake_case` for Android resource names.
- Prefer existing extension functions and helpers from `exoLib` when the codebase already relies on them.
- Do not call network or repository code directly from UI classes.
- Keep business calculations out of Fragment and Activity classes.

## Layout Rules

- Match the existing layout system already used by the target screen. In this repo that is usually XML layouts for existing Fragment screens.
- Keep layout files under `app/src/main/res/layout` with descriptive `snake_case` names.
- Reuse common styles, colors, and drawables before adding new ones.
- Keep IDs descriptive and aligned with existing naming patterns such as `tv_*`, `iv_*`, `cv_*`, `layout_*`, `et_*`.
- For complex screens, split repeated sections into included layouts instead of duplicating XML.

## Architecture Rules

- Follow `UI -> ViewModel -> UseCase -> Repository -> DataSource`.
- Prefer `navGraphViewModels` and shared ViewModel state where the surrounding flow already uses it.
- Use `StateFlow` or `LiveData` consistently with the local module rather than mixing patterns arbitrarily.
- Keep source-of-truth in ViewModel state for rendered UI values.
- Put shared or reusable logic in `exoLib` only when it is truly cross-feature and matches existing shared responsibilities.

## Delivery Rules

- Keep one logical change per PR.
- Follow the repo's Korean commit message style if a commit is requested.
- For UI changes, be ready to provide screenshots or recordings and the executed verification commands.
- Do not create new secrets or environment-specific values.

## Reference

- Read [repo-rules.md](./references/repo-rules.md) before implementing anything non-trivial in this repository.
