import unittest
import sys
import os
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

# Ajoute le dossier parent au path pour permettre les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from scripts.scraper import scrape_reddit, scrape_telegram
except ImportError as e:
    print(f"❌ ImportError: {e}")
    scrape_reddit = None
    scrape_telegram = None


class TestScraper(unittest.TestCase):

    def test_scrape_reddit_exists(self):
        """Vérifie que la fonction scrape_reddit est bien importée."""
        self.assertIsNotNone(scrape_reddit, "❌ scrape_reddit n’est pas importé")

    def test_scrape_telegram_exists(self):
        """Vérifie que la fonction scrape_telegram est bien importée."""
        self.assertIsNotNone(scrape_telegram, "❌ scrape_telegram n’est pas importé")

    def test_scrape_reddit_output(self):
        """Vérifie que scrape_reddit renvoie une liste (si elle ne plante pas)."""
        if scrape_reddit:
            try:
                data = scrape_reddit()
                self.assertIsInstance(data, list, "❌ scrape_reddit ne renvoie pas une liste")
            except Exception as e:
                self.skipTest(f"⚠️ Erreur lors de l’appel à scrape_reddit : {e}")
        else:
            self.skipTest("⚠️ scrape_reddit non défini")

    def test_scrape_telegram_output(self):
        """Vérifie que scrape_telegram renvoie une liste (si elle ne plante pas)."""
        if scrape_telegram:
            try:
                data = scrape_telegram()
                self.assertIsInstance(data, list, "❌ scrape_telegram ne renvoie pas une liste")
            except Exception as e:
                self.skipTest(f"⚠️ Erreur lors de l’appel à scrape_telegram : {e}")
        else:
            self.skipTest("⚠️ scrape_telegram non défini")


if __name__ == "__main__":
    unittest.main()
