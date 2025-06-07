import unittest
from scripts.preprocessing import clean_text

class TestPreprocessing(unittest.TestCase):
    def test_clean_text_basic(self):
        raw = "Hello!! This is a test :)"
        cleaned = clean_text(raw)
        self.assertIsInstance(cleaned, str)
        self.assertNotIn("!", cleaned)
        self.assertIn("hello", cleaned.lower())

    def test_clean_empty_string(self):
        self.assertEqual(clean_text(""), "")
    
if __name__ == '__main__':
    unittest.main()
