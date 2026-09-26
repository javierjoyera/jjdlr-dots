# Feature: Ghostty chezmoi extension

## Goal

Extend the existing macOS chezmoi + Starship foundation so this repository also owns a portable Ghostty configuration, without installing Ghostty or modifying unrelated system preferences.

## Decisions

- Ghostty configuration only; Ghostty installation remains outside this repository.
- Manage only `$HOME/.config/ghostty/config` through the nested chezmoi source.
- Preserve the existing Starship and `.zshrc` boundaries.
- Preview before apply; rollback removes or restores only managed files.
- Keep machine-specific paths, secrets, and host state out of the repository.
- The frozen artifacts must name the font by its installed family name, `MesloLGS Nerd Font Mono`, not by the unresolved alias `MesloLGS NF`.

## Verified state (2026-09-26)

- Source `chezmoi/dot_config/ghostty/config` and applied target `~/.config/ghostty/config` are byte-identical.
- `chezmoi --source ./chezmoi diff` and `chezmoi --source ./chezmoi status` report no drift and no other managed target.
- `ghostty +validate-config` (Ghostty 1.3.1) reports no warnings or errors.
- Effective configuration resolves `font-family = MesloLGS Nerd Font Mono`, `font-size = 14`, `theme = Catppuccin Mocha`, `scrollback-limit = 10000`, `window-padding-x = 12`.
- The theme resolves from Ghostty's bundled resources (`Catppuccin Mocha (resources)`; 463 themes available), so no external theme file is required.
- The applied configuration came from an explicit-source `chezmoi --source ./chezmoi apply`, not from the planned `scripts/macos-starship` workflow, which does not exist yet.
- chezmoi has no persistent source configuration: `~/.local/share/chezmoi` is absent and there is no `~/.config/chezmoi/chezmoi.toml`, so every command must pass `--source <repo>/chezmoi`. This is the cause of the earlier "apply ran but nothing changed" symptom.
- `.codegraph/.gitignore` already contains `*` plus `!.gitignore`, so the local CodeGraph database and daemon files cannot be committed by accident; only the self-whitelisting `.gitignore` itself appears as untracked.

## Tasks

1. Correct the stale `MesloLGS NF` alias to the installed family name `MesloLGS Nerd Font Mono` in the frozen OpenSpec design and task artifacts.
2. Resolve the local-index ignore policy: no root `.gitignore` edit is required because `.codegraph/.gitignore` already ignores every data file while whitelisting itself; decide whether that self-whitelisting file is committed.
3. Run the available checks: `./scripts/check-local-paths.sh`, `ghostty +validate-config`, and a chezmoi dry-run against the nested source.
4. Create work-unit commits for this slice and record their identities as evidence.
5. Record the corrected manual-verification status, including the part that is still unverifiable.

## Non-goals

- Installing or uninstalling Ghostty.
- Editing macOS preferences, terminal profiles, or `.zshrc` for Ghostty.
- Adding host-specific profiles, secrets, or absolute paths.
- Implementing `scripts/macos-starship`, `.chezmoiroot`, or the SDD task list of `macos-chezmoi-starship-foundation`.

## Evidence

- `openspec/changes/macos-chezmoi-starship-foundation/` carries the approved scope for this feature; this document tracks the narrower, already-implemented slice.
- `openspec/changes/macos-chezmoi-starship-foundation/tasks.md:94` requires manual verification of the selected font; only its Ghostty half is currently verifiable because no Starship target exists in the source yet.
