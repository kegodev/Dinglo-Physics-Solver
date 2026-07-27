# Physics Contribution Guide

Calculation changes require more than code that produces a plausible number.
They must be physically correct, clear to learners and testable.

## Adding an equation

Document:

1. the standard equation;
2. every symbol and SI unit;
3. assumptions and limitations;
4. valid and invalid input ranges;
5. sign conventions;
6. every supported rearrangement; and
7. at least one verified example.

## Numerical behaviour

- Use SI units internally.
- Avoid rounding intermediate values.
- Round only the displayed result.
- Reject undefined divisions.
- Reject inputs that make a real-valued answer impossible.
- Allow negative vector components when they represent direction.

## Required tests

For a new calculator, include:

- the direct form of the equation;
- each inverse form;
- zero and boundary cases;
- a negative-direction case when relevant;
- invalid-input errors; and
- one result verified independently.

## Learner-facing working

Every solution should display:

1. the formula;
2. the rearranged formula when necessary;
3. substituted numerical values with units; and
4. the final answer with its SI unit.

Use conventional symbols and language that a learner can reproduce in an
assignment or examination.
