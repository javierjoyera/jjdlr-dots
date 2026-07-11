# Explore: bootstrap-repo-foundation

## Summary

The repository is at the beginning of the `jjdlr-dots` SDD flow. Project context has been initialized from `.context/objetivo.md`, and the first useful change should establish a small repository foundation for future Fedora-first dotfiles work.

## Current state

- `openspec/config.yaml` and `openspec/project-context.md` exist.
- The repository has no executable implementation yet.
- `README.md` and `docs/` are present but foundational documentation is not yet established.
- No package manifest, dependency manager, automated test runner, installer, or module implementation exists.
- Git is initialized, but several files are still untracked.

## Recommended first change

Change name: `bootstrap-repo-foundation`

Scope the first proposal to:

- a clear initial README;
- foundational architecture documentation;
- minimal repository structure for the modular monolith;
- explicit Fedora-first boundaries;
- documentation of deferred Windows, macOS, installer, CLI, and full tool configuration work.

## Out of scope for the first change

- Implementing the Fedora installer.
- Installing packages.
- Writing real shell/terminal/Zellij/Starship configuration.
- Adding Windows or macOS behavior.
- Creating a custom CLI or `doctor` command.

## Risks and notes

- Strict TDD is enabled, but no test runner exists yet. The first executable change must introduce appropriate verification.
- The project should stay learning-focused: generated structure and docs must explain intent instead of hiding decisions behind opaque scripts.
- The public repository must avoid secrets and private machine-specific data.
