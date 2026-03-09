# 🤖 AgentFlow — AI Agents Portfolio

> Portfolio de 3 agents autonomes construits avec LangGraph.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-green)
![Groq](https://img.shields.io/badge/LLM-Groq%20llama--3.3--70b-orange)
![Tests](https://img.shields.io/badge/Tests-30%2F30-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Objectif

Démontrer la maîtrise des **AI Agents** modernes en production :
- Graphes d'états avec **LangGraph**
- LLMs locaux (**Ollama**) et cloud (**Groq**)
- Recherche web autonome
- Analyse de données multi-outils
- Orchestration multi-agents
- Observabilité avec **Langfuse** (self-hosted)
- Tests unitaires avec **pytest**
- Gestion des erreurs et retry automatique

---

## 🗂️ Agents

### ✅ Agent 1 — Research Agent
Agent de recherche web autonome avec boucle d'itération intelligente.

**Stack :** LangGraph · Groq llama-3.3-70b · DuckDuckGo · Gradio · Langfuse

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
- Streaming des tokens en temps réel
- Interface Gradio interactive
- Fallback Ollama si pas de clé Groq
- Retry automatique sur erreurs réseau

### ✅ Agent 2 — Data Analyst Agent
Agent d'analyse de données avec génération automatique de code et visualisations.

**Stack :** LangGraph · Groq llama-3.3-70b · Pandas · Matplotlib · Gradio · Langfuse

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
- Tracking des runs dans Langfuse

### ✅ Agent 3 — Multi-Agent Orchestrator
Supervisor intelligent qui route automatiquement vers le bon agent.

**Stack :** LangGraph · Groq llama-3.3-70b · Agent1 · Agent2 · Langfuse

**Architecture :**
```
supervisor → [research?] → research_agent → synthesizer → END
           → [analyst?]  → analyst_agent  → synthesizer → END
```

**Fonctionnalités :**
- Routing automatique : Research vs Analyst
- Décision et justification expliquées à l'utilisateur
- Fallback intelligent si CSV absent
- Tracking du routing dans Langfuse

---

## 🔭 Observabilité — Langfuse

Chaque run est tracé dans **Langfuse** (self-hosted via Docker) :
- Input/Output de chaque agent
- Nombre d'itérations
- Agent sélectionné par le supervisor
- Tags par agent pour filtrage
```bash
# Lancer Langfuse
docker compose up -d
# Dashboard : http://localhost:3000
```

---

## 🧪 Tests
```bash
pytest tests/ -v
# 30 tests : 30 passed
```

| Fichier | Tests | Couverture |
|---|---|---|
| test_agent1.py | 9 | state, nodes, graph, routing |
| test_agent2.py | 11 | state, nodes, graph, executor |
| test_agent3.py | 10 | state, supervisor, routing, edge cases |

---

## 🎯 Evaluation Automatique — LLM-as-a-Judge

Les agents sont évalués automatiquement via **Groq llama-3.3-70b** comme juge :
```bash
python -m evaluation.run_eval
```

| Agent | Pertinence | Qualité | Factualité | Global |
|---|---|---|---|---|
| Research Agent | 0.87 | 0.77 | 0.68 | 0.77 |
| Data Analyst Agent | 0.93 | 0.80 | 1.00 | 0.91 |
| **Moyenne** | | | | **0.84/1.0** |

3 critères mesurés automatiquement :
- **Pertinence** : la réponse répond-elle à la question ?
- **Qualité** : clarté et structure de la réponse
- **Factualité** : présence des éléments attendus

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
pip install ddgs pandas matplotlib seaborn tabulate langchain-groq langfuse==2.60.3

# Configurer les variables d'environnement
cp .env.example .env
# Editer .env : ajouter GROQ_API_KEY et LANGFUSE keys

# Lancer Langfuse (observabilité)
docker compose up -d
```

## ▶️ Lancer les agents
```bash
# Agent 1 — Research Agent (Gradio)
python app.py

# Agent 1 — Streaming
python app_streaming.py

# Agent 2 — Data Analyst (Gradio)
python app2.py

# Agent 3 — Orchestrator (Gradio)
python app3.py

# CLI
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
| Observabilité | Langfuse v2 (self-hosted) |
| Tests | pytest 9 · 30 tests |
| Conteneurisation | Docker · docker-compose |
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
│       ├── error_handler.py  # retry_with_backoff, safe_node
│       └── observability.py  # Langfuse tracking
├── tests/
│   ├── test_agent1.py        # 9 tests
│   ├── test_agent2.py        # 11 tests
│   └── test_agent3.py        # 10 tests
├── docs/
│   └── sample_data.csv       # Dataset de test
├── app.py                    # UI Agent 1
├── app_streaming.py          # UI Agent 1 (streaming)
├── app2.py                   # UI Agent 2
├── app3.py                   # UI Agent 3
├── main.py                   # CLI Agent 1
├── docker-compose.yml        # Langfuse + PostgreSQL
├── .env.example              # Template configuration
└── pyproject.toml
├── evaluation/
│   ├── dataset.py            # 6 questions/réponses attendues
│   ├── judge.py              # LLM-as-a-Judge scorer
│   └── run_eval.py           # Pipeline d'évaluation complet
```

---

## 👤 Auteur

**Naim** — [GitHub](https://github.com/NaimMG)