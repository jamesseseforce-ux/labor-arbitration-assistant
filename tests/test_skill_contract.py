import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_all_local_markdown_links_exist(self):
        for source in sorted(ROOT.rglob("*.md")):
            text = source.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (source.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(resolved.exists(), f"missing link from {source.name}: {target}")

    def test_response_levels_cover_requested_thresholds(self):
        text = (ROOT / "references" / "response-levels.md").read_text(encoding="utf-8")
        self.assertIn("缺1—2项", text)
        self.assertIn("缺3项以上", text)
        self.assertIn("文书正文不计入", text)

    def test_behavior_suite_has_new_cases(self):
        text = (ROOT / "tests" / "scenarios.md").read_text(encoding="utf-8")
        ids = {int(number) for number in re.findall(r"\| T(\d+) \|", text)}
        self.assertTrue(set(range(15, 22)).issubset(ids))

    def test_package_has_no_private_absolute_path(self):
        for source in sorted(ROOT.rglob("*.md")):
            text = source.read_text(encoding="utf-8")
            self.assertNotIn("C:\\Users\\", text)
            self.assertNotIn("/D:/", text)


if __name__ == "__main__":
    unittest.main()
