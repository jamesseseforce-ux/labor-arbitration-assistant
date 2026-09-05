import re
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseAssetTests(unittest.TestCase):
    def test_bilingual_identity_and_user_docs(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        publishing = (ROOT / "PUBLISHING.md").read_text(encoding="utf-8")
        examples = (ROOT / "examples" / "usage-examples.md").read_text(encoding="utf-8")
        combined = "\n".join((readme, publishing))
        self.assertIn("劳动仲裁全能助手", combined)
        self.assertIn("Employee Labor Arbitration Assistant", combined)
        self.assertIn("简介", readme)
        self.assertIn("如何使用", readme)
        self.assertGreaterEqual(examples.count("```text"), 8)
        self.assertIn("推广文案", publishing)

    def test_logo_is_valid_square_png(self):
        logo = ROOT / "assets" / "logo.png"
        data = logo.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        color_type = data[25]
        self.assertEqual(width, height)
        self.assertGreaterEqual(width, 512)
        self.assertIn(color_type, (4, 6), "logo should include an alpha channel")

    def test_ui_metadata_references_existing_logo(self):
        metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        for value in re.findall(r'icon_(?:small|large):\s*"([^"]+)"', metadata):
            self.assertTrue((ROOT / value).resolve().exists(), value)
        self.assertIn('brand_color: "#0B3F7A"', metadata)


if __name__ == "__main__":
    unittest.main()
