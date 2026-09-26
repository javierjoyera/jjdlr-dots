# jjdlr-dots project context

## Vision

`jjdlr-dots` is an open-source personal dotfiles repository for learning how to build and maintain a reproducible workstation environment. It should provide a modern, attractive, and practical terminal experience while keeping every tool and configuration decision understandable.

## Scope and roadmap

- **First verified platform:** macOS.
- **First planned implementation slice:** minimal chezmoi source state and application flow with Starship configuration on macOS.
- **Future platforms:** Linux and Windows, introduced through later approved changes while preserving portable ownership boundaries.
- **Deferred ideas:** broader modules and profiles, package installation, additional terminal tools, tmux support, a possible Go CLI, and a `doctor` command.

Work should proceed in small, reviewable milestones rather than generating the complete environment at once.

## Architecture

Use a **modular monolith**: one repository with explicit responsibility boundaries rather than unrelated scripts. Intended modules are:

- `core`: operating-system detection, base packages, and common dependencies.
- `shell`: shell setup, aliases, functions, exports, and `PATH`.
- `terminal`: terminal-emulator configuration, initially Kitty or WezTerm.
- `multiplexer`: Zellij initially, with possible future tmux support.
- `monitoring`: visual system tools such as btop and fastfetch.
- `git`: Git configuration, lazygit, and useful aliases.
- `devtools`: mise, runtime tooling, and development helpers.
- `profiles`: platform and context overlays such as Fedora, Windows, macOS, work, and personal.

`chezmoi` is the selected dotfile management and application layer. Its first use should remain minimal: establish only the source state and behavior required for the macOS-first Starship slice. Additional tools belong to later changes rather than the initial implementation.

## Engineering principles

- Keep module responsibilities clear and automation readable.
- Make fresh-machine installation simple, portable, and eventually reproducible.
- Keep secrets and private machine data out of the public repository.
- Prefer practical behavior over appearance, while still providing a polished terminal.
- Treat documentation as a first-class deliverable and explain decisions.
- Do not copy third-party dotfiles without understanding and adapting them.
- Verify macOS first; add Linux and Windows only through later scoped changes.
- Use strict test-driven development once executable behavior is introduced.

## Current repository state

As of 2026-07-22, the repository contains an MIT license, repository documentation, archived foundation SDD artifacts, and a GitHub Actions check that runs `scripts/check-local-paths.sh`. There is no managed chezmoi source state, Starship configuration, dependency manifest, package/build system, automated test runner, coverage tool, linter, type checker, or formatter. The current branch is `main`.

Strict TDD remains project policy, but it is not yet executable because no test runner exists. The first implementation proposal must select suitable automated checks before implementation. Until then, verification is limited to repository inspection, artifact/schema checks, shell syntax validation, and the local-path safety check.

The repository-facing README, architecture decisions, and merged foundation specification still describe Fedora-first sequencing. They are preserved as historical/current artifacts during initialization and must be reconciled through the next approved SDD change rather than rewritten out of phase.

## SDD operating constraints

- Current workflow mode is interactive: complete one SDD phase at a time.
- The artifact store is OpenSpec.
- The review budget is 800 changed lines.
- Use a single pull request by default; split only when reviewability or cohesion requires it.
- Initialization must not create explore, proposal, spec, design, task, or implementation artifacts.

## Source

Updated from the repository state and the user-approved macOS-first, minimal-chezmoi direction. Technical artifacts remain in English.
