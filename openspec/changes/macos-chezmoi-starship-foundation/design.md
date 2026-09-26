# Design: macOS chezmoi and Starship foundation

## Decision

Deliver one small, reproducible macOS terminal slice: Homebrew supplies `chezmoi`, `starship`, and `font-meslo-lg-nerd-font`; chezmoi owns exactly the Starship and Ghostty configuration targets; a lifecycle command owns only one marked Starship block in `.zshrc`. Ghostty must be installed outside this workflow and is never installed or uninstalled by it. The workflow is **preview → explicit apply → verify**, with a separate rollback command for user-managed files. It is intentionally not a workstation provisioner, shell framework, application installer, or macOS-preferences manager.

The implementation remains a modular monolith: a small command boundary coordinates independent dependency, chezmoi, shell-integration, state, validation, and documentation responsibilities without introducing services, plugins, or a TUI.

## Quick path

1. Install Ghostty outside this workflow if it is not already available; this prerequisite is required for manual verification, not for safely managing its configuration file.
2. Run `scripts/macos-starship preview` to inspect prerequisites, allowed Homebrew dependencies, both intended targets, and the plan identifier without changing the machine.
3. Run `scripts/macos-starship apply --plan <plan-id>` only after accepting that exact preview. It installs missing approved Homebrew dependencies and applies the bounded Starship and Ghostty file changes.
4. Open Ghostty, start a new Zsh session, and visually confirm the prompt and glyphs using the managed Ghostty font configuration. Do not use Apple Terminal for this verification.
5. Run `scripts/macos-starship rollback` to restore file state when needed. Homebrew package removal remains an explicit, separately documented user action; Ghostty installation and removal always remain outside this workflow.

## Architecture and ownership

| Boundary | Responsibility | Explicit non-responsibility |
|---|---|---|
| Command coordinator | Parse `preview`, `apply`, and `rollback`; sequence preflight, plan validation, mutations, and reporting. | General machine setup or interactive navigation. |
| Homebrew adapter | Verify an existing usable `brew`; inspect approved formula/cask state; install only approved missing items. | Installing, repairing, updating, upgrading, or configuring Homebrew; installing or uninstalling Ghostty. |
| Chezmoi adapter | Dry-run and apply the nested source root; verify that its two resolved targets are allowlisted. | Managing the repository root, arbitrary home files, the Ghostty application, macOS preferences, or the `.zshrc` activation block. |
| Shell integration adapter | Add, replace in place, inspect, or remove the one delimited Starship block in `.zshrc`. | Taking ownership of `.zshrc`, reformatting it, or changing any user-authored line. |
| Local transaction state | Store private backups, creation records, hashes, and transaction status needed for rollback. | Committing user configuration or backups to the repository. |
| Validation and safety | Check target bounds, syntax, convergence, rollback, and public-repository safety. | Reading, logging, or scanning user shell content for secrets. |
| Documentation | Explain the bounded macOS workflow, external Ghostty prerequisite, manual Ghostty verification, and future module direction. | Claiming Linux/Windows, full shell ownership, Ghostty lifecycle management, or terminal UI/macOS-preference automation. |

The intended larger modular-monolith vocabulary remains `core`, `shell`, `terminal`, `multiplexer`, `monitoring`, `git`, `devtools`, and `profiles`. This slice implements a narrow part of **core** (safe orchestration), **shell** (Starship activation), and **terminal** (configuration-only Ghostty state). Manual rendering verification remains a human hand-off in externally installed Ghostty. The remaining modules are architectural direction, not delivered behavior.

## Repository and chezmoi source layout

The repository root is never a chezmoi source directory. A root `.chezmoiroot` points at a nested source root, preventing repository metadata, OpenSpec artifacts, scripts, and documentation from becoming accidental home-directory candidates.

```text
.chezmoiroot                         # selects the nested source only
chezmoi/
  dot_config/
    starship.toml                    # maps to ~/.config/starship.toml
    ghostty/
      config                         # maps to ~/.config/ghostty/config
scripts/
  macos-starship                     # command dispatcher; proposed implementation
  lib/                               # private command modules; proposed implementation
```

