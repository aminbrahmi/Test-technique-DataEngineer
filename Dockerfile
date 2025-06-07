FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && \
    apt-get install -y git curl jq && \
    rm -rf /var/lib/apt/lists/*

# Installer wait-for-it
ADD https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Commande d'entrée améliorée
CMD ["sh", "-c", "./wait-for-it.sh elasticsearch:9200 --timeout=120 && \
                 ./wait-for-it.sh mongo:27017 --timeout=60 && \
                 python scripts/scraper.py"]