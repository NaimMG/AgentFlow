import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Sans interface graphique
import matplotlib.pyplot as plt
from io import StringIO
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from agent2_analyst.state import AnalystState
from shared.observability import trace_agent_run

load_dotenv()


def get_llm():
    """Groq par défaut, Ollama en fallback."""
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    return ChatOllama(model="llama3.2:latest", temperature=0)


llm = get_llm()


def loader_node(state: AnalystState) -> dict:
    """Charge le CSV et génère un aperçu des données."""
    try:
        df = pd.read_csv(state["csv_path"])
        buf = StringIO()
        df.info(buf=buf)
        preview = f"""
## Aperçu du dataset

**Shape :** {df.shape[0]} lignes x {df.shape[1]} colonnes

**Colonnes :**
{df.dtypes.to_string()}

**Premières lignes :**
{df.head().to_string()}

**Statistiques :**
{df.describe().to_string()}
        """
        return {"data_preview": preview, "attempts": 0}
    except Exception as e:
        return {"data_preview": f"Erreur chargement : {e}", "attempts": 0}


def code_generator_node(state: AnalystState) -> dict:
    """Génère du code Python pour répondre à la question."""
    response = llm.invoke([
        HumanMessage(content=f"""
Tu es un expert Data Analyst Python.

Voici les informations sur le dataset (chargé dans la variable `df`) :
{state['data_preview']}

Question : {state['query']}

Génère du code Python qui :
1. Utilise la variable `df` déjà chargée (ne recharge pas le CSV)
2. Répond à la question avec pandas
3. Si pertinent, crée une visualisation avec matplotlib et sauvegarde-la avec : plt.savefig('output_chart.png', bbox_inches='tight')
4. Affiche le résultat final avec print()

Réponds UNIQUEMENT avec le code Python, sans explications ni balises markdown.
        """)
    ])
    return {
        "generated_code": response.content,
        "messages": [response]
    }


def code_executor_node(state: AnalystState) -> dict:
    """Exécute le code Python généré de façon sécurisée."""
    code = state["generated_code"]

    # Nettoyage du code (retire les balises markdown si présentes)
    code = code.replace("```python", "").replace("```", "").strip()

    # Capture de la sortie
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    chart_path = None

    try:
        df = pd.read_csv(state["csv_path"])
        exec_globals = {"df": df, "pd": pd, "plt": plt}
        exec(code, exec_globals)
        output = sys.stdout.getvalue()

        if os.path.exists("output_chart.png"):
            chart_path = "output_chart.png"

        return {
            "execution_result": output or "Code exécuté avec succès (pas de sortie texte).",
            "chart_path": chart_path,
            "attempts": state.get("attempts", 0) + 1
        }
    except Exception as e:
        return {
            "execution_result": f"ERREUR : {str(e)}",
            "chart_path": None,
            "attempts": state.get("attempts", 0) + 1
        }
    finally:
        sys.stdout = old_stdout


def answer_node(state: AnalystState) -> dict:
    """Formule la réponse finale en langage naturel."""
    response = llm.invoke([
        HumanMessage(content=f"""
        Question originale : {state['query']}

        Résultat de l'analyse :
        {state['execution_result']}

        Formule une réponse claire, structurée et professionnelle en français.
        Inclus les chiffres clés et insights importants.
        """)
    ])

    # Tracking Langfuse
    trace_agent_run(
        agent_name="analyst_agent",
        query=state["query"],
        result={
            "execution_result": state["execution_result"][:200],
            "chart_generated": bool(state.get("chart_path")),
            "attempts": state.get("attempts", 0)
        }
    )

    return {
        "final_answer": response.content,
        "messages": [response]
    }


def should_retry(state: AnalystState) -> str:
    """Retry si erreur et tentatives restantes, sinon continue."""
    if (
        "ERREUR" in state.get("execution_result", "")
        and state.get("attempts", 0) < state.get("max_attempts", 3)
    ):
        return "retry"
    return "answer"