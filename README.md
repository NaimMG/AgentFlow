# 🤖 AgentFlow — AI Agents Portfolio

> Portfolio de 3 agents autonomes construits avec LangGraph.

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

### ✅ Agent 2 — Data Analyst Agent
Agent d'analyse de données avec génération automatique de code et visualisations.

**Stack :** LangGraph · Groq llama-3.3-70b · Pandas · Matplotlib · Gradio

**Architecture :**
```
loader → code_generator → code_executor → [erreur?] → code_generator
                                               ↓
                                            answer → END
```

**Fonctionnalités :**
- Upload CSV et questions en langage naturel
- Génération et exécution automatique de code Python
- Visualisations matplotlib affichées dans l'UI
- Auto-retry si erreur de code (max 3 tentatives)

### ✅ Agent 3 — Multi-Agent Orchestrator
Supervisor intelligent qui route automatiquement vers le bon agent.

**Stack :** LangGraph · Groq llama-3.3-70b · Agent1 · Agent2

**Architecture :**
```
supervisor → [research?] → research_agent → synthesizer → END
           → [analyst?]  → analyst_agent  → synthesizer → END
```

**Fonctionnalités :**
- Routing automatique : Research vs Analyst
- Décision et justification expliquées à l'utilisateur
- Fallback intelligent si CSV absent

---

## 🚀 Installation
```bash
# Cloner le repo
git clone https://github.com/NaimMG/AgentFlow.git
cd AgentFlow

# Créer l'environnement virtuel
python -m venv AgentFlow
source AgentFlow/bin/activate  # Linux/Mac
# AgentFlow\Scripts\activate   # Windows

# Installer les dépendances
pip install -e ".[agent1]"
pip install ddgs pandas matplotlib seaborn tabulate langchain-groq

# Configurer les variables d'environnement
cp .env.example .env
# Ajouter GROQ_API_KEY=ta_clé dans .env
```

## ▶️ Lancer les agents
```bash
# Agent 1 — Research Agent
python app.py

# Agent 2 — Data Analyst Agent
python app2.py

# Agent 3 — Multi-Agent Orchestrator
python app3.py

# CLI Agent 1
python main.py
```

---

## 🛠️ Stack Technique

| Composant | Outil |
|---|---|
| Agent Framework | LangGraph 1.0 |
| LLM principal | Groq llama-3.3-70b (free tier) |
| LLM local fallback | Ollama llama3.2 |
| Search Tool | DuckDuckGo |
| Data Analysis | Pandas · Matplotlib |
| UI | Gradio 6 |
| Versionning | Git + GitHub |

---

## 📁 Structure
```
AgentFlow/
├── src/
│   ├── agent1_research/
│   │   ├── state.py          # ResearchState TypedDict
│   │   ├── nodes.py          # planner, search, synthesizer
│   │   └── graph.py          # LangGraph StateGraph
│   ├── agent2_analyst/
│   │   ├── state.py          # AnalystState TypedDict
│   │   ├── nodes.py          # loader, code_generator, executor, answer
│   │   └── graph.py          # LangGraph StateGraph
│   ├── agent3_orchestrator/
│   │   ├── state.py          # OrchestratorState TypedDict
│   │   ├── nodes.py          # supervisor, research, analyst, synthesizer
│   │   └── graph.py          # LangGraph StateGraph
│   └── shared/
├── docs/
│   └── sample_data.csv       # Dataset de test
├── tests/
├── app.py                    # UI Agent 1
├── app2.py                   # UI Agent 2
├── app3.py                   # UI Agent 3 (Orchestrator)
├── main.py                   # CLI Agent 1
└── pyproject.toml
```

---

## 👤 Auteur

**Naim** — [GitHub](https://github.com/NaimMG)