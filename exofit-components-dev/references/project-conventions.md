# Exofit Components Library Conventions

## Architecture Map

- `src/components`: Reusable rendering units and shared UI primitives such as `PlotGraph`, `GraphContainer`, `TrajectoryChart`, `OrbitalScene`.
- `src/webviews`: Route-level pages intended for WebView or demo usage. These often own message wiring and sample-data bootstrapping.
- `src/wrappers`: Public adapters for consumers. `WebViewWrapper` handles native message-driven rendering. `WebWrapper` handles direct prop-driven web rendering.
- `src/hooks`: Stateful logic for message subscription, resize observation, and specialized data ingestion.
- `src/utils`: Pure helpers and environment logic such as Plotly config merging, payload parsing, postMessage bridging, and performance helpers.
- `src/routes/routes.ts`: Single source of truth for lazy-loaded page routes.
- `src/index.ts`: Public package surface. Update this when a new public component, hook, utility, or type becomes part of the library API.

## File Placement Rules

- Add shared types to `src/components/types.ts` when more than one module consumes them.
- Keep route-local types inside the route file when they are specific to one page.
- Put message parsing that can be reused into hooks or utils instead of leaving it embedded in components.
- Keep wrapped route behavior centralized. `App.tsx` handles `/wrapped/*`, so do not duplicate wrapped routes in `routes.ts`.

## React and TypeScript Style

- Use `React.FC<...>` consistently for components in this repo.
- Use named exports for the main symbol and retain `export default` at the end when the surrounding file already does both.
- Use `memo`, `useMemo`, `useCallback`, and `useEffect` in the same pragmatic style as adjacent files. Do not introduce optimization helpers where the repo does not use them.
- Type style objects as `React.CSSProperties`.
- Favor explicit interfaces and type aliases over inferred complex object shapes when data crosses module boundaries.

## UI and UX Patterns

- Keep WebView-facing containers full-size, transparent where appropriate, and mobile-friendly.
- Prefer quiet empty/error states for graph surfaces. Existing components often render blank states instead of prominent inline errors.
- Keep style constants below the component when following the current inline-style pattern.
- Avoid introducing CSS modules, styled-components, or a new theming system unless the task explicitly requires a broader refactor.

## Routing and Loading Patterns

- Lazy-load route components with `React.lazy(() => import(...).then(...))` when exporting a named component.
- Wrap route rendering with `Suspense` and `LoadingFallback`.
- Root `/` and `*` currently resolve to empty pages. Preserve that behavior unless the task explicitly changes routing UX.

## WebView and Bridge Rules

- Preserve compatibility with React Native WebView, iOS `window.webkit.messageHandlers.native`, Android `window.Android.postMessage`, and browser fallback behavior.
- Keep origin validation through `isAllowedOrigin`.
- Use `sendReady`, `sendError`, `sendEvent`, or `sendWebViewMessage` instead of open-coded bridge dispatch when possible.
- When changing message contracts, inspect all senders and receivers. Message shape drift is easy to introduce in this repo.

## Plotly Rules

- Merge into `defaultLayout` and `defaultConfig` with `mergeLayout` and `mergeConfig`.
- Keep WebView/mobile defaults intact unless there is a concrete reason to change them.
- Prefer extending shared Plotly helpers over inlining repeated layout/config fragments across pages.

## Documentation and Comments

- Keep the repo's JSDoc-style block comments.
- Write concise Korean descriptions to match the existing codebase tone.
- Add examples only when the surrounding file already uses them or when the public API benefits from them.

## Change Checklist

- Did the change land in the correct layer?
- Did shared types move into `src/components/types.ts` when needed?
- Did route additions update `src/routes/routes.ts`?
- Did public API changes update `src/index.ts` and any local barrel files?
- Did bridge or message changes update both sender and receiver paths?
- Did validation run with at least `yarn build` for non-trivial changes?
