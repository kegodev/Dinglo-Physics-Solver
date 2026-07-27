import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class RepositoryHealthTests(unittest.TestCase):
    def test_community_files_exist(self):
        expected = [
            "CODE_OF_CONDUCT.md",
            "CONTRIBUTING.md",
            "LICENSE",
            "SECURITY.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/feature_request.yml",
            ".github/ISSUE_TEMPLATE/config.yml",
        ]
        missing = [path for path in expected if not (PROJECT_ROOT / path).is_file()]
        self.assertEqual(missing, [])

    def test_repository_uses_mit_license(self):
        license_text = (PROJECT_ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(license_text.startswith("MIT License"))
        self.assertIn("Mangena Kegorapetse", license_text)

    def test_contribution_guide_explains_pull_requests(self):
        guide = (PROJECT_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("Fork the repository", guide)
        self.assertIn("Opening a pull request", guide)
        self.assertIn("python -m unittest discover -s tests -v", guide)


if __name__ == "__main__":
    unittest.main()
