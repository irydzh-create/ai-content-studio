import unittest

from app.generators.content_pack import (
    generate_content_pack,
    parse_json_object,
)
from app.providers.template import TemplateProvider


class ContentPackTests(unittest.TestCase):
    def test_template_generation(self) -> None:
        content_pack = generate_content_pack(
            topic="Что такое RAG",
            audience="новички в IT",
            platform="Instagram",
            provider=TemplateProvider(),
        )

        self.assertTrue(content_pack.hook)
        self.assertTrue(content_pack.reel_script)
        self.assertEqual(
            len(content_pack.carousel_slides),
            6,
        )
        self.assertEqual(
            len(content_pack.video_prompts),
            3,
        )
        self.assertGreaterEqual(
            len(content_pack.hashtags),
            5,
        )

    def test_json_inside_markdown_block(self) -> None:
        raw_response = """
        ```json
        {
          "hook": "Тестовый хук"
        }
        ```
        """

        result = parse_json_object(raw_response)

        self.assertEqual(
            result["hook"],
            "Тестовый хук",
        )

    def test_empty_topic_is_rejected(self) -> None:
        with self.assertRaises(RuntimeError):
            generate_content_pack(
                topic=" ",
                audience="новички",
                platform="Instagram",
                provider=TemplateProvider(),
            )


if __name__ == "__main__":
    unittest.main()