import unittest

from page_generator import extract_title


class TestPageGenerator(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
# This is a title
Some content here.
"""
        title = extract_title(markdown)
        self.assertEqual(title, "This is a title")


if __name__ == "__main__":
    unittest.main()