The only chezmoi-managed targets in this first slice are `.config/starship.toml` and `.config/ghostty/config`. Their sources are generic and contain no host-specific paths, credentials, or private values. The Ghostty file may select the approved Nerd Font, but it does not install Ghostty, mutate `.zshrc`, or change macOS preferences. The command passes the nested source root explicitly to chezmoi rather than relying on a caller's default chezmoi source directory.

`.zshrc` is deliberately outside the chezmoi source tree. Chezmoi owns the full content of a rendered target; using it for `.zshrc` would make a minimal integration indistinguishable from claiming ownership of a user-owned file.

Before `chezmoi apply`, the coordinator obtains a chezmoi dry-run and rejects the operation unless the resolved targets equal the documented two-target allowlist. A missing `chezmoi` cannot be installed during preview; in that case preview reports the static intended mapping and that a runtime chezmoi dry-run will be performed after dependency installation but before file mutation.

## Commands and data flow

### Preview: read-only planning

`macos-starship preview` performs, in order:

1. Confirm macOS and an existing usable Homebrew executable.
2. Detect the three approved Homebrew-managed dependencies and report each as present, missing, or conflicting; separately report whether externally managed Ghostty is available for later manual verification.
3. Inspect the two-target nested source mapping, `.zshrc` marker state, and rollback-state health without changing them.
4. Produce a canonical, non-secret plan: source revision, Homebrew dependency actions, two allowed target actions, shell-block action, Ghostty verification prerequisite status, and validation steps.
5. Print a stable `plan-id`, calculated from that canonical plan, plus any prerequisite or conflict that prevents apply.

Preview does not install packages, create backup directories, invoke a mutating chezmoi command, change files, alter shell state, or write a plan cache. Target labels use `$HOME`-relative paths; output must not contain the caller's absolute home path or configuration content.

### Apply: an explicit, bound mutation

`macos-starship apply --plan <plan-id>` is the only mutating workflow. It recomputes the plan immediately before any mutation and requires its identifier to equal the supplied identifier. A mismatch means the host, source, or target state changed after preview; apply exits without mutation and requires a new preview.

Once the plan is valid, apply:

1. Re-runs prerequisite and target-boundary checks.
2. Creates an in-progress local transaction record and backups before each existing target changes.
3. Installs only the missing approved Homebrew dependencies.
4. Runs chezmoi's real dry-run with the explicit nested source root, validates the two-target allowlist again, then applies the Starship and Ghostty configurations.
5. Applies the `.zshrc` marker operation.
6. Runs post-apply checks and records the managed hashes and a completed transaction only if all checks pass.

The plan is intentionally not persisted by preview. Persisting it would violate the non-destructive preview contract; recomputing and matching a plan identifier prevents a stale preview from authorizing changed inputs.

### Rollback: file-state recovery only

`macos-starship rollback` operates only on the latest completed or safely recoverable transaction in local state. It does not require a previous preview because it is a recovery operation, but it runs the same target-boundary and transaction-integrity checks before writing.

Rollback restores backed-up pre-existing Starship and Ghostty configurations, removes either configuration when it was created by apply, and removes only the managed `.zshrc` block. It does not uninstall `chezmoi`, Starship, the font, or Ghostty; run `brew uninstall`; modify Homebrew or macOS preferences; or remove unrelated files. Package removal is intentionally a separately documented, opt-in command sequence because packages may be shared with other workflows.

If a managed target no longer matches the last recorded managed hash, rollback stops before touching that target and reports drift. This fails safely rather than overwriting a user edit made after apply. A user can manually resolve the drift or restore the local backup after inspecting it. A failed or interrupted transaction remains recoverable through its recorded backups; a subsequent apply must not silently proceed over it.

## Homebrew and dependency policy

Homebrew is a hard prerequisite. The adapter verifies that `brew` is discoverable and can answer a harmless availability query such as its prefix/version. Failure produces an actionable message to install or repair Homebrew outside this workflow, then exits before package or file mutation.

The approved Homebrew-managed dependency set is fixed:

| Homebrew type | Identifier | Purpose |
|---|---|---|
| Formula | `chezmoi` | Render and apply the isolated source state. |
| Formula | `starship` | Provide prompt initialization and rendering. |
| Cask | `font-meslo-lg-nerd-font` | Provide a known Nerd Font for the manual Ghostty check. |

