from __future__ import annotations

import math
import json
import mimetypes
import os
from pathlib import Path
from typing import Any
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse


BASE_DIR = Path(__file__).resolve().parent

SYMBOLS = {
    "F": "F", "m": "m", "a": "a", "F1": "F₁", "F2": "F₂", "p": "p",
    "v": "v", "J": "J", "t": "Δt", "m1": "m₁", "m2": "m₂",
    "u1": "u₁", "u2": "u₂", "v1": "v₁", "v2": "v₂", "u": "u",
    "theta": "θ", "g": "g", "h": "h", "W": "W", "d": "d", "E": "E",
}


class SolverError(ValueError):
    """A validation error safe to display to a learner."""


def number(data: dict[str, Any], key: str) -> float | None:
    raw = data.get(key)
    if raw is None or str(raw).strip() == "":
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise SolverError(f"{SYMBOLS.get(key, key)} must be a number.") from exc
    if not math.isfinite(value):
        raise SolverError("Use finite numerical values only.")
    return value


def display(value: float) -> str:
    if not math.isfinite(value):
        raise SolverError("The calculation produced an invalid result.")
    if abs(value) >= 10_000 or (0 < abs(value) < 0.001):
        return f"{value:.4e}"
    return f"{value:.5f}".rstrip("0").rstrip(".")


def one_blank(data: dict[str, Any], keys: list[str]) -> str:
    missing = [key for key in keys if number(data, key) is None]
    if len(missing) != 1:
        raise SolverError("Leave exactly one variable blank.")
    return missing[0]


def standard_solution(
    unknown: str,
    result: float,
    unit: str,
    formula: str,
    substitution: str,
) -> dict[str, Any]:
    symbol = SYMBOLS.get(unknown, unknown)
    answer = f"{symbol} = {display(result)} {unit}".strip()
    return {
        "answer": answer,
        "steps": [
            f"Formula: {formula}",
            f"Substitute: {substitution}",
            f"Answer: {answer}",
        ],
    }


def solve_newton_second(data: dict[str, Any]) -> dict[str, Any]:
    unknown = one_blank(data, ["F", "m", "a"])
    force, mass, acceleration = number(data, "F"), number(data, "m"), number(data, "a")
    if unknown == "F":
        return standard_solution("F", mass * acceleration, "N", "F = ma", f"F = ({mass})({acceleration})")
    if unknown == "m":
        if acceleration == 0:
            raise SolverError("Acceleration cannot be zero when solving for mass.")
        return standard_solution("m", force / acceleration, "kg", "m = F/a", f"m = {force}/{acceleration}")
    if mass == 0:
        raise SolverError("Mass cannot be zero.")
    return standard_solution("a", force / mass, "m/s²", "a = F/m", f"a = {force}/{mass}")


def solve_newton_third(data: dict[str, Any]) -> dict[str, Any]:
    unknown = one_blank(data, ["F1", "F2"])
    known_key = "F1" if unknown == "F2" else "F2"
    result = -number(data, known_key)
    return standard_solution(
        unknown, result, "N", f"{SYMBOLS[unknown]} = −{SYMBOLS[known_key]}",
        f"{SYMBOLS[unknown]} = −({number(data, known_key)})",
    )


def solve_momentum(data: dict[str, Any]) -> dict[str, Any]:
    unknown = one_blank(data, ["p", "m", "v"])
    p, mass, velocity = number(data, "p"), number(data, "m"), number(data, "v")
    if unknown == "p":
        return standard_solution("p", mass * velocity, "kg·m/s", "p = mv", f"p = ({mass})({velocity})")
    if unknown == "m":
        if velocity == 0:
            raise SolverError("Velocity cannot be zero when solving for mass.")
        return standard_solution("m", p / velocity, "kg", "m = p/v", f"m = {p}/{velocity}")
    if mass == 0:
        raise SolverError("Mass cannot be zero.")
    return standard_solution("v", p / mass, "m/s", "v = p/m", f"v = {p}/{mass}")


def solve_impulse(data: dict[str, Any]) -> dict[str, Any]:
    unknown = one_blank(data, ["J", "F", "t"])
    impulse, force, time = number(data, "J"), number(data, "F"), number(data, "t")
    if unknown == "J":
        return standard_solution("J", force * time, "N·s", "J = FΔt", f"J = ({force})({time})")
    if unknown == "F":
        if time == 0:
            raise SolverError("Time cannot be zero.")
        return standard_solution("F", impulse / time, "N", "F = J/Δt", f"F = {impulse}/{time}")
    if force == 0:
        raise SolverError("Force cannot be zero.")
    return standard_solution("t", impulse / force, "s", "Δt = J/F", f"Δt = {impulse}/{force}")


