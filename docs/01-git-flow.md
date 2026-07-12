# Git flow conventions

Use short-lived, purpose-specific branches and merge reviewed work into `main` through pull requests whenever possible. Branch names and commit messages are written in English so repository history remains consistent and easy to scan.

## Quick path

1. Start from an up-to-date `main` branch.
2. Create a branch named `<type>/<short-description>`.
3. Make coherent commits using Conventional Commits.
4. Open a small, focused pull request into `main`.

## Main branch

The stable primary branch is:

```text
main
```

`main` must contain reviewed, stable work. Avoid committing directly to it. Develop changes on purpose-specific branches and merge them through pull requests whenever possible.

## Branch naming

Use lowercase English words separated by hyphens:

```text
<type>/<short-description>
```

### Branch types

| Type | Use | Example |
| --- | --- | --- |
| `docs` | Documentation changes | `docs/product-vision` |
| `feature` | New product functionality | `feature/onboarding-flow` |
| `fix` | Bug fixes | `fix/training-status-calculation` |
| `refactor` | Internal improvements without behavior changes | `refactor/training-plan-service` |
| `test` | Test-only changes | `test/onboarding-validation` |
| `chore` | Maintenance tasks | `chore/update-dependencies` |

### Branch naming rules

- Use English words.
- Use lowercase letters.
- Use hyphens instead of spaces.
- Keep names short but descriptive.
- Prefer product or technical intent over vague labels.

Good examples:

```text
docs/product-vision
docs/user-journeys
feature/onboarding-flow
feature/training-dashboard
fix/plan-recalculation
```

Avoid:

```text
changes
new-stuff
test1
my-branch
final-version
```

## Commit messages

Follow the Conventional Commits format:

```text
<type>: <short summary>
```

### Commit types

| Type | Use | Example |
| --- | --- | --- |
| `docs` | Documentation changes | `docs: add product vision` |
| `feat` | New functionality | `feat: add onboarding flow` |
| `fix` | Bug fixes | `fix: correct plan recalculation` |
| `refactor` | Code restructuring without behavior changes | `refactor: simplify training plan builder` |
| `test` | Test changes | `test: add onboarding validation tests` |
| `chore` | Maintenance | `chore: update project dependencies` |

### Commit message rules

- Write commit messages in English.
- Use the imperative mood when possible.
- Keep the summary short and specific.
- Do not end the summary with a period.
- Keep each commit focused on one coherent change.

Good examples:

```text
docs: add product vision
docs: add git flow conventions
feat: add onboarding flow
fix: handle failed training sessions
refactor: extract training plan generator
```

Avoid:

```text
update
changes
fix stuff
final commit
more docs
```

## Documentation workflow

Documentation changes use `docs/<topic>` branches:

```text
docs/product-vision
docs/git-flow
docs/user-journeys
```

Give each document one clear purpose and avoid mixing unrelated topics. For example:

- Product vision belongs in `00-product-vision.md`.
- Git flow belongs in `01-git-flow.md`.
- User journeys belong in a separate file.

Use numeric prefixes such as `00`, `01`, and `02` to communicate documentation order when documents form a sequence.

## Pull request guidance

A pull request description should explain:

- What changed.
- Why it changed.
- Which files are most relevant for review.
- What is intentionally out of scope.

Documentation-only pull requests should remain small and focus on one document or one closely related topic.

## Convention summary

| Area | Convention |
| --- | --- |
| Main branch | `main` |
| Branch format | `<type>/<short-description>` |
| Branch language | English |
| Commit format | Conventional Commits |
| Commit language | English |
| Documentation order | Numeric prefixes such as `00`, `01`, and `02` |