Ghostty is intentionally absent from this table. Its installation is a prerequisite outside the workflow for manual verification, and no Ghostty formula, cask, application, or removal command may reach the Homebrew adapter.

Detection uses Homebrew's installed formula/cask records, not only `PATH`, so the workflow can report provenance and stay idempotent. If a similarly named externally installed binary shadows or conflicts with the expected Homebrew dependency, preview reports a conflict and apply stops rather than installing a duplicate silently. The user resolves that conflict explicitly.

Apply invokes Homebrew only for missing entries in the table and avoids `brew update`, `brew upgrade`, taps, cleanup, Ghostty operations, or any unrelated package. Homebrew's automatic update behavior is disabled for these bounded install calls so the workflow cannot turn a prompt setup into a package-manager update. Existing approved dependencies produce a reported no-op.

## Starship, Ghostty, and `.zshrc` contract

Starship configuration ownership is narrow and complete: the nested chezmoi source owns `$HOME/.config/starship.toml` for this foundation. Ghostty configuration ownership is equally narrow: the same source owns `$HOME/.config/ghostty/config` and nothing about the Ghostty application lifecycle or macOS preferences. Before replacing either existing file, apply captures it in local transaction state. Both sources must remain portable and generic; host-specific prompt or terminal customization belongs to a future, explicitly designed profile mechanism.

The Ghostty target is configuration-only. It may select `MesloLGS Nerd Font Mono` — the family name installed by the approved font cask; the shorthand `MesloLGS NF` is not a resolvable family name — and other minimal settings required by this foundation, but it never installs, launches, updates, or uninstalls Ghostty; invokes `defaults`; edits an application bundle; or changes `.zshrc`. Ghostty must be installed separately before the user performs manual visual verification.

`.zshrc` remains user-owned. The shell adapter may own only this exact, documented block:

```zsh
# >>> jjdlr-dots macos-starship-foundation >>>
eval "$(starship init zsh)"
# <<< jjdlr-dots macos-starship-foundation <<<
```

Rules for the marker parser are deliberately strict:

- No complete block: append one canonical block while retaining every existing line in order.
- Exactly one complete block: retain it if canonical, or replace only its enclosed managed content if an older managed version requires an update.
- Duplicate, inverted, or unmatched markers: stop without editing `.zshrc`; the user must repair the ambiguity.
- Rollback removes exactly one complete block and nothing outside it. Missing or malformed markers are reported, not guessed.

The adapter uses atomic replacement for its edited target and preserves file permissions where the platform permits. It does not source `.zshrc`, execute user functions, evaluate arbitrary shell content, or print its contents.

## Backup, marker, and transaction strategy

Local state lives under `$HOME/.local/state/jjdlr-dots/macos-starship-foundation/` (or its explicit XDG state equivalent), never in the repository. The state directory uses owner-only permissions. Backups may contain personal configuration and therefore remain local, non-logged, and untracked.

A transaction contains a status (`in-progress`, `complete`, or `rollback-complete`), source revision, plan identifier, relative target names, whether each target existed, backup location when applicable, and cryptographic hashes of the post-apply managed targets. It never records target contents or absolute local paths in repository-facing logs.

For the first change to a target in an open transaction, apply creates a backup if it existed; otherwise it records an absence sentinel. Re-runs retain the original pre-apply backup instead of replacing it with managed state. This is what makes rollback restore the user's baseline rather than merely the previous run.

The transaction is marked `in-progress` before the first target mutation and is finalized only after post-apply verification. Interrupted or failed transactions are visible on the next invocation. The command reports the phase that failed and directs the user to inspect/rollback; it does not assume that partial mutation is safe to overwrite.

## Verification design

### Isolated HOME harness

Automated checks run with a disposable, isolated home directory. The harness sets `HOME`, `ZDOTDIR`, `XDG_CONFIG_HOME`, and `XDG_STATE_HOME` to subdirectories beneath that fixture root, prepends controlled tool shims to `PATH`, passes the nested chezmoi source explicitly, and cleans up through a trap. No test reads or writes the developer's real home, default chezmoi state, Ghostty application state outside the isolated config target, macOS preferences, or local backups.

