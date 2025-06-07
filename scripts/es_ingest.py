from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
import time

# Configuration avec gestion des erreurs
max_retries = 5
wait_time = 10

# Connexion MongoDB
mongo_client = MongoClient(
    'mongodb://localhost:27017/',
    serverSelectionTimeoutMS=5000
)

# Connexion Elasticsearch avec réessais
for i in range(max_retries):
    try:
        es = Elasticsearch(
            ["http://localhost:9200"],
            request_timeout=30
        )
        if es.ping():
            print("✅ Connected to Elasticsearch")
            break
    except Exception as e:
        if i == max_retries - 1:
            raise Exception(f"❌ Failed to connect to Elasticsearch after {max_retries} attempts")
        print(f"⏳ Elasticsearch connection failed, retrying in {wait_time} seconds...")
        time.sleep(wait_time)

# Définir index et mapping
index_name = "harcelement_posts"
mapping = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"},
            "cleaned_content": {"type": "text"},
            "author": {"type": "keyword"},
            "date": {"type": "date"},
            "url": {"type": "keyword"},
            "source": {"type": "keyword"},
            "language": {"type": "keyword"},
            "sentiment": {"type": "keyword"},
            "sentiment_score": {"type": "float"},
            "retweets": {"type": "integer"},
            "processed": {"type": "boolean"}
        }
    }
}

# Créer l'index si nécessaire
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)
    print(f"✅ Index '{index_name}' créé.")
else:
    print(f"ℹ️ Index '{index_name}' existe déjà.")

# Générateur de documents
def doc_generator():
    db = mongo_client['harcelement']
    for post in db.posts.find({"processed": True}):
        yield {
            "_index": index_name,
            "_id": str(post["_id"]),
            "_source": {
                "title": post.get("title", ""),
                "content": post.get("content", ""),
                "cleaned_content": post.get("cleaned_content", ""),
                "author": post.get("author", ""),
                "date": post.get("date"),
                "url": post.get("url", ""),
                "source": post.get("source", ""),
                "language": post.get("language", ""),
                "sentiment": post.get("sentiment", ""),
                "sentiment_score": post.get("sentiment_score", 0),
                "retweets": post.get("retweets", 0),
                "processed": True
            }
        }

# Indexation
try:
    success, _ = helpers.bulk(es, doc_generator())
    print(f"✅ Indexation terminée - Documents indexés : {success}")
    es.indices.refresh(index=index_name)
    print(f"📊 Total documents : {es.count(index=index_name)['count']}")
except Exception as e:
    print(f"❌ Erreur lors de l'indexation : {str(e)}")
