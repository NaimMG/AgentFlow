FROM python:3.10-slim

# Répertoire de travail
WORKDIR /app

# Copie des fichiers
COPY pyproject.toml .
COPY src/ ./src/
COPY app.py app2.py app3.py app_streaming.py main.py ./
COPY docs/ ./docs/
COPY .env.example .env

# Installation des dépendances
RUN pip install --upgrade pip && \
    pip install -e ".[agent1]" && \
    pip install ddgs pandas matplotlib seaborn tabulate \
    langchain-groq "langfuse==2.60.3"

# Port Gradio
EXPOSE 7860

# Lancement par défaut : Orchestrator
CMD ["python", "app3.py"]