# Utilise une image Python 3.9 officielle comme point de départ
FROM python:3.9-slim-buster

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers nécessaires dans le conteneur
COPY app.py requirement.txt /app/

# Installe les dépendances Python spécifiées dans le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port 8050 utilisé par Plotly Dash
EXPOSE 8050

# Démarre l'application avec la commande "python app.py"
CMD ["python", "app.py", "--host=0.0.0.0", "--port=8050", "--debug"]
