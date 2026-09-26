# Proposal: macOS chezmoi and Starship foundation

## Intent

Deliver a visibly working Starship prompt in Zsh on macOS, with a bounded Ghostty configuration for the terminal used to verify it. Replace the active Fedora-first direction while protecting existing shell configuration and public-repository safety.

## Scope

### In Scope
- Install only `chezmoi`, Starship, and one Nerd Font idempotently through existing Homebrew.
- Add isolated Starship and Ghostty state and a preview-first chezmoi workflow.
- Manage only `~/.config/starship.toml` and `~/.config/ghostty/config` through chezmoi.
- Treat an existing Ghostty installation as an external prerequisite; do not install or uninstall Ghostty.
- Preserve an existing `.zshrc`; add only the already-scoped reversible, uniquely delimited Starship initialization block. The Ghostty target introduces no `.zshrc` change.
- Verify preview, apply, no-op re-run, rollback, both-target config preservation, and secret/path safety.
- Reconcile active docs and repository-foundation requirements with macOS-first delivery.

### Out of Scope
- Homebrew installation; Linux, Windows, and other package ecosystems.
- Full `.zshrc` ownership, broader Zsh, secrets, extra tools, or terminal emulators beyond the configuration-only Ghostty target.
- Ghostty installation or uninstallation, macOS preference changes, or automated terminal UI changes; font and visual verification remain manual in Ghostty.
- Any edits to archived SDD history.

## Capabilities

### New Capabilities
- `macos-chezmoi-starship-foundation`: Safe dependency bootstrap, isolated Starship and Ghostty configuration application, minimal Zsh activation, preview, idempotency, and rollback.

### Modified Capabilities
- `repository-foundation`: Replace Fedora-first/documentation-only requirements with macOS-first status, implemented boundaries, and the current review budget.

## Approach

Use a nested chezmoi source root so repository files cannot map accidentally into `$HOME`. Preview before mutation, install the approved Homebrew-managed dependencies, apply the Starship and Ghostty configurations, and insert a delimited Starship initialization block without replacing `.zshrc`. Ghostty itself must already be installed outside this workflow and is never installed or uninstalled here. Back up both chezmoi targets and the existing shell target before changing them. Automated checks use an isolated home; prompt and glyph rendering are verified manually in Ghostty without changing macOS preferences.

## Affected Areas

| Area | Impact | Description |
|---|---|---|
| `.chezmoiroot`, nested source | New | Isolated Starship and Ghostty state |
| `scripts/` | New/Modified | Bootstrap, integration, checks, rollback |
| `README.md`, `docs/*.md` | Modified | macOS-first workflow and rationale |
| `openspec/specs/repository-foundation/spec.md` | Modified | Active contract |

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Existing shell state is damaged | Medium | Preview, backup, markers, isolated-home tests |
| Re-run duplicates work or config | Medium | Idempotency checks and marker-aware updates |
| Public files expose local data | Low | Path/secret checks and generic fixtures |
| Ghostty is unavailable for manual verification | Medium | State the external installation prerequisite and stop short of managing the application |
| Font glyphs do not render | Medium | Manual Ghostty font and prompt verification |

## Rollback Plan

Remove only the Zsh block, restore or remove the managed Starship and Ghostty targets according to their pre-apply state, and preview the reverted state. Homebrew-managed packages remain unless the user runs documented uninstall commands; Ghostty is never installed or uninstalled by this workflow.

## Dependencies

- macOS with Homebrew and network access.
- Ghostty already installed outside this workflow for manual verification; its installation is not an apply prerequisite for managing `~/.config/ghostty/config`.

## Success Criteria

- [ ] After preview, apply, and manual verification in an externally installed Ghostty, a new Zsh session shows Starship with the configured font and glyphs.
- [ ] Re-running produces no duplicate block or unintended change.
- [ ] Existing `.zshrc`, Starship, and Ghostty configuration content survives apply and rollback according to the documented ownership and backup rules.
- [ ] Checks prove the two-target isolated mapping, syntax, idempotency, rollback, and secret/path safety.
- [ ] Active docs/specs agree on macOS-first scope; archived artifacts are unchanged.