def solve_collision(data: dict[str, Any]) -> dict[str, Any]:
    mass1, mass2 = number(data, "m1"), number(data, "m2")
    if mass1 is None or mass2 is None or mass1 <= 0 or mass2 <= 0:
        raise SolverError("Enter positive values for both masses.")
    unknown = one_blank(data, ["u1", "u2", "v1", "v2"])
    u1, u2, v1, v2 = (number(data, key) for key in ["u1", "u2", "v1", "v2"])
    if unknown == "u1":
        result = (mass1 * v1 + mass2 * v2 - mass2 * u2) / mass1
    elif unknown == "u2":
        result = (mass1 * v1 + mass2 * v2 - mass1 * u1) / mass2
    elif unknown == "v1":
        result = (mass1 * u1 + mass2 * u2 - mass2 * v2) / mass1
    else:
        result = (mass1 * u1 + mass2 * u2 - mass1 * v1) / mass2
    substitution = (
        f"({mass1})({u1 if u1 is not None else '?'}) + "
        f"({mass2})({u2 if u2 is not None else '?'}) = "
        f"({mass1})({v1 if v1 is not None else '?'}) + "
        f"({mass2})({v2 if v2 is not None else '?'})"
    )
    return standard_solution(
        unknown, result, "m/s",
        f"m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂; solve for {SYMBOLS[unknown]}",
        substitution,
    )


def solve_projectile(data: dict[str, Any]) -> dict[str, Any]:
    speed, angle = number(data, "u"), number(data, "theta")
    gravity = number(data, "g") or 9.81
    if speed is None or angle is None:
        raise SolverError("Enter launch speed and angle.")
    if speed < 0 or gravity <= 0 or not 0 <= angle <= 90:
        raise SolverError("Use u ≥ 0, g > 0 and an angle from 0° to 90°.")
    radians = math.radians(angle)
    ux, uy = speed * math.cos(radians), speed * math.sin(radians)
    time = 2 * uy / gravity
    distance = speed**2 * math.sin(2 * radians) / gravity
    height = uy**2 / (2 * gravity)
    return {
        "answer": f"T = {display(time)} s  •  R = {display(distance)} m  •  H = {display(height)} m",
        "steps": [
            f"Resolve velocity: uₓ = {display(ux)} m/s, uᵧ = {display(uy)} m/s",
            f"Time of flight: T = 2u sinθ/g = {display(time)} s",
            f"Range: R = u² sin(2θ)/g = {display(distance)} m",
            f"Maximum height: H = u²sin²θ/(2g) = {display(height)} m",
        ],
    }


def solve_horizontal(data: dict[str, Any]) -> dict[str, Any]:
    speed, height = number(data, "u"), number(data, "h")
    gravity = number(data, "g") or 9.81
    if speed is None or height is None:
        raise SolverError("Enter horizontal speed and height.")
    if speed < 0 or height < 0 or gravity <= 0:
        raise SolverError("Speed and height cannot be negative, and gravity must be positive.")
    time = math.sqrt(2 * height / gravity)
    distance = speed * time
    vertical_speed = gravity * time
    impact_speed = math.hypot(speed, vertical_speed)
    return {
        "answer": f"t = {display(time)} s  •  R = {display(distance)} m  •  v = {display(impact_speed)} m/s",
        "steps": [
            f"Fall time: t = √(2h/g) = {display(time)} s",
            f"Horizontal range: R = ut = ({speed})({display(time)}) = {display(distance)} m",
            f"Impact speed: v = √(u² + (gt)²) = {display(impact_speed)} m/s",
        ],
    }


def solve_work(data: dict[str, Any]) -> dict[str, Any]:
    work, force, distance = number(data, "W"), number(data, "F"), number(data, "d")
    angle = number(data, "theta")
    if angle is None and all(value is not None for value in [work, force, distance]):
        if force * distance == 0:
            raise SolverError("Force × displacement cannot be zero.")
        ratio = work / (force * distance)
        if not -1 <= ratio <= 1:
            raise SolverError("These values do not produce a real angle.")
        result = math.degrees(math.acos(ratio))
        return standard_solution("theta", result, "°", "θ = cos⁻¹(W/Fd)", f"θ = cos⁻¹({work}/({force})({distance}))")
    angle = angle or 0
    unknown = one_blank(data, ["W", "F", "d"])
    cosine = math.cos(math.radians(angle))
    if unknown == "W":
        return standard_solution("W", force * distance * cosine, "J", "W = Fd cosθ", f"W = ({force})({distance})cos({angle}°)")
    if unknown == "F":
        if distance * cosine == 0:
            raise SolverError("d cosθ cannot be zero.")
        return standard_solution("F", work / (distance * cosine), "N", "F = W/(d cosθ)", f"F = {work}/(({distance})cos({angle}°))")
    if force * cosine == 0:
        raise SolverError("F cosθ cannot be zero.")
    return standard_solution("d", work / (force * cosine), "m", "d = W/(F cosθ)", f"d = {work}/(({force})cos({angle}°))")