The harness uses generic fixtures for pre-existing `.zshrc`, Starship configuration, and Ghostty configuration. Homebrew and chezmoi shims model missing, present, and failure responses without network access or real installation. Where installed tools are available, a separate opt-in integration check may exercise their read-only/dry-run behavior against the same isolated home; it must still not mutate the real workstation.

### Required automated evidence

| Check | Evidence |
|---|---|
| Preview safety | Preview makes no file, package, shell, preference, or state mutation and reports missing Homebrew/dependencies plus Ghostty's external verification-prerequisite status. |
| Dependency allowlist | Only the two formulas and one cask can reach the Homebrew adapter; Ghostty operations are forbidden; conflicts and Homebrew absence halt before mutation. |
| Isolated mapping | Chezmoi dry-run/apply candidates contain exactly `.config/starship.toml` and `.config/ghostty/config`; unrelated repository files and metadata never resolve as targets. |
| Ghostty boundary | Managing `.config/ghostty/config` performs no Ghostty install/uninstall, `.zshrc` change, application launch, or macOS-preference mutation. |
| Shell preservation | Fixture-authored `.zshrc` lines remain byte-for-byte in order outside the marker block; exactly one canonical block is added. |
| Syntax | The generated block and resulting fixture `.zshrc` pass `zsh -n` without sourcing user configuration. |
| Convergence | A second preview/apply reports no planned file or package change, performs no duplicate marker insertion, and leaves managed hashes unchanged. |
| Rollback | Existing Starship and Ghostty targets restore from baseline backups; created targets are removed; fixture user content survives; Homebrew packages and the Ghostty application are untouched. |
| Failure recovery | A simulated failure leaves an inspectable in-progress record and no later apply overwrites it automatically. |
| Safety | Scoped tracked repository inputs contain no prohibited secret/private-path patterns and no machine-specific fixture values. |

The convergence assertion is behavioral, not merely textual: it compares pre- and post-second-run target hashes, marker count, dependency adapter calls, and transaction baseline identity. This catches a script that emits “no-op” while still rewriting files or regenerating backups.

### Manual Ghostty verification

Prompt and glyph rendering are intentionally human verification steps. After apply reports the installed font cask and both managed targets, the documentation instructs the user to open an externally installed Ghostty, start a new Zsh session, and visually confirm that Starship glyphs render correctly with **MesloLGS Nerd Font Mono** (the family installed by the approved font cask) selected by the managed Ghostty configuration. Apple Terminal is not used for this verification.

The workflow does not install or launch Ghostty, call `defaults`, edit macOS or Apple Terminal preference files, manipulate terminal UI settings, or claim to verify pixels programmatically. A successful automated run proves dependency, configuration, and activation mechanics; it does not prove that Ghostty is installed or that visual glyph rendering succeeds. The final user-facing completion message must state that distinction clearly.

## Safety scanning and documentation reconciliation

A repository safety check scopes itself to tracked, change-relevant source, scripts, fixtures, documentation, and active OpenSpec files. It checks both filenames and content for private keys, credential/token patterns, private host details, and environment-specific absolute paths. It reports a file and rule category only, never the matching value. It must not scan `$HOME`, `.zshrc` content, local backups, or arbitrary untracked developer data.

Documentation is reconciled in the same change, with progressive disclosure and a consistent vocabulary:

- `README.md` presents the learning-oriented project, macOS-first verified status, the existing-Homebrew prerequisite, the delivered narrow foundation, and links to the supporting documents.
- `docs/architecture.md` distinguishes this implemented core/shell/configuration-only-terminal slice from planned modular-monolith modules and future platforms.
- `docs/decisions.md` records macOS-first sequencing, the existing-Homebrew constraint, the externally installed Ghostty prerequisite, nested two-target chezmoi isolation, marker ownership, preview/apply/rollback, manual Ghostty verification, and public-repository safety, including consequences and alternatives.
- The macOS workflow documentation gives copyable preview/apply/rollback commands, no-op expectations for both targets, manual Ghostty verification, drift recovery, separate Homebrew package-uninstall guidance, and the rule that Ghostty installation/removal is always outside this workflow.

