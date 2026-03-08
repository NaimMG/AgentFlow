# 🤖 AgentFlow — AI Agents Portfolio

> Portfolio de 3 agents autonomes construits avec LangGraph, 100% open-source.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-green)
![Groq](https://img.shields.io/badge/LLM-Groq%20llama--3.3--70b-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Objectif

Démontrer la maîtrise des **AI Agents** modernes :
- Graphes d'états avec **LangGraph**
- LLMs locaux (**Ollama**) et cloud (**Groq**)
- Recherche web autonome
- Analyse de données multi-outils
- Orchestration multi-agents

---

## 🗂️ Agents

### ✅ Agent 1 — Research Agent
Agent de recherche web autonome avec boucle d'itération intelligente.

**Stack :** LangGraph · Groq llama-3.3-70b · DuckDuckGo · Gradio

**Architecture :**
```
planner → web_search → synthesizer → [continue?] → web_search
                                           ↓
                                          END
```

**Fonctionnalités :**
- Recherche web automatique via DuckDuckGo
- Boucle d'itération si l'information est insuffisante
- Synthèse structurée avec références datées
- Interface Gradio interactive
- Fallback Ollama si pas de clé Groq

### 🔜 Agent 2 — Data Analyst Agent
*(En cours)*

### 🔜 Agent 3 — Multi-Agent Orchestrator
*(Prévu)*

---

## 🚀 Installation
```bash
# Cloner le repo
git clone https://github.com/NaimMG/AgentFlow.git
cd AgentFlow

# Créer l'environnement virtuel
python -m venv AgentFlow
source AgentFlow/bin/activate

# Installer les dépendances
pip install -e ".[agent1]"

# Configurer les variables d'environnement
cp .env.example .env
# Ajouter GROQ_API_KEY dans .env
```

## ▶️ Lancer l'Agent 1
```bash
# Interface Gradio
python app.py

# CLI
python main.py
```

---

## 🛠️ Stack Technique

| Composant | Outil |
|---|---|
| Agent Framework | LangGraph 1.0 |
| LLM principal | Groq llama-3.3-70b (free tier) |
| LLM local | Ollama llama3.2 |
| Search Tool | DuckDuckGo |
| UI | Gradio |
| Versionning | Git + GitHub |

---

## 📁 Structure
```
AgentFlow/
├── src/
│   ├── agent1_research/
│   │   ├── state.py      # ResearchState TypedDict
│   │   ├── nodes.py      # planner, search, synthesizer
│   │   └── graph.py      # LangGraph StateGraph
│   └── shared/
├── tests/
├── docs/
├── app.py                # Interface Gradio
├── main.py               # CLI
└── pyproject.toml
```

---

## 👤 Auteur

**Naim** — [GitHub](https://github.com/NaimMG)