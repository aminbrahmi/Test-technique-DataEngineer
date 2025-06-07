 Test Technique Data Engineer : Détection de contenus liés au harcèlement

Ce projet vise à démontrer l'application d'un pipeline de collecte, traitement et visualisation de données sur le thème du harcèlement à partir de Reddit, Twitter et Telegram. Le pipeline inclut le scraping, le prétraitement NLP, l'indexation dans Elasticsearch et la visualisation via Kibana.

✈️ Objectifs Techniques

-Scraping des réseaux sociaux : Reddit, Twitter, Telegram

-Stockage NoSQL avec MongoDB

-Prétraitement linguistique (cleaning + NLP)

-Indexation avec Elasticsearch

-Visualisation avec Kibana (ELK stack)

-Conteneurisation via Docker/Docker Compose

-Tests unitaires de validation des scripts

Architecture

Test-technique-DataEngineer/
│
├── config/              # Configuration API (config.ini)
├── scripts/             # Scripts principaux
│   ├── scraper.py       # Scraping Reddit, Twitter, Telegram
│   ├── preprocessing.py # Nettoyage et lemmatisation
│   ├── nlp_pipeline.py  # Langue + sentiment
│   └── es_ingest.py     # Indexation Elasticsearch
│
├── tests/               # Tests unitaires
│   ├── test_scraper.py
│   ├── test_preprocessing.py
│   └── test_nlp_pipeline.py
│
├── docs/                # Données et visualisations
│   ├── Kibana Dashboard/        # Captures écran Kibana
│   ├── mongo_results.json       # Export MongoDB
│   └── es_results.json          # Export Elasticsearch
│
├── Dockerfile           # Environnement d'exécution
├── docker-compose.yml   # Lancement des services
├── requirements.txt     # Librairies Python
└── README.md            # Documentation actuelle

1. 💿 Scraping des données (scripts/scraper.py)

Reddit : via praw, depuis les subreddits bullying, TrueOffMyChest

Twitter (X) : via tweepy et token Bearer

Telegram : via Telethon, accès à des groupes publics

Les données sont stockées dans MongoDB (db: harcelement, collection: posts).

Champs collectés : title, content, author, date, url, source, processed

2. ⚖️ Prétraitement des textes (scripts/preprocessing.py)

Suppression des balises HTML et URLs

Nettoyage (ponctuation, chiffres)

Lemmatisation et suppression des stopwords avec SpaCy

Mise à jour du champ cleaned_content et processed = True

3. 🧠 Traitement NLP (scripts/nlp_pipeline.py)

Langue : détection via langid

Traduction automatique si besoin avec GoogleTranslator

Sentiment : via TextBlob

Ajout des champs : language, sentiment, sentiment_score

4. ⚙️ Indexation Elasticsearch (scripts/es_ingest.py)

Connexion à MongoDB et Elasticsearch

Création d'index harcelement_posts avec mapping personnalisé

Indexation via helpers.bulk

Rafraîchissement pour Kibana

Champs indexés : title, content, author, language, sentiment, sentiment_score, etc.

5. 📊 Visualisation avec Kibana

Kibana Dashboard (URL: http://localhost:5601)

Contenus du tableau de bord :

Diagramme de répartition par langue

Diagramme de répartition par sentiment

Courbe temporelle des publications

Liste des contenus les plus négatifs

Filtres dynamiques : langue, source, date

📚 Choix techniques

MongoDB pour le stockage NoSQL (souplesse de structure)

Elasticsearch pour l'indexation rapide et recherches avancées

TextBlob + GoogleTranslator : facile à intégrer pour de l'analyse de sentiment rapide

Docker Compose : isolation de chaque service (Mongo, ES, Kibana, Scraper)


🔧 Lancement manuel

# Scraping
docker exec -it scraper python scripts/scraper.py

# Nettoyage
docker exec -it scraper python scripts/preprocessing.py

# NLP
docker exec -it scraper python scripts/nlp_pipeline.py

# Indexation
python scripts/es_ingest.py


📚 Tests unitaires (dossier /tests)

test_scraper.py : vérifie que les fonctions Reddit/Telegram sont appelables

test_preprocessing.py : vérifie le nettoyage du texte

test_nlp_pipeline.py : vérifie la langue et le sentiment

💾 Export des données

MongoDB : docs/mongo_results.json

Elasticsearch : docs/es_results.json

Les fichiers se trouvent dans le dossier docs/

Les captures d’écran du tableau de bord Kibana dans docs/Kibana Dashboard/