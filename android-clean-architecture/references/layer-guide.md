# Android Clean Architecture Layer Guide

## Layer Responsibilities

### Presentation
- Own `Activity`, `Fragment`, `Composable`, `Adapter`, `ViewModel`, UI state, and UI event classes.
- Convert domain output into display-ready text or visual state.
- Trigger navigation and one-off effects through the project's existing effect pattern.
- Depend on domain abstractions, never on remote APIs, DAOs, or repository implementations.

### Domain
- Own domain models, use cases, repository interfaces, and pure business policies.
- Stay independent from Android framework types and transport or persistence details.
- Keep use cases narrow. One use case should express one business action or query.

### Data
- Own Retrofit services, Room DAOs, local or remote data sources, DTOs, entities, mappers, and repository implementations.
- Translate infrastructure concerns into domain-facing contracts.
- Hide pagination keys, headers, HTTP codes, SQL schema details, and cache decisions from upper layers.

## Dependency Direction

- Allow `presentation -> domain`.
- Allow `data -> domain`.
- Forbid `domain -> presentation`.
- Forbid `domain -> data`.
- Forbid `presentation -> data` unless the repository already uses a pragmatic shortcut and the user asks to preserve it.

## Model Placement Rules

- Put API response DTOs in data.
- Put Room entities in data.
- Put screen-only items such as tab labels, selection state, and formatted text in presentation.
- Put shared business concepts such as `UserProfile`, `WorkoutPlan`, or `AuthSession` in domain when they are not tied to transport or storage shape.
- Keep mapper names explicit, such as `toDomain()`, `toEntity()`, or `toUiModel()`.

## Flow Template

1. UI sends intent or event to `ViewModel`.
2. `ViewModel` calls a use case.
3. Use case calls a repository interface from domain.
4. Repository implementation coordinates local or remote data sources.
5. Data layer maps raw models into domain models.
6. `ViewModel` reduces domain results into UI state.
7. UI renders state and emits the next event.

## Review Checklist

- Can the use case run in a plain JVM test without Android dependencies?
- Does any UI class contain validation, calculation, or mapping that belongs in a use case or mapper?
- Does any repository implementation return raw Retrofit or Room models to upper layers?
- Is loading, error, and empty handling represented in UI state?
- Are side effects such as navigation, toasts, and analytics kept out of domain?
- Does the change follow the project's existing folder and naming conventions?
