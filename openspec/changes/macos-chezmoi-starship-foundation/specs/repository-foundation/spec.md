# Delta for Repository Foundation

## MODIFIED Requirements

### Requirement: Project entry point communicates current status and direction

`README.md` MUST provide a concise, scan-friendly entry point that states the project's learning-oriented purpose, identifies macOS as the first verified platform, summarizes the currently implemented chezmoi/Starship foundation, and distinguishes delivered capability from future platform and tooling scope.

(Previously: The entry point described a documentation-only, Fedora-first project and presented the tool ecosystem as roadmap context.)

#### Scenario: New reader understands the current boundary

- GIVEN a reader opens `README.md` without access to private project context
- WHEN they review the project overview and workflow
- THEN they can identify the macOS-first purpose, the implemented foundation, the existing Homebrew prerequisite, and the remaining future scope
- AND unsupported platforms, Homebrew installation, full shell ownership, and unrelated tools are not presented as delivered behavior

#### Scenario: Reader can navigate the foundation documents

- GIVEN the repository contains the foundation documentation
- WHEN a reader follows the README documentation links
- THEN they can reach the architecture, decision, and macOS workflow documentation
- AND the links describe each document's role accurately

### Requirement: Intended modular-monolith boundaries are documented

`docs/architecture.md` MUST describe the intended modular-monolith direction and responsibilities of `core`, `shell`, `terminal`, `multiplexer`, `monitoring`, `git`, `devtools`, and `profiles`, while identifying the macOS chezmoi/Starship foundation as the first implemented slice and preserving explicit ownership boundaries.

(Previously: The architecture described all platform and tooling work as future direction, including Fedora-first sequencing.)

#### Scenario: Reader distinguishes implemented and planned responsibilities

- GIVEN a reader reviews the architecture document
- WHEN they inspect module responsibilities and the first slice
- THEN each named module has a clear, non-overlapping intended responsibility
- AND the document distinguishes the implemented macOS foundation from planned modules and capabilities

#### Scenario: Platform sequencing is understandable

- GIVEN a reader reviews the architecture document
- WHEN they inspect platform and tooling decisions
- THEN macOS-first delivery, existing Homebrew, chezmoi, and Starship are explained as the current verified foundation
- AND Linux and Windows are identified as future scope rather than current behavior

### Requirement: Initial decisions and tradeoffs are discoverable

`docs/decisions.md` MUST record the decisions for macOS-first delivery, existing-Homebrew prerequisite handling, isolated chezmoi mapping, minimal reversible `.zshrc` activation, preview-before-mutation, rollback, public-repository secret safety, and the boundaries of manual Apple Terminal font selection, including rationale, alternatives, and consequences suitable for future review.

(Previously: The decisions centered on documentation-first delivery and Fedora-first sequencing before executable workstation behavior existed.)

#### Scenario: Contributor understands the foundation tradeoffs

- GIVEN a contributor reads the decision overview
- WHEN they review the initial decision records
- THEN they can understand why the first slice is macOS-first and why it avoids Homebrew installation, full `.zshrc` ownership, and broad tool automation
- AND they can identify the tradeoff between safe incremental automation and immediate full workstation ownership

#### Scenario: Secret safety is explicit

- GIVEN a contributor prepares or reviews repository documentation or fixtures
- WHEN they consult the decision overview
- THEN it states that credentials, private host details, employer information, machine-specific secrets, and environment-specific absolute paths MUST NOT be committed
- AND examples remain generic and safe for a public repository

### Requirement: Desired repository layout is documented without accidental ownership

The foundation documentation MUST show the intended repository layout and explain the purpose of its major areas, including the isolated chezmoi source and validation scripts, without implying ownership of unrelated home-directory state or requiring unsupported platform scaffolding.

(Previously: The layout was illustrative and explicitly deferred all implementation scaffolding.)

#### Scenario: Layout communicates delivered and planned scope

- GIVEN a reader reviews the documented layout
- WHEN they compare it with the repository contents and managed targets
- THEN delivered macOS foundation areas are distinguishable from planned areas
- AND the layout does not imply that unrelated repository files or the complete `.zshrc` are managed

### Requirement: Foundation behavior is implemented within the approved macOS boundary

This change MAY introduce the approved macOS foundation behavior, including preview-first workflow, existing-Homebrew dependency handling, isolated chezmoi state, Starship configuration, minimal delimited `.zshrc` activation, backup, rollback, and validation checks. It MUST NOT install Homebrew, broaden to Linux or Windows, take full `.zshrc` ownership, modify Apple Terminal preferences automatically, add unrelated tools, or introduce secrets or private machine data.

(Previously: The change was documentation-only and prohibited all installer scripts, package installation, managed dotfiles, shell configuration, and platform implementations.)

#### Scenario: Review finds only bounded macOS behavior

- GIVEN the change is reviewed before delivery
- WHEN its files, documented scope, and managed targets are inspected
- THEN the executable behavior is limited to the approved macOS chezmoi/Starship foundation
- AND Homebrew installation, cross-platform behavior, unrelated packages, full shell ownership, and automatic terminal preference changes remain explicitly excluded

### Requirement: Foundation documentation and checks are reviewable and safe

The foundation documents and checks MUST be written in English, use clear headings and progressive disclosure, remain concise enough for the 800-line review budget, reconcile with the macOS-first behavior, and contain no secrets or private machine data.

(Previously: Documentation was constrained to a 500-line documentation-only review and Fedora-first status.)

#### Scenario: Documentation passes repository review

- GIVEN a reviewer reads the changed documentation and specifications
- WHEN they check language, consistency, scope, examples, and safety
- THEN the content is easy to scan, internally consistent, and educational
- AND it accurately describes preview, apply, no-op re-run, backup, rollback, manual font selection, and safety boundaries without exposing private data
