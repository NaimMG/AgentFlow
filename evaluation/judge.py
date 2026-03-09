"""
LLM-as-a-Judge : évalue automatiquement les réponses des agents.
"""
import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

judge_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def evaluate_response(
    query: str,
    response: str,
    expected_keywords: list,
    min_length: int = 50
) -> dict:
    """
    Evalue une réponse d'agent sur 3 critères :
    - Pertinence (0-1) : la réponse répond-elle à la question ?
    - Complétude (0-1) : la réponse est-elle suffisamment détaillée ?
    - Factualité (0-1) : la réponse contient-elle les éléments attendus ?
    """

    # Score factualité basé sur les keywords
    keywords_found = sum(
        1 for kw in expected_keywords
        if kw.lower() in response.lower()
    )
    factuality_score = round(keywords_found / len(expected_keywords), 2)

    # Score longueur
    length_score = min(1.0, len(response) / min_length)

    # Score pertinence et qualité via LLM judge
    judge_response = judge_llm.invoke([
        HumanMessage(content=f"""
Tu es un évaluateur expert de réponses d'agents IA.

Question posée : "{query}"
Réponse de l'agent : "{response[:500]}"

Evalue cette réponse sur 2 critères, réponds UNIQUEMENT en JSON :
{{
    "pertinence": <score entre 0 et 1>,
    "qualite": <score entre 0 et 1>,
    "commentaire": "<une phrase d'explication>"
}}

Critères :
- pertinence : est-ce que la réponse répond bien à la question ?
- qualite : est-ce que la réponse est claire, structurée et utile ?
        """)
    ])

    try:
        content = judge_response.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()
        scores = json.loads(content)
    except Exception:
        scores = {"pertinence": 0.5, "qualite": 0.5, "commentaire": "Parsing error"}

    return {
        "pertinence": scores.get("pertinence", 0.5),
        "qualite": scores.get("qualite", 0.5),
        "factualite": factuality_score,
        "longueur": round(length_score, 2),
        "score_global": round(
            (scores.get("pertinence", 0.5) +
             scores.get("qualite", 0.5) +
             factuality_score) / 3, 2
        ),
        "commentaire": scores.get("commentaire", ""),
        "keywords_found": f"{keywords_found}/{len(expected_keywords)}"
    }