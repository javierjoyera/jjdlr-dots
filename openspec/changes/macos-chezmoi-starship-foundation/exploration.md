## Exploration: macOS chezmoi and Starship foundation

### Current State

The repository is a documentation foundation with no managed dotfiles, chezmoi source state, Starship configuration, dependency manifest, test runner, linter, or formatter. The existing local-path check is the only repository automation (`scripts/check-local-paths.sh`), and GitHub Actions runs it. The project context now identifies macOS as the first verified platform, chezmoi as the minimal application layer, and Linux/Windows as later evolutions.

The repository-facing artifacts are not yet reconciled: `README.md`, `docs/architecture.md`, and `docs/decisions.md` still describe Fedora as the first implementation target. The merged `openspec/specs/repository-foundation/spec.md` also preserves that Fedora-first contract. These are the Fedora-first artifacts that this change must supersede or explicitly update in its later proposal/spec work; the archived foundation change remains historical and must not be rewritten.

Upstream behavior relevant to the slice:

- chezmoi normally uses `~/.local/share/chezmoi` as its source directory and maps source-state names such as `dot_config/starship.toml` to `~/.config/starship.toml`.
- A `.chezmoiroot` file can point the source root at a nested directory, allowing repository documentation and OpenSpec artifacts to coexist without being interpreted as home-directory targets.
- `chezmoi status` and `chezmoi diff` preview changes; `chezmoi apply` applies the computed state. `chezmoi init` initializes source state and can optionally apply it, so the public workflow must not make implicit application the only path.
- Starship needs the `starship` executable and shell initialization (for zsh, `eval "$(starship init zsh)"`). Its configuration convention is `~/.config/starship.toml`, or a path selected with `STARSHIP_CONFIG`.
- Starship's current upstream guide lists an installed and enabled Nerd Font as a prerequisite for the intended glyph experience. Font installation is not the responsibility of a dotfile source-state change.

### Affected Areas

- `README.md` — must stop presenting Fedora as the first implementation target and describe the macOS-first foundation without claiming package installation or complete shell support.
- `docs/architecture.md` — must define the initial chezmoi/Starship ownership boundary and distinguish source-state application from bootstrap and package installation.
- `docs/decisions.md` — must supersede the Fedora sequencing decision and record the macOS-first, minimal-chezmoi tradeoff rather than silently rewriting history.
- `openspec/specs/repository-foundation/spec.md` — the later proposal/spec should modify the Fedora-first requirements so the source-of-truth specification matches the approved direction.
- `openspec/changes/archive/2026-07-11-bootstrap-repo-foundation/` — historical audit trail; do not edit. Its Fedora-first statements explain why the active delta must be explicit.
- New chezmoi source-state area (exact path to be chosen in design) — likely one Starship TOML file and no broad shell/tool configuration in the first slice.
- `scripts/check-local-paths.sh` and `.github/workflows/local-path-validation.yml` — existing safety checks should remain enabled and be extended only if new fixtures or validation need it.

### Approaches

1. **Nested chezmoi source root with configuration-only first slice** — keep repository docs at the top level, add `.chezmoiroot` pointing to a dedicated source directory (for example `home/`), and manage only `home/dot_config/starship.toml`.
   - Pros: prevents README/docs/OpenSpec files from becoming accidental home targets; makes ownership and review boundaries obvious; avoids clobbering an existing `.zshrc`; keeps package installation, font setup, and shell policy separate.
   - Cons: Starship is not active until the executable and zsh initialization exist; the nested layout adds one chezmoi convention to teach.
   - Effort: Low

2. **Nested source root with Starship config plus a managed zsh initialization file** — use the same isolation, but also manage `.zshrc` or a sourced Starship fragment.
   - Pros: can provide a complete prompt activation path when the executable is already installed; application is more visibly useful.
   - Cons: `.zshrc` is high-collision user state; a fragment still needs a reliable sourcing contract; it couples shell ownership to the first slice and risks silently replacing user configuration.
   - Effort: Medium

3. **Root-level chezmoi source state** — use repository root as the source root and rely on naming conventions or exclusions while keeping docs beside managed files.
   - Pros: fewer directories and familiar default chezmoi behavior.
   - Cons: unsafe default for this repository because ordinary documentation paths can be interpreted as destination files; harder to explain and validate; increases accidental home-directory writes.
   - Effort: Low initially, high safety/maintenance cost

### Recommendation

Use Approach 1 for the first implementation boundary: an isolated nested chezmoi source root managing only a Starship configuration file. The first slice should prove source-state initialization, preview, safe apply, idempotent re-apply, and rollback of that one file. It should not install chezmoi, Starship, a Nerd Font, Homebrew, or any other package; those belong to a later macOS bootstrap/package change. It should not take ownership of `.zshrc` unless a separate decision establishes that the file is wholly owned by this project.

The proposal should define the following ownership contract:

| Concern | First slice owner | Deferred responsibility |
| --- | --- | --- |
| Starship TOML content | chezmoi source state | richer prompt modules and machine-specific tuning |
| Rendering/application to `~/.config/starship.toml` | chezmoi | bootstrap orchestration |
| `chezmoi` binary installation | none in this slice | macOS bootstrap/package manager |
| `starship` binary installation | none in this slice | macOS bootstrap/package manager |
| zsh initialization | documented prerequisite or later shell slice | shell module / explicitly owned shell file |
| Nerd Font installation and terminal selection | none in this slice | macOS bootstrap/terminal slice |
| secrets and machine-specific values | no public source-state secrets | later approved secret integration |

Strict TDD is policy, but no runner exists. Before implementation, the design/tasks phase must select executable checks and write them first. A small, tool-independent initial check set can validate: source layout and `.chezmoiroot`; `starship.toml` parseability using the installed Starship binary when available; `chezmoi diff`/status expectations against an isolated temporary home; apply twice with no second diff; rollback by restoring/removing the managed target; local-path safety; secret-pattern scanning; shell syntax only if shell initialization is added; and the existing GitHub Actions check. Tests requiring real package installation, a Nerd Font, or a user's live home directory should remain manual verification, not CI prerequisites.

The later proposal should supersede Fedora-first wording in the active repository-facing artifacts and main foundation spec. The archived `bootstrap-repo-foundation` artifacts should remain unchanged as historical evidence.

### Risks

- A root-level source state could accidentally map documentation into `$HOME`; isolation with `.chezmoiroot` and a temporary-home test is the primary mitigation.
- Managing `.zshrc` can overwrite user-owned shell behavior. Keep it out of the first slice or define an explicit merge/sourcing contract before implementation.
- A valid Starship config does not guarantee a working prompt when the binary, zsh init, or Nerd Font is absent. Verification must separate rendered configuration from runtime appearance.
- `chezmoi init --apply` can write immediately. Document and test preview-first behavior, and make rollback a concrete target-file restore/removal procedure.
- Templates can expose machine data or secrets if introduced prematurely. Prefer static TOML first; do not commit credentials, private paths, hostnames, or local configuration values.
- Updating current docs without a delta to the main spec would leave contradictory requirements. The active change must explicitly modify or supersede Fedora-first requirements while preserving the archive.
- Adding package installation to this change would expand platform coupling and review scope beyond the 800-line budget; keep it as a later approved change.

### Ready for Proposal

Yes. The orchestrator should tell the user that the smallest safe boundary is an isolated, configuration-only chezmoi source state for Starship on macOS, with preview/idempotency/rollback and safety checks designed before implementation. The proposal must explicitly reconcile the Fedora-first README, architecture, decisions, and foundation specification while leaving the archived Fedora-first change untouched.
