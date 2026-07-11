# jjdlr-dots

`jjdlr-dots` is a learning-oriented project for building a reproducible, modular, and maintainable personal workstation environment. **Current status:** this repository is a documentation foundation only; it has no supported installer and no working dotfiles yet.

## Direction at a glance

| Status | Direction |
| --- | --- |
| **Current** | Documentation that records the intended architecture and its decisions. |
| **Planned** | Fedora Linux is the first implementation target. |
| **Future** | Windows/WSL and macOS need separate approved changes before implementation. |

The planned Fedora tool ecosystem is roadmap context, not installed or configured capability: zsh and Starship for the shell experience; Kitty and Zellij for terminal work; btop and fastfetch for inspection; and Git, lazygit, mise, eza, bat, fd, ripgrep, fzf, and zoxide for daily development.

## Read the foundation

| Document | What it answers |
| --- | --- |
| [Architecture](docs/architecture.md) | How the planned modular-monolith boundaries, platform sequence, and future layout fit together. |
| [Decisions](docs/decisions.md) | Why this milestone is documentation-first and which tradeoffs guide later work. |

## Roadmap

1. **Current:** document the project purpose, ownership boundaries, and decisions.
2. **Next:** propose a separate Fedora installer milestone.
3. **Future:** add configuration and additional platform support only through approved changes.

There are intentionally no installation or package commands in this repository yet.

## Contribute safely

Keep changes focused, readable, and accurate about **Current**, **Planned**, and **Future** capability. This is a public repository: never commit credentials, tokens, private host details, employer information, personal machine paths, or other machine-specific secrets. Use generic examples and preserve the documented ownership boundaries when implementation begins.