def solve_kinetic(data: dict[str, Any]) -> dict[str, Any]:
    unknown = one_blank(data, ["E", "m", "v"])
    energy, mass, speed = number(data, "E"), number(data, "m"), number(data, "v")
    if unknown == "E":
        return standard_solution("E", 0.5 * mass * speed**2, "J", "Eₖ = ½mv²", f"Eₖ = ½({mass})({speed})²")
    if unknown == "m":
        if speed == 0:
            raise SolverError("Speed cannot be zero.")
        return standard_solution("m", 2 * energy / speed**2, "kg", "m = 2Eₖ/v²", f"m = 2({energy})/({speed})²")
    if mass <= 0 or energy < 0:
        raise SolverError("Mass must be positive and energy cannot be negative.")
    return standard_solution("v", math.sqrt(2 * energy / mass), "m/s", "v = √(2Eₖ/m)", f"v = √(2({energy})/{mass})")


def solve_potential(data: dict[str, Any]) -> dict[str, Any]:
    gravity = number(data, "g") or 9.81
    if gravity <= 0:
        raise SolverError("Gravity must be positive.")
    unknown = one_blank(data, ["E", "m", "h"])
    energy, mass, height = number(data, "E"), number(data, "m"), number(data, "h")
    if unknown == "E":
        return standard_solution("E", mass * gravity * height, "J", "Eₚ = mgh", f"Eₚ = ({mass})({gravity})({height})")
    if unknown == "m":
        if gravity * height == 0:
            raise SolverError("Height cannot be zero.")
        return standard_solution("m", energy / (gravity * height), "kg", "m = Eₚ/(gh)", f"m = {energy}/(({gravity})({height}))")
    if mass * gravity == 0:
        raise SolverError("Mass cannot be zero.")
    return standard_solution("h", energy / (mass * gravity), "m", "h = Eₚ/(mg)", f"h = {energy}/(({mass})({gravity}))")


SOLVERS = {
    "newton2": solve_newton_second,
    "newton3": solve_newton_third,
    "momentum": solve_momentum,
    "impulse": solve_impulse,
    "collision": solve_collision,
    "projectile": solve_projectile,
    "horizontal": solve_horizontal,
    "work": solve_work,
    "kinetic": solve_kinetic,
    "potential": solve_potential,
}


class DingloHandler(BaseHTTPRequestHandler):
    """Serve the page and its JSON calculator API using Python's standard library."""

    def send_bytes(self, content: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        self.send_bytes(
            json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            "application/json; charset=utf-8",
            status,
        )

    def do_GET(self) -> None:
        path = unquote(urlparse(self.path).path)
        if path == "/":
            page = (BASE_DIR / "templates" / "index.html").read_text(encoding="utf-8")
            page = page.replace(
                "{{ url_for('static', filename='style.css') }}", "/static/style.css"
            ).replace(
                "{{ url_for('static', filename='app.js') }}", "/static/app.js"
            )
            self.send_bytes(page.encode("utf-8"), "text/html; charset=utf-8")
            return

        if path.startswith("/static/"):
            relative = Path(path.removeprefix("/static/"))
            static_root = (BASE_DIR / "static").resolve()
            requested = (static_root / relative).resolve()
            if static_root not in requested.parents or not requested.is_file():
                self.send_json({"error": "File not found."}, 404)
                return
            mime_type = mimetypes.guess_type(requested.name)[0] or "application/octet-stream"
            self.send_bytes(requested.read_bytes(), mime_type)
            return

        self.send_json({"error": "Page not found."}, 404)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/solve":
            self.send_json({"error": "Page not found."}, 404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self.send_json({"error": "Invalid JSON request."}, 400)
            return

        calculator_id = payload.get("calculator")
        if calculator_id not in SOLVERS:
            self.send_json({"error": "Calculator not found."}, 404)
            return
        try:
            self.send_json(SOLVERS[calculator_id](payload.get("values") or {}))
        except SolverError as exc:
            self.send_json({"error": str(exc)}, 400)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"[Dinglo] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), DingloHandler)
    print(f"Dinglo Physics Solver is running at http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Dinglo Physics Solver.")
    finally:
        server.server_close()
