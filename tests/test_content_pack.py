import unittest

from app.generators.content_pack import generate_content_pack
from app.providers.template import TemplateProvider


class ContentPackTests(unittest.TestCase):
    def test_template_content_pack_contains_required_sections(self) -> None:
        pack = generate_content_pack(
            topic="LLM для новачків",
            audience="люди, які починають вивчати AI",
            platform="instagram",
            provider=TemplateProvider(),
        )

        self.assertTrue(pack.hook)
        self.assertTrue(pack.reel_script)
        self.assertEqual(len(pack.carousel_slides), 6)
        self.assertEqual(len(pack.video_prompts), 3)
        self.assertGreaterEqual(len(pack.hashtags), 5)


if __name__ == "__main__":
    unittest.main()
