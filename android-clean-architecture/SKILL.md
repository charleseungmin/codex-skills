---
name: android-clean-architecture
description: Write or refactor Android code with clean architecture and modern Kotlin patterns. Use when Codex must implement features, fix bugs, review structure, or generate boilerplate for Android apps that separate presentation, domain, and data layers through ViewModel/UI state, use cases, repository contracts, DTO or entity mapping, coroutines or Flow, dependency injection, and testable boundaries.
---

# Android Clean Architecture

## Overview

Implement Android features with explicit layer boundaries instead of mixing UI, business rules, and data access. Match the existing project conventions first, then keep presentation, domain, and data responsibilities isolated so the code stays testable and replaceable.

## Workflow

1. Inspect the project before writing code.
   - Detect whether the app uses Compose or Views, Hilt or another DI framework, Room, Retrofit, GraphQL, paging, and its existing result wrapper pattern.
   - Mirror the local package layout, naming, and state-management style instead of introducing a new architecture flavor.
2. Model the feature as a dependency flow.
   - Start from the user action or screen load.
   - Trace `UI -> ViewModel -> UseCase -> Repository -> DataSource`.
   - Decide which data must be mapped into a domain model before it reaches the presentation layer.
3. Place each class in the correct layer.
   - Presentation owns screens, UI state, UI events, navigation triggers, and view-specific formatting.
   - Domain owns business rules, use cases, domain models, and repository interfaces.
   - Data owns API or database models, mappers, data sources, and repository implementations.
4. Implement from the center outward.
   - Define or update domain models and repository contracts first.
   - Add data models, data-source calls, mappers, and repository implementations next.
   - Add ViewModel orchestration and UI rendering last.
5. Keep async and error handling explicit.
   - Use `suspend` or `Flow` at repository and use-case boundaries when the surrounding project already uses them.
   - Convert infrastructure failures into the project's result or error model before the UI consumes them.
   - Keep loading, empty, success, and failure states visible in presentation state.
6. Validate architecture, not only compilation.
   - Check that domain code has no Android framework dependency.
   - Check that UI code does not call Retrofit, Room, DAO, or repository implementations directly.
   - Check that DTOs and database entities do not leak into UI state unless the repo already standardizes on shared models.

## Implementation Rules

- Prefer immutable UI state and unidirectional data flow.
- Keep `ViewModel` focused on orchestration and state reduction, not heavy business logic.
- Put reusable business rules in use cases instead of fragments, activities, composables, or repository implementations.
- Keep repository interfaces in domain and concrete implementations in data.
- Map transport or storage models into domain models when the boundaries are meaningful.
- Do not pass Android `Context`, `Bundle`, `NavController`, `Response`, Room entities, or Retrofit DTOs into the domain layer.
- Prefer small mapper functions over ad hoc field conversion spread across the codebase.
- Reuse the project's existing dispatcher, error wrapper, and logging pattern before adding new abstractions.
- If the project has no established pattern, prefer Kotlin, coroutines, `StateFlow`, constructor injection, and narrow use cases with one clear responsibility.

## Output Expectations

- Return code that is wired end to end for the requested change, not isolated fragments that ignore the rest of the flow.
- State any architectural assumption that could affect file placement, model ownership, or async behavior.
- Keep comments short and only explain non-obvious mapping or boundary decisions.
- Add or update tests when the repository already has unit-test coverage around use cases, repositories, or ViewModels.

## Reference

- Read [layer-guide.md](./references/layer-guide.md) when deciding where a class belongs, how to shape models across layers, or what dependencies are forbidden.
