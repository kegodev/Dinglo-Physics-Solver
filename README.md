# Dinglo Physics Solver

A polished Python web application that solves introductory mechanics problems
from the variables supplied by the learner. It covers Newton's laws, momentum,
projectile motion, work and energy while showing the formula, substitution and
final answer.

## About the project

Dinglo Physics Solver is designed for learners who know some of the variables
in a mechanics problem but need to determine the missing quantity.

For most calculators:

1. Enter the known values.
2. Leave exactly one unknown variable blank.
3. Select **Solve question**.
4. Read the rearranged formula, substitution and final answer.

Projectile calculators return the main motion quantities together.

## Calculators included

| Topic | Calculator | Main equation |
| --- | --- | --- |
| Forces | Newton's second law | `F = ma` |
| Forces | Newton's third law | `F₂ = -F₁` |
| Momentum | Linear momentum | `p = mv` |
| Momentum | Impulse | `J = FΔt` |
| Momentum | Conservation of momentum | `m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂` |
| Projectile motion | Angled projectile | `T = 2u sinθ/g`, `R = u² sin2θ/g` |
| Projectile motion | Horizontal launch | `t = √(2h/g)`, `R = ut` |
| Energy | Work done | `W = Fd cosθ` |
| Energy | Kinetic energy | `Eₖ = ½mv²` |
| Energy | Gravitational potential energy | `Eₚ = mgh` |

## Features

- Python calculation engine
- Automatic unknown-variable detection
- Formula rearrangement and step-by-step working
- Input validation with learner-friendly error messages
- Support for negative velocities to represent direction
- Default gravitational acceleration of `9.81 m/s²`
- Responsive Dinglo interface for phones, tablets and computers
- No database, API key or third-party Python package required
- JSON endpoint for every calculation

## Technology

- Python 3.10+
- Python standard-library HTTP server
- HTML5 templates
- CSS3
- Vanilla JavaScript

The physics calculations are performed by Python. JavaScript sends the supplied
variables to the Python endpoint and displays the returned solution.

## Project structure

```text
Dinglo-Physics-Solver-Python/
├── .github/
│   └── workflows/
│       └── tests.yml
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_solvers.py
├── .gitattributes
├── .gitignore
├── app.py
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Run locally

### Requirements

- Python 3.10 or newer
- A modern web browser

### Steps

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Dinglo-Physics-Solver-Python.git
cd Dinglo-Physics-Solver-Python
```

Start the server:

```bash
python app.py
```

Open the address shown in the terminal. By default:

```text
http://127.0.0.1:5000
```

No `pip install` step is required because the project uses only Python's
standard library.

## Using a different port

The server reads the standard `PORT` environment variable.

Linux or macOS:

```bash
PORT=8000 python app.py
```

Windows PowerShell:

```powershell
$env:PORT=8000
python app.py
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The automated test suite checks the main equations, inverse calculations,
projectile outputs and validation errors.

## API

The browser communicates with:

```text
POST /api/solve
```

Example request:

```json
{
  "calculator": "newton2",
  "values": {
    "F": "",
    "m": "10",
    "a": "2.5"
  }
}
```

Example response:

```json
{
  "answer": "F = 25 N",
  "steps": [
    "Formula: F = ma",
    "Substitute: F = (10.0)(2.5)",
    "Answer: F = 25 N"
  ]
}
```

Available calculator identifiers:

```text
newton2
newton3
momentum
impulse
collision
projectile
horizontal
work
kinetic
potential
```

## Deployment

Deploy the repository on a server that can run Python continuously. Start the
application with:

```bash
python app.py
```

The hosting service may provide its own `PORT` value, which the application
detects automatically.

## Accuracy note

This tool supports learning and checking calculations. Learners should still:

- convert values to SI units;
- use signs consistently for direction;
- round only at the final step; and
- follow the conventions required by their lecturer or examination.

## Author

**Mangena Kegorapetse**  
Founder and Full-Stack Developer  
Dinglo

## License

Copyright © 2026 Mangena Kegorapetse. All rights reserved. See [LICENSE](LICENSE).
