# Design: Make the repository foundation understandable before it is executable

## Outcome

This change will establish three English-language documentation entry points: `README.md`, `docs/architecture.md`, and `docs/decisions.md`. Together they will explain what `jjdlr-dots` is, what exists today, how the planned modular monolith is divided into lightweight ownership contexts, and why implementation is intentionally deferred.

The change remains documentation-only. It will not create installers, package manifests, managed dotfiles, module directories, profile directories, configuration files, test infrastructure, or any other executable behavior.

## Design drivers

| Driver | Design response |
| --- | --- |
| A new reader needs the truth quickly | Lead the README with purpose, current status, Fedora-first direction, and the next milestone. |
| Planned capability must not look delivered | Use consistent **Current**, **Planned**, and **Future** labels in all three documents. |
| The project is intended to remain modular | Define module ownership and dependency direction before configuration is added. |
| The project is educational | Record rationale, alternatives, and consequences rather than only conclusions. |
| The repository is public | Make secret safety a documented architectural and contribution constraint. |
| The first review is small | Use one entry point and two focused detail documents, with tables and links instead of repeated prose. |

## Current-state finding

Direct inspection found that `README.md` exists and is empty. `docs/architecture.md` and `docs/decisions.md` do not exist, so they will be new documents rather than edits to existing files. No implementation or automated test runner exists.

## Documentation architecture

The documents form a progressive-disclosure path:

```text
README.md
  |-- project status, purpose, planned toolset, roadmap
  |-- docs/architecture.md
  |     `-- planned boundaries, dependency rules, platform strategy, layout
  `-- docs/decisions.md
        `-- decisions, alternatives, tradeoffs, consequences
```

The README answers “What is this and where is it going?” Architecture answers “How will responsibilities be kept separate?” Decisions answers “Why were these constraints chosen?” Each fact has one primary owner; links replace unnecessary duplication.

### Content ownership contract

| Information | Primary owner | Other documents |
| --- | --- | --- |
| Current repository status and next milestone | `README.md` | Summarize only when needed to prevent overclaiming. |
| Module/context responsibilities and dependency rules | `docs/architecture.md` | Link from README and relevant decisions. |
| Decision rationale, alternatives, and consequences | `docs/decisions.md` | Architecture states the resulting rule and links to rationale. |
| Detailed illustrative repository tree | `docs/architecture.md` | README provides only a short document map. |
| Planned tool ecosystem | `README.md` | Architecture discusses tools only where they affect direction. |

## File designs

### `README.md`: reader entry point

The README will use the following scan order:

1. Project purpose and learning goal.
2. A prominent current-status statement: documentation foundation only; no supported installer or working dotfiles yet.
3. Fedora as the first implementation target, with Windows/WSL and macOS labeled future scope.
4. Planned tool ecosystem, grouped by role and explicitly marked as roadmap context.
5. Documentation links to architecture and decisions, with one-line descriptions.
6. A short roadmap that identifies the separate Fedora installer milestone as next without promising its design.
7. Public-repository safety and contribution expectations.

The README will not include installation commands, package commands, shell snippets, badges that imply build/support maturity, or screenshots of functionality that does not exist.

### `docs/architecture.md`: planned ownership model

The architecture document will begin with a status note stating that it describes intended boundaries, not implemented modules. It will then cover:

- architectural drivers and the modular-monolith choice;
- lightweight bounded contexts and their ownership;
- profile composition and dependency direction;
- Fedora-first platform sequencing;
- the planned role of `chezmoi`;
- an illustrative future repository layout;
- explicit deferred behavior and evolution rules.

#### Lightweight bounded contexts

The term **bounded context** is used only as a documentation and ownership aid. Each context owns one coherent type of configuration and its related future automation. This prevents unrelated settings from accumulating in shared scripts.

This is deliberately not formal domain-driven design. This milestone introduces no aggregates, domain events, service interfaces, or framework abstractions. Executable contracts should be introduced only when a later implementation demonstrates a need.

| Context | Planned ownership | Must not own |
| --- | --- | --- |
| `core` | OS detection, common prerequisites, and base packages shared by the workstation setup | Tool-specific presentation or profile policy |
| `profiles` | Composition of modules for a platform or usage context, initially Fedora | Module internals or duplicated tool configuration |
| `shell` | zsh, prompt integration, aliases, functions, exports, and `PATH` policy | Terminal emulator or multiplexer configuration |
| `terminal` | Terminal-emulator configuration, initially Kitty | Shell behavior or workspace/session orchestration |
| `multiplexer` | Zellij configuration and layouts; possible later tmux support | Terminal-emulator settings or system monitoring config |
| `monitoring` | btop, fastfetch, and related visual system-inspection configuration | Base package policy or development runtimes |
| `git` | Git behavior, aliases, and lazygit configuration | General shell aliases or unrelated development tools |
| `devtools` | mise, language/runtime tooling, and development helpers | Core OS setup or Git-specific configuration |

#### Dependency and composition rules

The architecture document will make these rules explicit:

1. `profiles` select and compose contexts; they do not absorb or duplicate context responsibilities.
2. `core` is the shared foundation and must not depend on feature contexts or profiles.
3. Feature contexts may rely on capabilities established by `core`, but must not depend on a profile.
4. A configuration item has one owning context. Another context references that capability instead of maintaining a second copy.
5. Direct feature-context dependencies should be avoided. If coordination becomes necessary, it must be documented with ownership and direction before executable coupling is added.
6. Platform selection belongs in profiles; context-specific configuration remains with its owning context.
7. Cross-platform abstractions are added only after another platform is approved and real differences are known.

The conceptual future direction is:

```text
profile (composition policy)
  |-- selects core
  `-- selects feature contexts
          |
          `-- source state managed through chezmoi
                    |
                    `-- user environment
```

