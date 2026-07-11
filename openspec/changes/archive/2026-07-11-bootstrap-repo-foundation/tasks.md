# Tasks: Bootstrap repository foundation

## Review Workload Forecast

| Field | Value |
| ------- | ------- |
| Estimated changed lines | 250–400 lines across 3 Markdown files |
| 400-line budget risk | Medium |
| Chained PRs recommended | No |
| Suggested split | Single PR: architecture and decisions → README → documentation review |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Medium

## Scope

Documentation only: `README.md`, `docs/architecture.md`, and `docs/decisions.md`. Do not add installers, package/configuration files, module or profile directories, managed dotfiles, CLI code, a `doctor` command, or test-runner configuration.

## Implementation checklist

### 1. Document the intended architecture

- [x] **Files:** Create `docs/architecture.md`.
- [x] State at the top that the document describes planned boundaries, not implemented modules.
- [x] Explain the modular-monolith choice and use “Current”, “Planned”, and “Future” consistently.
- [x] Define non-overlapping intended ownership for `core`, `shell`, `terminal`, `multiplexer`, `monitoring`, `git`, `devtools`, and `profiles`.
- [x] Record composition and dependency rules: profiles compose contexts, `core` is foundational, feature contexts do not depend on profiles, and each configuration item has one owner.
- [x] Explain Fedora-first sequencing, future Windows/WSL and macOS scope, and `chezmoi` as intended future direction rather than configured capability.
- [x] Include an **Illustrative future layout** showing planned areas without creating empty directories or implying they exist.
- [x] Keep low-level interfaces and premature DDD mechanisms out of the document.
- [x] **Finish when:** a reader can identify every planned boundary, its ownership, and what is explicitly not implemented.
- [x] **Verify:** inspect headings, module table, dependency rules, status labels, and layout wording against `specs/repository-foundation/spec.md`.
- [x] **Rollback:** revert only `docs/architecture.md` if the architecture needs revision; no runtime or workstation state is affected.

### 2. Record foundational decisions and tradeoffs

- [x] **Files:** Create `docs/decisions.md`.
- [x] Add concise decision records with status, decision, rationale, alternatives, consequences, and reconsideration triggers.
- [x] Cover documentation-first delivery, Fedora-first sequencing, modular-monolith boundaries, intended `chezmoi` direction, public-repository secret safety, and a practical-but-polished product tone.
- [x] State that credentials, private host details, employer information, and machine-specific secrets must not be committed; keep examples generic.
- [x] Explicitly defer installers, tool configuration, cross-platform implementation, CLI/`doctor` work, and test-runner selection.
- [x] Link to `docs/architecture.md` where it reduces duplication rather than repeating the module model.
- [x] **Finish when:** contributors can understand the tradeoffs behind the documentation-only milestone and know when each decision should be revisited.
- [x] **Verify:** manually compare all six decision records and their consequences with the design and specification.
- [x] **Rollback:** remove or revert `docs/decisions.md`; no executable behavior is affected.

### 3. Build the README entry point after detail pages exist

- [x] **Files:** Update `README.md` only; preserve the documentation-only scope.
- [x] Lead with the project purpose and learning-oriented goal.
- [x] Clearly label the current repository status as documentation foundation only, with no supported installer or working dotfiles yet.
- [x] Identify Fedora Linux as the first implementation target; label Windows/WSL and macOS as future scope.
- [x] Summarize the planned Fedora tool ecosystem as roadmap context, never as installed or configured capability.
- [x] Add repository-relative links to `docs/architecture.md` and `docs/decisions.md`, with accurate one-line descriptions.
- [x] Include a short roadmap naming the separate Fedora installer milestone as next, without adding installer instructions.
- [x] Include public-repository safety and contribution expectations; omit installation commands, package commands, unsupported badges, and misleading screenshots.
- [x] **Finish when:** a new reader can determine purpose, status, direction, documentation map, and next milestone without private context.
- [x] **Verify:** confirm both links resolve to the documents created in tasks 1–2 and check all planned/current/future wording.
- [x] **Rollback:** restore the prior `README.md`; the detail documents can remain only if the change is intentionally revised as a complete documentation set.

### 4. Perform final documentation inspection

- [x] **Targets:** `README.md`, `docs/architecture.md`, `docs/decisions.md`, and the repository tree.
- [x] Confirm the diff contains only the three repository-facing Markdown files.
- [x] Confirm all eight architecture contexts are named and responsibilities do not overlap materially.
- [x] Confirm the README links resolve and no link targets an absent future file or directory.
- [x] Confirm planned tools/platforms/`chezmoi` are not described as delivered behavior.
- [x] Confirm no installer, package, shell/tool configuration, profile/module scaffolding, manifest, CLI, or test runner was added.
- [x] Review English, headings, tables, progressive disclosure, and concise scanability.
- [x] Review for credentials, tokens, private hostnames, employer identifiers, personal paths, and machine-specific data.
- [x] Confirm the total documentation diff remains within the 500-line review budget.
- [x] **Finish when:** all specification scenarios are supported by readable repository content and the scope guardrail passes.
- [x] **Verification method:** Markdown review and repository inspection only; no test runner is selected for this documentation-only change.
- [x] **Rollback:** revert the complete documentation diff as one atomic change.
