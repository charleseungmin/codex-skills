# exoFit Repo Rules

## Primary Docs to Read
- `C:/Users/lenovo/StudioProjects/exoFit/AGENTS.md`
- `C:/Users/lenovo/StudioProjects/exoFit/docs/architecture.md`
- `C:/Users/lenovo/StudioProjects/exoFit/docs/app-development.md`
- `C:/Users/lenovo/StudioProjects/exoFit/docs/important-checklist.md`

## Module and Package Structure
- Main app module: `app/`
- Shared library module: `exoLib/`
- UI packages live under `app/src/main/java/com/exosystems/fit/view`
- ViewModels live under `app/src/main/java/com/exosystems/fit/viewmodel`
- Use cases live under `app/src/main/java/com/exosystems/fit/domain/usecase`
- Repository interfaces live under `app/src/main/java/com/exosystems/fit/domain/repository`
- Repository implementations and data sources live under `app/src/main/java/com/exosystems/fit/data`

## Implementation Pattern Seen in Current Code
- Fragment screens often use:
  - `@AndroidEntryPoint`
  - XML layout + ViewBinding delegate
  - `navGraphViewModels(...)`
  - `initializeView()`
  - `setupListeners()`
  - `setupObservers()`
  - `renderState(...)`
- UI input watchers update ViewModel state directly.
- Business validation and transformation live in UseCase or ViewModel, not in Fragment.
- Navigation uses the Navigation component and helper methods such as `navigateSafe` and `popBackStackSafe`.

## XML Layout Conventions
- Resource names use `snake_case`.
- IDs are prefixed by view type such as `tv_`, `iv_`, `cv_`, `et_`, `tl_`, `layout_`.
- Repeated sections are commonly split into `include` layouts.
- Material components and existing style resources are reused instead of redefining styles inline everywhere.

## Architecture Boundaries
- Keep Android framework types out of domain code.
- Do not call repositories or remote APIs directly from Fragment or Activity.
- Use ViewModel state as the source-of-truth for UI rendering.
- Put complex measurement or calculation logic into UseCase, manager, or data layers.

## Scope and Process Rules
- One feature per PR.
- Avoid unrelated refactors.
- Update `docs/architecture.md` if module responsibilities, dependency direction, or flow structure changes.
- Follow the Gradle commands from `AGENTS.md` for build, unit test, and lint.

## Quality Reminders
- Regression risk is high around BLE, auth, session, and measurement flows.
- Validate disconnect, reconnect, timeout, and lifecycle-sensitive behavior when touching measurement code.
- For UI changes, keep visual language consistent with existing screens rather than introducing a new design system.
