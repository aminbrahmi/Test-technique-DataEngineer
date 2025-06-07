import json
import os
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime

#Créer dossier s'il n'existe pas
os.makedirs("docs", exist_ok=True)

#Connexion MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['harcelement']
mongo_collection = mongo_db['posts']

#Export MongoDB
mongo_output_path = "docs/mongo_results.json"

with open(mongo_output_path, "w", encoding="utf-8") as f:
    for doc in mongo_collection.find():
        doc["_id"] = str(doc["_id"])
        for key, value in doc.items():
            if isinstance(value, datetime):
                doc[key] = value.isoformat()
        json.dump(doc, f, ensure_ascii=False)
        f.write("\n")

mongo_client.close()
print(f"✅ Données MongoDB exportées dans {mongo_output_path}")

#Connexion Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "harcelement_posts"
query = {"query": {"match_all": {}}}

# Export Elasticsearch
es_output_path = "docs/es_results.json"
results = es.search(index=index_name, query=query["query"], size=10000)

with open(es_output_path, "w", encoding="utf-8") as f:
    for hit in results["hits"]["hits"]:
        json.dump(hit["_source"], f, ensure_ascii=False)
        f.write("\n")

print(f"✅ Données Elasticsearch exportées dans {es_output_path}")
