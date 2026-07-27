# Contributing to Dinglo Physics Solver

Thank you for helping make physics easier to learn. Contributions of code,
tests, documentation, accessibility improvements and new physics solvers are
welcome.

You do not need prior permission to work on an open issue. For a large change,
open a feature request first so the approach can be discussed before you invest
significant time.

By contributing, you agree that your contribution will be licensed under the
project's [MIT License](LICENSE).

## Find something to work on

Start with the repository's Issues tab:

- `good first issue` — small, clearly scoped tasks for new contributors;
- `help wanted` — tasks where community assistance is especially welcome;
- `bug` — confirmed behaviour that needs correction;
- `enhancement` — approved improvements or new features; and
- `documentation` — writing and explanation improvements.

If no issue matches your idea, create one using the appropriate issue form.

## Development setup

1. Fork the repository on GitHub.
2. Clone your fork:

   ```bash
   git clone https://github.com/YOUR-USERNAME/Dinglo-Physics-Solver.git
   cd Dinglo-Physics-Solver
   ```

3. Create a focused branch:

   ```bash
   git checkout -b feature/short-description
   ```

4. Start the application:

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000`.

No third-party Python packages are required.

## Branch and commit names

Use a short branch prefix:

- `feature/` for new functionality;
- `fix/` for bug fixes;
- `docs/` for documentation;
- `test/` for tests; or
- `refactor/` for internal improvements.

Write commit messages in the imperative mood:

```text
Add power calculator
Fix negative velocity validation
Improve mobile focus states
```

## Code expectations

- Support Python 3.10 and newer.
- Keep calculation functions independent and testable.
- Show the formula, substitution and final answer.
- Preserve SI units in inputs and results.
- Treat direction consistently by allowing signed vectors where appropriate.
- Validate division by zero and physically invalid inputs.
- Maintain keyboard accessibility and both colour themes.
- Avoid dependencies unless the benefit clearly justifies them.
- Never commit secrets, API keys or `.env` files.

Read [Physics Contribution Guide](docs/PHYSICS_CONTRIBUTION_GUIDE.md) before
adding or changing a formula.

## Tests

Run the entire suite before opening a pull request:

```bash
python -m unittest discover -s tests -v
```

Add tests whenever you:

- introduce a new equation;
- support solving for another variable;
- fix a calculation bug;
- change input validation; or
- alter theme or interface behaviour.

All automated checks must pass before a pull request can be merged.

## Opening a pull request

1. Push your branch to your fork.
2. Open a pull request against the main repository's `main` branch.
3. Link the issue using `Closes #123`.
4. Complete every relevant section of the pull-request template.
5. Include screenshots for visible interface changes.
6. Explain how you verified the physics.
7. Respond to review comments and update the same branch.

Keep one pull request focused on one issue. Unrelated changes may be requested
as a separate pull request.

## Review process

The maintainer will check:

- correctness of the physics;
- clarity of the learning steps;
- automated tests;
- mobile, light-mode and dark-mode behaviour;
- accessibility; and
- whether the change fits Dinglo's educational purpose.

Approval is not guaranteed, but every respectful contribution will receive
clear feedback when maintainer capacity allows.

## Community standards

All participation must follow the [Code of Conduct](CODE_OF_CONDUCT.md).
Security problems must be reported according to [SECURITY.md](SECURITY.md),
not through a public issue.
