import math
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import SOLVERS, SolverError  # noqa: E402


class FormulaSolverTests(unittest.TestCase):
    def solve(self, calculator, **values):
        return SOLVERS[calculator](values)

    def test_newtons_second_law_finds_force(self):
        result = self.solve("newton2", F="", m="10", a="2.5")
        self.assertEqual(result["answer"], "F = 25 N")

    def test_newtons_second_law_finds_acceleration(self):
        result = self.solve("newton2", F="24", m="6", a="")
        self.assertEqual(result["answer"], "a = 4 m/s²")

    def test_newtons_third_law_reverses_direction(self):
        result = self.solve("newton3", F1="75", F2="")
        self.assertEqual(result["answer"], "F₂ = -75 N")

    def test_linear_momentum(self):
        result = self.solve("momentum", p="", m="4", v="-3")
        self.assertEqual(result["answer"], "p = -12 kg·m/s")

    def test_impulse(self):
        result = self.solve("impulse", J="", F="12", t="0.5")
        self.assertEqual(result["answer"], "J = 6 N·s")

    def test_conservation_of_momentum(self):
        result = self.solve(
            "collision",
            m1="2",
            u1="4",
            v1="",
            m2="2",
            u2="0",
            v2="1",
        )
        self.assertEqual(result["answer"], "v₁ = 3 m/s")

    def test_angled_projectile(self):
        result = self.solve("projectile", u="20", theta="45", g="9.81")
        self.assertIn("R = 40.77472 m", result["answer"])
        self.assertIn("H = 10.19368 m", result["answer"])

    def test_horizontal_projectile(self):
        result = self.solve("horizontal", u="5", h="10", g="9.81")
        self.assertIn("R = 7.13922 m", result["answer"])

    def test_work_done(self):
        result = self.solve("work", W="", F="10", d="4", theta="60")
        self.assertTrue(math.isclose(float(result["answer"].split()[2]), 20.0))

    def test_kinetic_energy(self):
        result = self.solve("kinetic", E="", m="2", v="3")
        self.assertEqual(result["answer"], "E = 9 J")

    def test_potential_energy_uses_default_gravity(self):
        result = self.solve("potential", E="", m="2", g="", h="5")
        self.assertEqual(result["answer"], "E = 98.1 J")

    def test_rejects_more_than_one_blank(self):
        with self.assertRaisesRegex(SolverError, "exactly one"):
            self.solve("newton2", F="", m="", a="2")

    def test_rejects_division_by_zero(self):
        with self.assertRaisesRegex(SolverError, "Mass cannot be zero"):
            self.solve("newton2", F="20", m="0", a="")

    def test_rejects_invalid_projectile_angle(self):
        with self.assertRaisesRegex(SolverError, "0° to 90°"):
            self.solve("projectile", u="20", theta="120", g="9.81")


class ThemeAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (PROJECT_ROOT / "templates" / "index.html").read_text(encoding="utf-8")
        cls.css = (PROJECT_ROOT / "static" / "style.css").read_text(encoding="utf-8")
        cls.javascript = (PROJECT_ROOT / "static" / "app.js").read_text(encoding="utf-8")

    def test_theme_toggle_is_accessible(self):
        self.assertIn('id="theme-toggle"', self.html)
        self.assertIn('aria-label="Switch to dark mode"', self.html)

    def test_dark_theme_styles_are_present(self):
        self.assertIn('[data-theme="dark"]', self.css)
        self.assertIn("color-scheme:dark", self.css)

    def test_theme_preference_is_saved(self):
        self.assertIn('localStorage.setItem("dinglo-theme"', self.javascript)
        self.assertIn("prefers-color-scheme: dark", self.javascript)


if __name__ == "__main__":
    unittest.main()
