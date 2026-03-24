---
name: code-flowchart-mermaid
description: Analyze code and draw Mermaid flowcharts for fragments, screen flows, navigation paths, lifecycle behavior, and core business logic branches. Use when Codex receives Android Kotlin or Java code, asks to explain a fragment flow, wants a navigation or state transition diagram, or needs a Mermaid flowchart summarizing key logic from source files.
---

# Code Flowchart Mermaid

## Overview

Read the relevant code, reconstruct the actual control flow, and output Mermaid flowcharts that explain screen behavior or core logic without inventing missing steps. Default to Korean labels unless the user explicitly asks for another language.

## Workflow

1. Determine the diagram scope first.
   - `Fragment flow`: lifecycle entry, UI initialization, listeners, observers, navigation, dialogs.
   - `Flow`: end-to-end screen movement across fragments, dialogs, activities, or bottom sheets.
   - `Core logic`: validation, branching, state mutation, repository/use case decisions.
2. Read only the files needed to explain the flow.
   - Start from the requested file.
   - Follow references to layout, ViewModel, UseCase, navigation targets, dialogs, or helper methods only when they change the visible flow.
3. Reconstruct the real decision points.
   - Identify entry points such as `onViewCreated`, click listeners, observer callbacks, and public methods.
   - Separate straight-line setup from conditional branches.
   - Distinguish UI actions, state changes, and navigation outcomes.
4. Choose the right diagram granularity.
   - Use one compact diagram when the flow is small.
   - Split into multiple Mermaid blocks when a single diagram would become noisy.
   - Prefer separate diagrams for `화면 초기화`, `주요 버튼 플로우`, `핵심 분기 로직` on larger screens.
5. Write Mermaid that mirrors the code.
   - Use `flowchart LR` by default.
   - Use quoted node labels.
   - Keep labels short and user-readable.
   - Preserve important branch conditions such as validation success or failure, device connected or not, and selected or not selected.
6. Add brief assumptions only when needed.
   - If a helper method or external class is not inspected, say that the node is summarized from the call site.
   - Do not fabricate API or navigation behavior that the code does not show.

## Diagram Rules

- Prefer `flowchart LR` unless vertical flow is materially clearer.
- Use node categories consistently: start, action, decision, state update, navigation, dialog.
- Keep one concept per node.
- Put branch text on edges, not buried in long node labels.
- Use Korean text in node labels by default.
- Keep code identifiers such as `MuscleActivationEvalSetFragment` or `canComplete()` as-is when they help anchor the diagram.
- When one method fans out into many listeners, make the setup node fan out rather than flattening everything into one line.

## Output Expectations

- Output Mermaid code blocks that can be pasted directly into Markdown.
- Add a one-line title above each diagram when there are multiple diagrams.
- If the flow is partial, state which files were used.
- Optimize for explainability over full call-graph coverage.
- Do not dump every helper call into the diagram; include only steps that affect UI, navigation, validation, or major state transitions.

## Reference

- Read [mermaid-guidelines.md](./references/mermaid-guidelines.md) for syntax rules, diagram patterns, and Android-specific flowchart examples before drawing a non-trivial flow.
