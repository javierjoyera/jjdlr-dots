# Foundation decisions

These lightweight records explain the **Current** documentation foundation and the **Planned** direction. They do not claim that the described automation or configuration exists.

## D-001 — Document before automating

- **Status:** Accepted
- **Decision:** Establish the README, architecture boundaries, and tradeoffs before executable work.
- **Rationale:** A small, explainable foundation gives contributors a shared model and keeps the first milestone reviewable.
- **Alternatives:** Start with an installer or copy configuration first.
- **Consequences:** Automation and working dotfiles are deferred; learning and clarity take precedence over immediate setup.
- **Reconsider when:** A separately approved executable milestone has defined behavior and verification.

## D-002 — Sequence Fedora first

- **Status:** Accepted
- **Decision:** Plan Fedora Linux as the first implementation target.
- **Rationale:** One platform gives the project a practical path for learning before portability is generalized.
- **Alternatives:** Implement Fedora, Windows/WSL, and macOS together; or defer a platform choice.
- **Consequences:** Windows/WSL and macOS are **Future** scope, not current support.
- **Reconsider when:** Fedora implementation exposes requirements that need a different order, or another platform is approved.

## D-003 — Keep one modular monolith

- **Status:** Accepted
- **Decision:** Use one repository with lightweight ownership contexts; profiles compose contexts while modules retain ownership.
- **Rationale:** Explicit boundaries prevent unrelated configuration from accumulating in shared scripts without imposing distributed systems or formal DDD machinery.
- **Alternatives:** One undifferentiated configuration collection, independent repositories, or formal DDD mechanisms now.
- **Consequences:** Each configuration item has one owner; `core` is foundational; feature contexts do not depend on profiles. The full model lives in [architecture](architecture.md).
- **Reconsider when:** Real implementation demonstrates a necessary coupling or a boundary is consistently unclear.

## D-004 — Treat chezmoi as direction, not capability

- **Status:** Accepted
- **Decision:** Keep `chezmoi` as the intended future source-state and dotfile application direction.
- **Rationale:** It can support reproducible management and templating without committing this foundation to a concrete setup.
- **Alternatives:** Configure it immediately, select another manager now, or postpone any stated direction.
- **Consequences:** No `chezmoi` source state, managed dotfiles, or application workflow exists in this milestone.
- **Reconsider when:** The first executable design defines its interaction with bootstrap and package work.

## D-005 — Make public safety a design constraint

- **Status:** Accepted
- **Decision:** Never commit credentials, private host details, employer information, or machine-specific secrets; examples remain generic.
- **Rationale:** The repository is public and documentation should be safe to share and review.
- **Alternatives:** Store private values alongside configuration or rely on informal reviewer memory.
- **Consequences:** Contributors must remove sensitive data before committing. Secret detection or enforcement is future executable-work design, not tooling added now.
- **Reconsider when:** A later approved change selects a safe secret-management and validation approach.

## D-006 — Prefer practical polish

- **Status:** Accepted
- **Decision:** Favor clarity, productivity, navigation, and concise explanations over decorative complexity.
- **Rationale:** A polished but practical experience helps learners and reviewers verify intent quickly.
- **Alternatives:** A visually dense showcase or minimal notes without explanation.
- **Consequences:** Documentation uses clear headings, tables, and links; it avoids unsupported badges, screenshots, and claims.
- **Reconsider when:** Reader feedback shows that the documentation is no longer easy to scan.

## Deferred work

This foundation intentionally defers installers, package and tool configuration, cross-platform implementation, a CLI or `doctor` command, and test-runner selection. Those decisions require their own approved change and implementation evidence.
