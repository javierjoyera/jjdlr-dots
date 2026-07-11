# Establish the repository foundation before adding automation

Create a small, documentation-first foundation for `jjdlr-dots` so contributors can understand the project's purpose, Fedora-first direction, and intended modular-monolith architecture before executable dotfiles or installation behavior are introduced.

## Intent

The repository currently communicates little beyond its source context and OpenSpec metadata. This change will turn the repository entry points into a practical, polished guide that explains what the project is, why its architecture is shaped this way, and how later milestones should grow it without prematurely creating implementation scaffolding.

This first milestone is deliberately educational: decisions and tradeoffs should be explained, not merely listed. Clarity and productivity take priority over visual decoration, while the presentation should still feel intentional and welcoming.

## Scope

### Included

- Build a clear README foundation that:
  - states the project's purpose and learning-oriented goals;
  - identifies Fedora as the first supported platform;
  - summarizes the planned tool ecosystem without implying it is already installed or configured;
  - gives readers a concise map of the current documentation and roadmap;
  - clearly labels the repository's current documentation-only status.
- Add foundational architecture documentation that:
  - records the modular-monolith direction;
  - defines the intended responsibilities of `core`, `shell`, `terminal`, `multiplexer`, `monitoring`, `git`, `devtools`, and `profiles`;
  - explains why Fedora-first delivery and `chezmoi` are the current direction;
  - distinguishes planned architecture from implemented capability.
- Add a lightweight decision record or decision overview covering the important initial choices and tradeoffs, including documentation-first delivery, Fedora-first sequencing, modular boundaries, public-repository secret safety, and practical-but-polished product tone.
- Document the desired future repository layout without creating numerous empty module, profile, platform, or configuration directories.
- Keep the documentation concise enough for a small first review while using progressive disclosure, clear headings, tables, and links where they reduce reader effort.

### Explicitly deferred

- Fedora installer scripts, package installation, or operating-system automation.
- Shell, Starship, terminal emulator, Zellij, tmux, btop, fastfetch, Git, development-tool, or other tool configuration.
- Concrete `chezmoi` source-state setup or managed dotfiles.
- Windows, WSL, PowerShell, Windows Terminal, or macOS implementation.
- A custom CLI, including any Go-based command-line application.
- A `doctor` or environment-validation command.
- Automated test-runner selection; that belongs with the first executable change.

## Affected areas

| Area | Proposed effect |
| --- | --- |
| `README.md` | Becomes the primary project entry point and accurately describes current versus planned capability. |
| `docs/architecture.md` | Explains the target modular-monolith boundaries and staged platform strategy. |
| `docs/decisions.md` | Captures initial decisions, rationale, alternatives, and consequences in a lightweight form. |
| Repository layout | Remains minimal; the planned structure is documented rather than represented by empty directories. |
| Future changes | Gain explicit boundaries for the later Fedora installer, modules, configurations, and cross-platform work. |

No executable behavior, user configuration, package state, or workstation state changes in this milestone.

## Product and documentation principles

- Lead with what exists now, then disclose the future roadmap.
- Never present planned tools or platforms as currently supported.
- Explain enough rationale that a learner can understand and revisit each decision.
- Prefer practical navigation and scanability over decorative complexity.
- Keep examples free of credentials, private host details, employer information, and machine-specific secrets.
- Preserve room for future platforms without adding speculative abstractions or empty scaffolding now.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Documentation overpromises a working dotfiles setup. | Label the repository as documentation-only and separate current state from roadmap. |
| The architecture becomes too detailed before implementation teaches us more. | Document responsibility boundaries and intent, not low-level interfaces or premature conventions. |
| Empty directories create a false sense of implementation progress and maintenance burden. | Show the desired layout in documentation and create directories only when a later milestone needs them. |
| Aesthetic goals make the README noisy or harder to maintain. | Use a practical-but-polished hierarchy; prioritize concise prose, navigation, and accurate status. |
| Public documentation leaks personal or machine-specific information. | Use generic examples and review all content for secrets and private identifiers. |
| The milestone expands into installer or tool configuration work. | Keep every executable and platform implementation item explicitly deferred to separate approved changes. |

## Rollback

Rollback is documentation-only: revert the README and foundational docs introduced by this change. No workstation state, user files, installed packages, or executable behavior will need restoration. If an architectural decision proves premature, revise or supersede its documentation in a later change rather than preserving misleading guidance.

## Success criteria

- A new reader can identify the project's purpose, current status, Fedora-first direction, and next milestone from the README without consulting private context.
- The architecture documentation explains the modular-monolith approach and each planned responsibility boundary without claiming those modules exist today.
- Initial decisions and their tradeoffs are recorded in a discoverable, didactic form.
- The intended repository structure is visible in documentation, while unnecessary empty implementation directories are absent.
- Fedora installer work, shell/tool configuration, Windows/macOS implementation, CLI work, and the `doctor` command are unambiguously out of scope.
- Repository-facing documentation is in English, easy to scan, internally consistent, and contains no secrets or private machine data.
- The change remains documentation-only and reviewable within the 500-line budget.

## Proposal question round

The supplied answers establish these proposal assumptions:

1. The first deliverable is documentation and a minimal structural foundation, not an installer.
2. Documentation should teach the reasoning and tradeoffs behind decisions.
3. The desired directory structure should be documented before implementation needs create those directories.
4. The product tone should be practical but polished, with clarity and productivity ahead of aesthetics.
5. Planned tools and platforms are roadmap context only and must not appear as delivered capability.

No additional product decision is required to bound this proposal. These assumptions can still be corrected before the next SDD phase, or a second product-question round can be requested if further refinement is desired.
