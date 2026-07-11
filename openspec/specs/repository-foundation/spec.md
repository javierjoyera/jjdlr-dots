# Repository Foundation Specification

## Purpose

Define the documentation-only foundation that makes `jjdlr-dots` understandable, accurately bounded, and ready for later implementation milestones without creating executable workstation behavior.

## Requirements

### Requirement: Project entry point communicates current status and direction

`README.md` MUST provide a concise, scan-friendly entry point that states the project's learning-oriented purpose, identifies Fedora Linux as the first supported platform, summarizes the planned tool ecosystem as roadmap context, and distinguishes current documentation from future capability.

#### Scenario: New reader understands the project boundary

- GIVEN a reader opens `README.md` without access to private project context
- WHEN they review the project overview and roadmap
- THEN they can identify the purpose, documentation-only status, Fedora-first direction, planned tools, and next milestone
- AND planned tools and platforms are not presented as installed, configured, or currently supported

#### Scenario: Reader can navigate the foundation documents

- GIVEN the repository contains the foundation documentation
- WHEN a reader follows the README documentation links
- THEN they can reach the architecture and decision documentation
- AND the links describe the role of each document accurately

### Requirement: Intended modular-monolith boundaries are documented

`docs/architecture.md` MUST describe the intended modular-monolith direction and the responsibilities of `core`, `shell`, `terminal`, `multiplexer`, `monitoring`, `git`, `devtools`, and `profiles`.

#### Scenario: Reader can distinguish module responsibilities

- GIVEN a reader reviews the architecture document
- WHEN they inspect the module responsibility overview
- THEN each named module has a clear, non-overlapping intended responsibility
- AND the document states that these boundaries describe planned architecture rather than implemented modules

#### Scenario: Platform sequencing is understandable

- GIVEN a reader reviews the architecture document
- WHEN they inspect platform and tooling decisions
- THEN Fedora-first delivery and `chezmoi` are explained as current direction with rationale
- AND Windows, WSL, and macOS are identified as future scope rather than current behavior

### Requirement: Initial decisions and tradeoffs are discoverable

`docs/decisions.md` MUST record the initial decisions for documentation-first delivery, Fedora-first sequencing, modular boundaries, public-repository secret safety, and a practical-but-polished product tone, including rationale, relevant alternatives, and consequences at a level suitable for future review.

#### Scenario: Contributor can understand why the foundation is documentation-only

- GIVEN a contributor reads the decision overview
- WHEN they review the initial decision records
- THEN they can understand why executable installers and configuration are deferred
- AND they can identify the tradeoff between learning and immediate automation

#### Scenario: Secret safety is explicit

- GIVEN a contributor prepares or reviews repository documentation
- WHEN they consult the decision overview
- THEN it states that credentials, private host details, employer information, and machine-specific secrets MUST NOT be committed
- AND examples remain generic and safe for a public repository

### Requirement: Desired repository layout is documented without premature scaffolding

The foundation documentation MUST show the intended future repository layout and explain the purpose of its major areas without requiring empty module, profile, platform, or configuration directories to be created in this change.

#### Scenario: Layout communicates intent without implying implementation

- GIVEN a reader reviews the documented layout
- WHEN they compare it with the repository contents
- THEN the layout is clearly labeled as planned or illustrative
- AND absent implementation directories are not represented as delivered capability

### Requirement: Scope remains documentation-only

This change MUST modify only repository-facing documentation and MUST NOT introduce installer scripts, package installation, operating-system automation, managed dotfiles, shell or tool configuration, platform implementations, a custom CLI, a `doctor` command, or test-runner selection.

#### Scenario: Review finds no executable workstation behavior

- GIVEN the change is reviewed before implementation milestones begin
- WHEN its changed files and documented scope are inspected
- THEN no executable behavior, user configuration, package state, or workstation state is changed
- AND Fedora installer work, tool configuration, cross-platform implementation, CLI work, and environment validation remain explicitly deferred

### Requirement: Foundation documentation is reviewable and safe

The foundation documents MUST be written in English, use clear headings and progressive disclosure, remain concise enough for the 500-line review budget, and contain no secrets or private machine data.

#### Scenario: Documentation passes repository review

- GIVEN a reviewer reads the changed documentation
- WHEN they check language, consistency, scope, and examples
- THEN the content is easy to scan, internally consistent, and educational
- AND it contains no credentials, private identifiers, or machine-specific data
