# Contributing

Thank you for your interest in improving Dinglo Physics Solver.

This is a proprietary project. Before preparing a contribution, open a
discussion or contact the project owner to confirm that the proposed change is
appropriate.

## Development workflow

1. Fork the repository after receiving permission.
2. Create a focused branch for one change.
3. Preserve the existing Dinglo design system.
4. Add or update tests for calculation changes.
5. Run the full test suite:

   ```bash
   python -m unittest discover -s tests -v
   ```

6. Explain the physics reasoning and user-facing impact in the pull request.

## Code expectations

- Use Python 3.10-compatible syntax.
- Keep calculation functions independent and testable.
- Validate division-by-zero cases and invalid physical values.
- Preserve SI units in labels and results.
- Avoid adding dependencies unless they provide a clear benefit.
- Never commit secrets, API keys or environment files.
