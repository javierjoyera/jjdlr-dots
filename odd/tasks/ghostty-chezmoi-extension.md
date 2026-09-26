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
- The self-whitelisting `.codegraph/.gitignore` is committed so every clone keeps local index data out of git.
- The feature branch follows the repository Git flow table (`feature/<short-description>`).

## Verified state (2026-09-26)

- Source `chezmoi/dot_config/ghostty/config` and applied target `$HOME/.config/ghostty/config` are byte-identical.
- `chezmoi --source ./chezmoi diff` and `chezmoi --source ./chezmoi status` report no drift and no other managed target.
- `ghostty +validate-config` (Ghostty 1.3.1) reports no warnings or errors.
- Effective configuration resolves `font-family = MesloLGS Nerd Font Mono`, `font-size = 14`, `theme = Catppuccin Mocha`, `scrollback-limit = 10000`, `window-padding-x = 12`.
- The theme resolves from Ghostty's bundled resources (`Catppuccin Mocha (resources)`; 463 themes available), so no external theme file is required.
- The applied configuration came from an explicit-source `chezmoi --source ./chezmoi apply`, not from the planned `scripts/macos-starship` workflow, which does not exist yet.
- chezmoi has no persistent source configuration: `$HOME/.local/share/chezmoi` is absent and there is no `$HOME/.config/chezmoi/chezmoi.toml`, so every command must pass `--source <repo>/chezmoi`. This is the cause of the earlier "apply ran but nothing changed" symptom.
- `.codegraph/.gitignore` already contains `*` plus `!.gitignore`, so the local CodeGraph database and daemon files cannot be committed by accident; only the self-whitelisting `.gitignore` itself appeared as untracked.

## Tasks

1. [x] Correct the stale `MesloLGS NF` alias to the installed family name `MesloLGS Nerd Font Mono` in the frozen OpenSpec design and task artifacts. Evidence: `design.md` (lines 112, 168) and `tasks.md` (lines 91, 94) now use the resolvable family name; the only remaining mentions of the old shorthand are explicit statements that it does not resolve.
2. [x] Resolve the local-index ignore policy without adding a redundant root `.gitignore` entry. Evidence: `git check-ignore -v .codegraph/codegraph.db` reports `.codegraph/.gitignore:4:*`; that self-whitelisting file is committed in `e6897c6`.
3. [x] Run the available checks. Evidence: `./scripts/check-local-paths.sh` printed `No local user paths detected.` and exited 0; `ghostty +validate-config` exited 0; `chezmoi --source ./chezmoi apply --dry-run --verbose` exited 0 with no planned change, confirming convergence.
4. [x] Create work-unit commits for this slice. Evidence: `e6897c6`, `6bd1150`, `49a40c0`.
5. [x] Record the corrected manual-verification status. See the section below.

## Manual verification status

- Human-verified on 2026-09-26: the applied Ghostty configuration renders with the intended font family and theme. The user confirmed the terminal now displays correctly, and the harness corroborated font resolution, theme resolution, and zero drift against the source.
- Still unverifiable: `openspec/changes/macos-chezmoi-starship-foundation/tasks.md:94` also requires confirming that Starship glyphs render correctly. No Starship target exists in the chezmoi source yet, so that half of the task stays open and unchecked.

## Commits

| Commit | Change |
| --- | --- |
| `e6897c6` | `chore: ignore the local CodeGraph index` |
| `6bd1150` | `docs: plan the macOS chezmoi and Ghostty foundation` |
| `49a40c0` | `feat: add the portable Ghostty configuration` |

## Follow-ups

- Implement the SDD task list of `macos-chezmoi-starship-foundation`: `scripts/macos-starship`, `.chezmoiroot`, `scripts/lib/*`, `scripts/tests/macos-starship-test.sh`, and `docs/macos-starship.md`. Until then, applying this configuration requires the manual `chezmoi --source <repo>/chezmoi apply`.
- Decide the chezmoi source binding. Without a `chezmoi.toml` `sourceDir` or `.chezmoiroot`, every command must pass `--source`, and the default source path does not exist on this host.
- Add the Starship configuration target so the second half of the manual verification task becomes testable.

## Non-goals

- Installing or uninstalling Ghostty.
- Editing macOS preferences, terminal profiles, or `.zshrc` for Ghostty.
- Adding host-specific profiles, secrets, or absolute paths.

## Evidence

- `openspec/changes/macos-chezmoi-starship-foundation/` carries the approved scope for this feature; this document tracks the narrower, already-implemented slice.
- `openspec/changes/macos-chezmoi-starship-foundation/tasks.md:94` requires manual verification of the selected font, which is only half satisfiable today.
