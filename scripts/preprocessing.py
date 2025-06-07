import re
from pymongo import MongoClient
from bs4 import BeautifulSoup
import spacy

# Initialiser le modèle spaCy français
nlp = spacy.load("fr_core_news_sm")

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['harcelement']
collection = db['posts']

def clean_text(text):
    if not text:
        return ""

    # Supprimer balises HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # Supprimer les URLs
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)

    # Mise en minuscules
    text = text.lower()

    # Supprimer toute ponctuation
    text = re.sub(r"[^\w\s]", '', text)

    # Tokenisation + lemmatisation + suppression des stopwords
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop]

    return ' '.join(tokens)


def preprocess_all():
    posts = collection.find({"processed": False})  # Prétraiter seulement les non traités

    for post in posts:
        cleaned = clean_text(post.get("content", ""))
        collection.update_one(
            {"_id": post["_id"]},
            {"$set": {"cleaned_content": cleaned, "processed": True}}
        )
        print(f"✅ Cleaned post from {post['source']} | Content preview: {cleaned[:50]}")

if __name__ == "__main__":
    print("🔄 Starting text preprocessing...")
    preprocess_all()
    print("✅ Preprocessing complete.")
