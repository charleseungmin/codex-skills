---
name: project-convention-adapter
description: Inspect the current repository to identify its real technology stack, build tools, architecture, coding conventions, and validation commands, then implement changes in that local style instead of using generic defaults. Use when Codex starts work in an unfamiliar project on any platform or language and must first infer repo-specific patterns from files such as AGENTS.md, README, package manifests, build configs, lint or formatter configs, CI workflows, and nearby source files.
---

# Project Convention Adapter

## Overview

Adapt to the repository that is actually in front of you. Detect the stack, rules, and architecture from project files and nearby code, then make the smallest change that matches those established patterns.

## Workflow

1. Establish the repo context before proposing code.
   - Read `AGENTS.md` first when present.
   - Read the top-level `README` and the nearest feature or module docs that affect the task.
   - Check git status before editing so you do not overwrite unrelated user changes.
2. Detect the stack from project manifests and tool configs.
   - JavaScript or TypeScript: inspect `package.json`, lockfiles, `tsconfig*`, bundler configs, ESLint, Prettier, Vitest, Jest, Playwright, Storybook.
   - Python: inspect `pyproject.toml`, `requirements*.txt`, `poetry.lock`, `ruff.toml`, `mypy.ini`, `pytest.ini`.
   - JVM or Android: inspect `settings.gradle*`, `build.gradle*`, `gradle.properties`, `libs.versions.toml`, `AndroidManifest.xml`.
   - Rust: inspect `Cargo.toml`, `Cargo.lock`, `rustfmt.toml`, `clippy.toml`.
   - Go: inspect `go.mod`, `go.sum`, lint configs, task or mage files.
   - Ruby, PHP, Swift, .NET, C or C++, and mixed repos: inspect the equivalent manifest, formatter, test, and build files before assuming conventions.
3. Find the local pattern closest to the requested change.
   - Search for nearby files in the same feature, layer, package, route, module, or platform target.
   - Prefer copying structure from the closest working example instead of inventing a new abstraction.
   - Match file placement, naming, imports, state management style, error handling, tests, and comments to surrounding code.
4. Infer architectural boundaries before editing.
   - Identify where UI, domain logic, infrastructure, data access, and utilities live in this repository.
   - Keep new code in the existing layer; do not collapse boundaries for convenience.
   - If the repo mixes old and new patterns, follow the one used by the files you are touching unless the task explicitly asks for migration.
5. Implement conservatively.
   - Reuse existing helpers, shared types, wrappers, hooks, services, or utilities before adding new ones.
   - Keep the public API shape, naming style, and dependency direction consistent.
   - Do not introduce new frameworks, linters, formatters, or folder structures unless the task requires it.
6. Validate with the repo's own commands.
   - Use the smallest command that gives meaningful confidence: targeted tests first, then broader build or lint if needed.
   - Prefer commands already defined in scripts, task runners, Makefiles, Gradle, npm scripts, tox, or CI workflows.
   - If validation cannot run, state exactly what blocked it.

## Detection Priorities

When time is limited, inspect sources in this order:

1. Repository instructions: `AGENTS.md`, contribution docs, architecture docs.
2. Build and dependency manifests: package managers, workspace files, module definitions.
3. Quality gates: lint, formatter, type-check, test, CI configuration.
4. The exact files adjacent to the requested change.
5. Shared abstractions and barrel exports affected by the change.

## Implementation Rules

- Prefer `rg` and `rg --files` for codebase discovery when available.
- Read only enough files to establish confidence; do not bulk-read the whole repository.
- Mirror the existing naming conventions exactly:
  - file names
  - class, function, and variable casing
  - test file placement and naming
  - resource or asset naming rules
- Match the local formatting style even when it differs from your default preference.
- Preserve existing dependency injection, routing, module registration, and export patterns.
- If you encounter multiple valid conventions in one repo, say which one you are following and why.
- Treat generated files, migrations, snapshots, and lockfiles according to existing repo practice; do not regenerate them unless the change requires it.

## What to Inspect by Category

### Frontend or web app

- Framework entrypoints, routing, component folders, styling approach, design tokens, state libraries, test setup, story files, build scripts.

### Backend or service

- Application entrypoints, dependency injection setup, HTTP framework, schema or validation libraries, database layer, background job conventions, observability patterns.

### Mobile

- Platform module boundaries, navigation patterns, UI technology, resource naming, ViewModel or controller conventions, build variants, dependency management.

### Library or SDK

- Public export surface, semantic versioning signals, backward compatibility constraints, wrapper patterns, generated artifacts, sample apps, contract tests.

### Monorepo

- Workspace root, package boundaries, shared config packages, code ownership hints, per-package scripts, affected-package test strategy.

## Output Expectations

- State the stack and conventions you inferred when they materially affect the implementation.
- Mention the key files you used to infer those rules.
- Call out any assumption when the repo is ambiguous.
- Report the validation commands you ran and any that you could not run.

## Avoid

- Do not impose a favorite architecture when the repo already has one.
- Do not rewrite unrelated files to make the codebase feel cleaner.
- Do not rely on generic framework best practices when local code contradicts them.
- Do not skip validation when the repository clearly exposes a standard command for it.
