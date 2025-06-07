from pymongo import MongoClient
from textblob import TextBlob
import langid
from deep_translator import GoogleTranslator

# Connexion MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['harcelement']
collection = db['posts']

# Fonction de détection de langue
def detect_lang(text):
    lang, _ = langid.classify(text)
    return lang

# Fonction d’analyse de sentiment
def analyze_sentiment(text, lang):
    try:
        # Traduction si texte non anglais
        if lang != 'en':
            try:
                text = GoogleTranslator(source='auto', target='en').translate(text)
            except Exception as e:
                print(f"❌ Erreur de traduction : {e}")
                return 'indéterminé'
        # Analyse avec TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return 'positif'
        elif polarity < -0.1:
            return 'négatif'
        else:
            return 'neutre'
    except Exception as e:
        print(f"❌ Erreur d'analyse de sentiment : {e} | Texte : {text[:100]}")
        return 'indéterminé'

# Traitement des documents
def process_nlp():
    posts = collection.find({"processed": True, "language": {"$exists": False}})

    for post in posts:
        text = post.get("cleaned_content", "")
        if not text.strip():
            continue

        lang = detect_lang(text)

        # Texte trop court : inutile d’analyser
        if len(text.split()) < 4:
            sentiment = 'indéterminé'
        else:
            sentiment = analyze_sentiment(text, lang)

        # Mise à jour MongoDB
        collection.update_one(
            {"_id": post["_id"]},
            {"$set": {
                "language": lang,
                "sentiment": sentiment
            }}
        )
        print(f"📄 Post {post['_id']} => Langue: {lang} | Sentiment: {sentiment}")

if __name__ == "__main__":
    print("🧠 NLP processing en cours...")
    process_nlp()
    print("✅ NLP terminé.")