This diagram is explicitly labeled conceptual. No such runtime or configuration flow is created by this change.

#### Planned `chezmoi` role

`chezmoi` will be documented as the intended future source-state and application mechanism because it supports reproducible dotfile management and templating across machines. It is a direction, not a currently configured dependency. Package installation, profile orchestration, and the exact boundary between `chezmoi` and future bootstrap automation remain decisions for executable changes.

#### Illustrative layout

The document will show a compact tree containing the intended major areas such as `docs/`, `profiles/`, `modules/`, and a future chezmoi source-state area. The tree must be titled **Illustrative future layout** and annotate absent areas as planned. It must not imply that empty directories should be created now.

### `docs/decisions.md`: lightweight decision overview

This file will use short, stable decision records rather than a heavyweight ADR framework. Each record contains:

- status (`Accepted` for current direction);
- decision;
- rationale;
- alternatives considered;
- consequences and triggers for reconsideration.

The initial records will cover:

| ID | Decision |
| --- | --- |
| D-001 | Establish documentation before executable automation. |
| D-002 | Deliver Fedora first; defer Windows/WSL and macOS. |
| D-003 | Use one modular monolith with lightweight bounded contexts. |
| D-004 | Treat `chezmoi` as the intended dotfiles manager, not a current capability. |
| D-005 | Keep the public repository free of credentials, private host details, employer information, and machine-specific secrets. |
| D-006 | Prefer a practical-but-polished experience, with clarity and productivity ahead of decoration. |

D-003 will explicitly state that profiles compose modules, modules retain ownership, and formal DDD mechanisms are premature. D-005 will require generic public examples and identify secret detection/enforcement as work to design with executable changes rather than tooling added now.

## Documentation contracts

### Status vocabulary

All documents will use these meanings consistently:

- **Current:** present and verifiable in the repository now.
- **Planned:** approved architectural direction without delivered behavior.
- **Future:** roadmap possibility that requires a separate approved change.

Words such as “supported,” “installs,” “configures,” and “provides” must not describe planned functionality in present tense.

### Navigation

README links will use repository-relative paths:

- `docs/architecture.md`
- `docs/decisions.md`

Links between the two detail documents are optional and should be added only where they reduce duplicated explanation. No link may target an absent future file or directory as if it exists.

### Safety

Examples and prose must contain no credentials, tokens, private hostnames, employer identifiers, personal machine paths, or private account data. Tool names and the public project name are safe. No example will instruct readers to place secrets in managed dotfiles.

## Verification design

No test runner will be selected for this documentation-only change. Verification is repository inspection plus Markdown review:

| Check | Evidence |
| --- | --- |
| Changed scope is documentation-only | Diff contains only `README.md`, `docs/architecture.md`, and `docs/decisions.md`. |
| Required documents exist | All three paths can be read from the repository. |
| Navigation works | Each relative README link resolves to an existing file. |
| Status is truthful | Search/review confirms planned tools and platforms are not described as delivered. |
| Boundaries are complete | Architecture names all eight contexts and states ownership and dependency rules. |
| Decisions are complete | Decision overview covers all six initial decisions and their tradeoffs. |
| No premature scaffolding | No module, profile, installer, configuration, manifest, CLI, or test files are added. |
| Public content is safe | Manual review checks for credentials, private identifiers, host details, and machine-specific data. |
| Review remains bounded | Total changed documentation stays within the configured 500-line budget. |
| Presentation is usable | Headings, tables, links, and concise sections support progressive disclosure in English. |

Because there is no executable behavior, idempotency, installation, and workstation-state tests do not apply to this milestone. The first executable change must separately select verification tooling and follow strict TDD.

## Rollout and rollback

The three documents should land together so the README never links to missing foundation pages. There is no migration, compatibility handling, or workstation rollout because nothing is executed or applied.

Rollback is a normal documentation revert: restore the prior README and remove the two new docs. No packages, user files, shell state, or machine configuration require restoration. Later architectural learning should normally supersede a decision in `docs/decisions.md` rather than silently rewriting its history.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| “Bounded context” suggests unnecessary DDD machinery | Define it narrowly as ownership guidance and explicitly reject aggregates, events, and interfaces for now. |
| Profiles become a dumping ground | State that profiles compose contexts and cannot own duplicated module behavior. |
| The planned tree appears implemented | Label it illustrative and distinguish absent paths from current files. |
| Documentation drifts across files | Assign each fact a primary owner and use links for detail. |
| `chezmoi` sounds operational | Describe it only as intended direction and defer source-state setup. |
| The README overpromises support | Lead with documentation-only status and use controlled status vocabulary. |
| Review exceeds the line budget | Keep detailed rationale in the two focused docs and avoid repeated prose. |

## Scope guardrail

Completion of this design authorizes only repository-facing documentation. Fedora installation, package management, shell or tool configuration, real profiles/modules, managed chezmoi state, Windows/WSL/macOS behavior, a custom CLI, a `doctor` command, and test-runner selection remain outside this change and require later SDD work.
