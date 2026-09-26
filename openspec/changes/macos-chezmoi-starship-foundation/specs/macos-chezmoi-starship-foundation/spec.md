# macOS chezmoi and Starship Foundation Specification

## Purpose

Define a safe, macOS-first foundation that installs the approved prompt dependencies, applies isolated Starship and Ghostty configuration through chezmoi, and activates Starship without taking ownership of an existing shell configuration or managing the Ghostty application.

## Requirements

### Requirement: Preview precedes workstation mutation

The workflow MUST provide a preview that reports the planned dependency, source-state, two-target, shell-activation, and external Ghostty-prerequisite state before any workstation mutation. Applying changes MUST require an explicit operation after preview.

#### Scenario: Preview is non-destructive

- GIVEN a macOS host with Homebrew and an existing home directory
- WHEN the user requests a preview
- THEN the workflow reports the planned changes and any unmet prerequisite
- AND it does not install packages, modify files, or alter the active shell

#### Scenario: Apply follows an approved preview

- GIVEN a preview has completed successfully
- WHEN the user explicitly runs the apply operation
- THEN only the changes described by the applicable preview are performed
- AND the workflow reports the resulting targets and activation state

### Requirement: Existing Homebrew is a prerequisite

The workflow MUST require an existing, usable Homebrew installation and MUST NOT install, modify, or repair Homebrew. When Homebrew is unavailable, the workflow MUST stop before mutation and provide an actionable prerequisite message.

#### Scenario: Homebrew is missing

- GIVEN Homebrew is not available
- WHEN the user requests preview or apply
- THEN the workflow reports that Homebrew is required
- AND it performs no package or file mutation

### Requirement: Approved Homebrew dependencies are installed idempotently

The workflow MUST manage only chezmoi, Starship, and one Nerd Font through the existing Homebrew installation. It MUST avoid duplicate or unnecessary changes when those dependencies already satisfy the requirement. Ghostty is not part of this Homebrew allowlist and MUST NOT be installed or uninstalled by the workflow.

#### Scenario: Missing approved dependencies are installed

- GIVEN Homebrew is available and one or more approved dependencies are absent
- WHEN the user applies the workflow
- THEN the missing chezmoi, Starship, and/or selected Nerd Font dependency is installed
- AND no unapproved package or font is installed

#### Scenario: Dependencies are already present

- GIVEN the approved dependencies are already available
- WHEN the user applies the workflow again
- THEN dependency state remains unchanged
- AND the workflow reports no unnecessary installation

#### Scenario: Ghostty is outside dependency management

- GIVEN Ghostty is installed, absent, or installed by any external mechanism
- WHEN the user previews, applies, or rolls back the workflow
- THEN no Ghostty install or uninstall operation is planned or performed
- AND the workflow identifies Ghostty installation as an external prerequisite for manual verification

### Requirement: Ghostty installation is an external verification prerequisite

The workflow MUST document that Ghostty must be installed outside this workflow before manual verification. Ghostty absence MUST NOT expand package-management scope, and it MUST NOT prevent previewing or applying the configuration-only target.

#### Scenario: Ghostty is absent during configuration apply

- GIVEN Ghostty is not installed
- WHEN the user previews or applies the workflow
- THEN the workflow reports that manual verification remains unavailable until Ghostty is installed externally
- AND it may still safely manage `~/.config/ghostty/config`
- AND it does not install Ghostty

### Requirement: Chezmoi state is isolated from repository files

The workflow MUST map only the intended nested chezmoi source state to the user's home directory. It MUST NOT accidentally map repository metadata, unrelated files, local paths, or arbitrary repository content into the home directory.

#### Scenario: Preview shows isolated mapping

- GIVEN the repository contains the intended chezmoi source and unrelated repository files
- WHEN the user previews application
- THEN the preview lists only intended home targets
- AND no repository metadata, unrelated file, or local absolute path is selected as a home target

#### Scenario: Applied targets remain bounded

- GIVEN the user applies the workflow
- WHEN the resulting home targets are inspected
- THEN every managed target belongs to the documented macOS Starship and Ghostty foundation scope
- AND repository files outside that scope remain unmapped

### Requirement: Chezmoi manages exactly two configuration targets

The nested chezmoi source MUST manage only `~/.config/starship.toml` and `~/.config/ghostty/config`. The Ghostty target MUST be treated as configuration data only and MUST NOT authorize application installation, shell-file changes, or macOS preference changes.

#### Scenario: Preview lists both allowlisted targets

- GIVEN the nested source contains the approved Starship and Ghostty configuration files
- WHEN the user previews application
- THEN the preview lists exactly `~/.config/starship.toml` and `~/.config/ghostty/config`
- AND no additional home target is selected

#### Scenario: Ghostty configuration is applied without unrelated mutation