Examples use `$HOME`, `~`, fixture paths, and generic names only. Archived SDD material is never edited. Documentation and checks should remain focused, but the added second-target coverage raises a material risk of exceeding the 800-line review budget. Implementation must be sliced before writing rather than compressing away target-boundary, rollback, safety, or Ghostty-prerequisite evidence.

## Failure handling and observability

Every command reports a phase-oriented result: `preflight`, `plan`, `backup`, `dependencies`, `chezmoi`, `shell-integration`, `verification`, or `rollback`. Human output identifies changed target labels and next safe action without emitting configuration contents, token-like values, private paths, or backup locations. A machine-readable mode may expose the same redacted status for tests and automation.

Exit behavior is deterministic: success includes both changed and already-converged outcomes; prerequisite/conflict/plan-drift failures occur before mutation; unsafe target/marker/transaction states fail closed; post-mutation failures retain the in-progress transaction and identify rollback as the recovery path. The command never masks a failed package, chezmoi, file, or verification step as success.

## Alternatives and tradeoffs

| Alternative | Why it is not selected | Consequence of the selected design |
|---|---|---|
| Make the repository root the chezmoi source | It can map documentation, scripts, metadata, or future files into `$HOME` by accident. | A nested source adds one indirection but creates a reviewable allowlist boundary. |
| Let chezmoi manage the whole `.zshrc` | It would replace or merge user-owned shell state and violate the preservation requirement. | The marker adapter is bespoke but has a tiny, auditable ownership surface. |
| Apply immediately after dependency detection | It blurs inspection and mutation and makes stale assumptions hard to see. | A plan identifier adds one explicit command argument and protects against source/host drift. |
| Install Ghostty as another Homebrew dependency | The confirmed scope is configuration-only and must not take ownership of the terminal application's lifecycle. | Ghostty must be installed externally before manual verification, while configuration apply remains safe when it is absent. |
| Automatically change macOS or Apple Terminal preferences | Terminal and OS preferences are personal, UI-owned state and difficult to roll back safely. | Ghostty uses its managed file configuration, and the final glyph check is manual and clearly documented. |
| Uninstall packages during rollback | Packages can be used outside this foundation; removing them is not a safe inverse of file application. | Rollback is predictable for files; package removal is an explicit user choice. |
| Build a full workstation provisioner | Cross-platform support, Homebrew bootstrapping, broad tools, secrets, profiles, and shell ownership create a much larger trust and rollback surface. | This slice establishes repeatable boundaries before later modules are considered. |
| Build a Gentleman.Dots-style TUI | A TUI adds stateful navigation, broader product decisions, and a UI testing burden before the command contracts are proven. | Simple commands are scriptable, testable in isolation, and educational about the underlying tools. |

The selected design favors boring, inspectable operations over immediacy. It teaches the distinction between declarative dotfile ownership (chezmoi), narrowly scoped integration (`.zshrc` markers), externally owned application installation, and human-owned visual verification. That foundation can support future modules without pretending that they already exist.

## Review checklist

- [ ] The nested chezmoi source maps only `.config/starship.toml` and `.config/ghostty/config`.
- [ ] Preview is non-destructive, reports the external Ghostty verification prerequisite, and apply requires its matching plan identifier.
- [ ] Homebrew is required but never installed, repaired, updated, or broadly modified.
- [ ] Only `chezmoi`, `starship`, and `font-meslo-lg-nerd-font` are candidates for installation; Ghostty is never installed or uninstalled.
- [ ] `.zshrc` retains user content and contains at most one documented managed block; the Ghostty target introduces no `.zshrc` change.
- [ ] Backups and transaction records stay local, private, and sufficient for safe rollback of both configuration targets.
- [ ] Isolated-home checks prove two-target mapping, preservation, syntax, convergence, rollback, Ghostty lifecycle exclusion, and failures.
- [ ] Manual verification is performed in Ghostty, not Apple Terminal, without macOS preference changes.
- [ ] Repository scanning and documentation use generic, public-safe values.
- [ ] The implementation remains a small macOS-first foundation, not a provisioner or TUI.

## Next phase

Translate this design and both approved specifications into implementation tasks. Keep each task within the stated ownership boundaries and review budget.
