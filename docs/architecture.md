# Planned architecture boundaries

This document describes **planned** boundaries, not implemented modules. **Current** repository content is documentation only; no profiles, modules, installer, managed dotfiles, or `chezmoi` source state exists yet.

## Quick path

1. Read the ownership table to see where a future configuration belongs.
2. Apply the dependency rules before coupling planned areas.
3. Treat the layout and platform plan as direction, not as files or support available today.

## Status vocabulary

- **Current:** present and verifiable in this repository now.
- **Planned:** approved direction without delivered behavior.
- **Future:** a possibility that requires a separate approved change.

## Modular monolith

The project is planned as one modular monolith: one coherent repository with small, explicit ownership contexts instead of independently deployed components or a shared configuration dumping ground. The goal is to keep a workstation setup understandable while it grows.

“Context” is an ownership aid, not formal domain-driven design. This plan does not introduce aggregates, events, service interfaces, or framework abstractions.

| Planned context | Owns | Does not own |
| --- | --- | --- |
| `core` | OS detection, shared prerequisites, and base package policy | Tool presentation or profile policy |
| `shell` | zsh, prompt integration, aliases, functions, exports, and `PATH` policy | Terminal-emulator or multiplexer settings |
| `terminal` | Terminal-emulator configuration, initially Kitty | Shell behavior or session orchestration |
| `multiplexer` | Zellij configuration and layouts; possible later tmux support | Terminal settings or monitoring configuration |
| `monitoring` | btop, fastfetch, and related inspection presentation | Base packages or development runtimes |
| `git` | Git behavior, aliases, and lazygit configuration | General shell aliases or unrelated developer tools |
| `devtools` | mise, language/runtime tooling, and development helpers | Core OS setup or Git-specific configuration |
| `profiles` | Composition of contexts for a platform or usage context, initially Fedora | Context internals or copied tool configuration |

## Composition and dependencies

1. `profiles` select and compose contexts; they do not absorb or duplicate their responsibilities.
2. `core` is foundational and must not depend on feature contexts or profiles.
3. Feature contexts may use capabilities established by `core`, but must not depend on profiles.
4. Each configuration item has one owner. Other contexts reference that capability instead of maintaining a second copy.
5. Direct dependencies between feature contexts are avoided; any necessary future coupling must document ownership and direction first.
6. Platform selection belongs in profiles; context-specific configuration remains with its owner.

Conceptually, a future profile selects `core` and feature contexts. Future source state may be managed through `chezmoi` before reaching a user environment. This is a planning model only; it creates no runtime flow today.

## Platform sequencing

**Planned:** Fedora Linux is first because it provides a focused learning and implementation path. A future Fedora milestone can validate the ownership model with real automation before the project generalizes it.

**Future:** Windows, WSL, and macOS are deliberately out of scope until separately approved. Cross-platform abstractions should be introduced only when real platform differences are known.

`chezmoi` is the intended future source-state and dotfile application direction because it can support reproducible management and templating across machines. It is not configured now. The boundary between it, package installation, and future bootstrap automation remains for executable changes to decide.

## Illustrative future layout

The following is a **planned illustration**, not a representation of existing directories and not a request to create empty scaffolding.

```text
jjdlr-dots/
├── README.md                 # Current entry point
├── docs/                     # Current foundation documentation
│   ├── architecture.md
│   └── decisions.md
├── profiles/                 # Planned composition policy
├── modules/                  # Planned: core and feature contexts
│   ├── core/
│   ├── shell/
│   ├── terminal/
│   ├── multiplexer/
│   ├── monitoring/
│   ├── git/
│   └── devtools/
└── chezmoi/                  # Planned future source-state area
```

## Boundaries for later work

Installer work, package management, tool configuration, managed dotfiles, platform implementations, a CLI or `doctor` command, and test-runner selection are deferred. When implementation starts, keep one owner per configuration item and update this document only when the demonstrated design warrants a boundary change.

For the rationale behind these choices, see [the decision overview](decisions.md).
