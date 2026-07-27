# Maintainer Setup

Complete these one-time GitHub settings after uploading the repository.

## Repository settings

1. Keep the default branch named `main`.
2. Enable **Issues**.
3. Enable **Discussions** if you want a place for questions and ideas that are
   not yet actionable issues.
4. Enable **Private vulnerability reporting** under the Security settings.
5. Add repository topics such as:

   ```text
   python
   physics
   education
   mechanics
   stem
   dark-mode
   beginner-friendly
   ```

## Labels

GitHub creates `bug`, `enhancement`, `good first issue` and `help wanted` by
default. Add these extra labels:

| Label | Purpose |
| --- | --- |
| `documentation` | README, guides and explanations |
| `tests` | Automated test improvements |
| `accessibility` | Keyboard, contrast and assistive technology |
| `physics-review` | Requires equation or unit verification |
| `needs-triage` | Maintainer has not reviewed the issue |

Create several tasks from [Contributor Task Ideas](CONTRIBUTOR_TASKS.md), then
apply `good first issue` or `help wanted`.

## Protect the main branch

Create a branch ruleset for `main`:

- require changes through pull requests;
- require at least one approval;
- require all automated tests to pass;
- dismiss stale approvals when new commits are added;
- require conversations to be resolved; and
- block force pushes and branch deletion.

The maintainer can still close unsuitable pull requests without merging them.

## Ownership

Create `.github/CODEOWNERS` after confirming your exact GitHub username:

```text
* @YOUR-GITHUB-USERNAME
```

This automatically requests your review on pull requests. Do not leave the
placeholder unchanged.

## First public contribution tasks

Publish at least three small, well-scoped issues before promoting the
repository. Contributors are more likely to act when the work is already
defined and acceptance criteria are clear.

For each issue:

1. explain the learner-facing problem;
2. identify likely files;
3. give acceptance criteria;
4. add the correct labels; and
5. state that the issue is available for assignment.
