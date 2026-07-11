# jjdlr-dots project context

## Vision

`jjdlr-dots` is an open-source personal dotfiles repository for learning how to build and maintain a reproducible workstation environment. It should provide a modern, attractive, and practical terminal experience while keeping every tool and configuration decision understandable.

## Scope and roadmap

- **MVP platform:** Fedora Linux.
- **Future platforms:** a conservative enterprise Windows setup using Windows Terminal, PowerShell, and/or WSL; macOS later.
- **Initial milestones:** establish the repository structure, README and architecture documentation; add a basic Fedora installer; then introduce the `core` and `shell` modules followed by Starship, Zellij, btop, and fastfetch configuration.
- **Deferred ideas:** broader modules and profiles, tmux support, a possible Go CLI, and a `doctor` command.

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

`chezmoi` is the intended dotfiles manager. The Fedora MVP toolset is zsh, Starship, Zellij, Kitty, btop, fastfetch, eza, bat, fd, ripgrep, fzf, zoxide, lazygit, and mise.

## Engineering principles

- Keep module responsibilities clear and automation readable.
- Make fresh-machine installation simple, portable, and eventually reproducible.
- Keep secrets and private machine data out of the public repository.
- Prefer practical behavior over appearance, while still providing a polished terminal.
- Treat documentation as a first-class deliverable and explain decisions.
- Do not copy third-party dotfiles without understanding and adapting them.
- Implement Fedora first; add other platforms only through later scoped changes.
- Use strict test-driven development once executable behavior is introduced.

## Current repository state

As of 2026-07-10, the repository contains an MIT license, an empty README, empty architecture and Git-flow documents, and local SDD runtime metadata. There is no implementation, dependency manifest, package/build system, or automated test runner yet. Git is initialized and points to an existing remote; the active branch is `docs/project-information` based on `main`.

Testing infrastructure must be selected and documented with the first executable implementation. Until then, verification is limited to artifact/schema checks and repository inspection.

## SDD operating constraints

- Current workflow mode is interactive: complete one SDD phase at a time.
- The artifact store is OpenSpec.
- The review budget is 500 changed lines.
- Chained pull requests require asking the user each time.
- Initialization must not create explore, proposal, spec, design, task, or implementation artifacts.

## Source

Synthesized in English from `.context/objetivo.md`; that Spanish source remains the authoritative statement of the user's initial intent.
