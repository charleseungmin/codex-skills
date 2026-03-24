---
name: exofit-components-dev
description: Develop and modify the Exofit React components library in a way that matches its current architecture, public API shape, WebView bridge patterns, and TypeScript/React coding conventions. Use when Codex is working in this repository on chart components, wrappers, webview pages, hooks, routes, exports, Plotly configuration, postMessage handling, or related refactors that must stay consistent with the existing project structure.
---

# Exofit Components Dev

Follow the repository's existing architecture instead of introducing a new pattern. Keep changes aligned with the current React 19 + TypeScript + Vite library structure, especially the split between reusable components, route-level webview pages, hooks, wrappers, and bridge utilities.

Read [references/project-conventions.md](references/project-conventions.md) before making structural decisions, adding a new module, or changing exports.

## Workflow

1. Classify the task by layer before editing.
   - Use `src/components` for reusable rendering units.
   - Use `src/webviews` for route-level pages that receive or simulate message-driven data.
   - Use `src/wrappers` for public adapters that compose hooks and components for consumers.
   - Use `src/hooks` for stateful message, resize, or data acquisition logic.
   - Use `src/utils` for pure helpers, config, parsing, performance, or bridge code.
   - Use `src/routes/routes.ts` for route registration and lazy loading.
   - Use `src/index.ts` and local `index.ts` files for public exports.

2. Extend the smallest existing abstraction that fits.
   - Prefer reusing `GraphContainer`, `PlotGraph`, existing hooks, and Plotly config helpers before adding new abstractions.
   - Keep message parsing and bridge behavior in hooks or utils, not inside route components unless the pattern already exists there.

3. Preserve the repository's API style.
   - Use TypeScript types and interfaces in `src/components/types.ts` when the type is shared across modules.
   - Favor named exports and keep the local default export only when the file already follows that pattern.
   - When adding a public feature, update the relevant barrel file and `src/index.ts`.

4. Match the implementation style already used in the surrounding files.
   - Keep JSDoc-style block comments and concise Korean descriptions where the repo already uses them.
   - Keep style objects typed with `React.CSSProperties` and colocated in the file when extending the current inline-style approach.
   - Keep empty or error behavior quiet for WebView-facing surfaces unless the task explicitly asks for visible UX changes.

5. Validate with repository commands after edits.
   - Run `yarn build` for broad TypeScript and bundling validation.
   - Run `yarn lint` when the change touches formatting, hooks, or event handling patterns that lint rules may catch.
   - If a route, export, or bridge contract changes, verify all linked files were updated consistently.

## Common Tasks

### Add or change a chart/webview page

Update the route component in `src/webviews`, keep message handling near the page through `useMessage` or a dedicated hook, and register the page in `src/routes/routes.ts` with `React.lazy(...)`. If the page is public or reusable, export the right pieces from the nearest barrel file and `src/index.ts`.

### Add or change reusable graph behavior

Start in `src/components`, `src/hooks`, or `src/utils` instead of duplicating logic in a route component. Keep Plotly defaults merged through `mergeLayout` and `mergeConfig` rather than replacing defaults wholesale.

### Change WebView bridge behavior

Inspect `src/utils/postMessageHandler.ts`, `src/utils/webViewBridge.ts`, and the consuming hooks before editing. Keep origin checks, graceful fallbacks for browser development, and native bridge compatibility intact.

## Output Expectations

When completing work with this skill:

- Keep the final code path consistent with the existing folder responsibilities.
- Keep exports synchronized so library consumers and route loading do not drift.
- Call out any contract changes that native clients or library consumers must know about.
- Mention which validation commands ran and which were not run.
