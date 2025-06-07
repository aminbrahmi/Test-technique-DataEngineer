import unittest
from scripts.nlp_pipeline import detect_lang, analyze_sentiment

class TestNLPPipeline(unittest.TestCase):
    def test_detect_lang(self):
        self.assertEqual(detect_lang("Bonjour tout le monde"), "fr")
        self.assertEqual(detect_lang("Hello world"), "en")

    def test_analyze_sentiment_english(self):
        text = "I am very happy today!"
        sentiment = analyze_sentiment(text, "en")
        self.assertEqual(sentiment, "positif")

    def test_analyze_sentiment_negative(self):
        text = "I am depressed and hate everything."
        sentiment = analyze_sentiment(text, "en")
        self.assertEqual(sentiment, "négatif")

if __name__ == '__main__':
    unittest.main()