- GIVEN the two-target preview has been approved
- WHEN the user applies the workflow
- THEN chezmoi manages `~/.config/ghostty/config` together with `~/.config/starship.toml`
- AND the Ghostty target causes no Ghostty install or uninstall, no `.zshrc` mutation, and no macOS preference change

### Requirement: Existing `.zshrc` content is preserved

The workflow MUST preserve all pre-existing `.zshrc` content and MUST add, rather than replace, the Starship activation integration. Adding the Ghostty configuration target MUST NOT add any further `.zshrc` change.

#### Scenario: Existing configuration survives apply

- GIVEN `.zshrc` contains user-authored content before apply
- WHEN the user applies the workflow
- THEN the original content remains intact and in its original order
- AND Starship activation is added without replacing unrelated configuration

### Requirement: Activation uses a unique reversible boundary

The workflow MUST place Starship initialization inside one uniquely identifiable, documented delimiter block. Repeated application MUST update or retain that block rather than create duplicates, and rollback MUST remove only that block.

#### Scenario: First activation creates one block

- GIVEN `.zshrc` does not contain the foundation activation block
- WHEN the user applies the workflow
- THEN exactly one complete delimited Starship activation block is present
- AND the block is distinguishable from user-authored content

#### Scenario: Existing activation block is not duplicated

- GIVEN `.zshrc` already contains the foundation activation block
- WHEN the user applies the workflow again
- THEN exactly one block remains
- AND unrelated `.zshrc` content is unchanged

#### Scenario: Rollback removes only managed activation

- GIVEN `.zshrc` contains user content and the foundation activation block
- WHEN the user runs the documented rollback
- THEN the activation block is removed
- AND all other `.zshrc` content remains intact

### Requirement: Apply supports backup and rollback

Before changing either existing chezmoi-managed target or the managed Starship activation block, the workflow MUST create or retain a recoverable backup and MUST provide a rollback operation that restores the prior state or removes only newly introduced managed state. Homebrew package uninstallation MUST remain separate from rollback, and Ghostty MUST never be uninstalled by rollback.

#### Scenario: Existing targets can be restored

- GIVEN a managed target exists before apply
- WHEN apply changes that target and the user requests rollback
- THEN the pre-apply target content is restored
- AND the workflow reports the rollback result

#### Scenario: Newly created targets can be removed

- GIVEN a managed target did not exist before apply
- WHEN the user requests rollback
- THEN that newly introduced managed target is removed
- AND unrelated files are not removed

### Requirement: A second run is a no-op

After a successful apply with no relevant environment or source change, a second preview/apply cycle MUST report no unintended changes, MUST not duplicate activation, and MUST leave both managed configuration targets and existing user content unchanged.

#### Scenario: Repeated application converges

- GIVEN the first apply completed successfully and the source and host prerequisites are unchanged
- WHEN the user performs a second apply
- THEN the workflow reports a no-op or equivalent converged state
- AND file content, activation boundaries, and dependency state remain unchanged

### Requirement: Ghostty verification remains manual

The workflow MUST document manual prompt and glyph verification in Ghostty and MUST NOT modify macOS preferences or automate terminal UI settings. The managed `~/.config/ghostty/config` MAY declare the approved Nerd Font using Ghostty's file-based configuration, but the workflow MUST NOT claim visual success until the user opens Ghostty and checks a new Zsh session.

#### Scenario: User completes manual Ghostty verification

- GIVEN Ghostty was installed outside the workflow, the approved Nerd Font is installed, and both managed configuration targets were applied
- WHEN the user opens Ghostty and starts a new Zsh session
- THEN the user can verify that Starship renders with the configured font's glyph support
- AND no macOS preference or terminal UI setting was changed by the workflow itself

### Requirement: Documentation and safety checks match macOS-first behavior

The delivered documentation and acceptance checks MUST describe macOS as the first verified platform, Homebrew as an existing prerequisite, Ghostty installation as an external manual-verification prerequisite, the two-target scope boundaries, preview/apply/rollback behavior, and manual verification in Ghostty. Repository artifacts MUST contain no credentials, machine-specific secrets, private host data, or environment-specific absolute paths.

#### Scenario: Documentation agrees with delivered behavior

- GIVEN a reader reviews the README, active documentation, and specifications
- WHEN they compare the documented workflow with the foundation behavior
- THEN the documentation consistently presents the macOS-first scope and its boundaries
- AND it does not claim Homebrew or Ghostty installation, full `.zshrc` ownership, macOS-preference or terminal-UI automation, support for terminal emulators beyond the configuration-only Ghostty target, or cross-platform support

#### Scenario: Public-repository safety holds

- GIVEN the repository is checked before review
- WHEN source, documentation, fixtures, and generated examples are inspected
- THEN no credential, private host detail, machine-specific secret, or environment-specific absolute path is committed
- AND examples use generic, reproducible paths and values
