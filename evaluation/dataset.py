"""
Dataset de questions/réponses attendues pour évaluer les agents.
"""

RESEARCH_DATASET = [
    {
        "query": "Qu'est-ce que LangGraph ?",
        "expected_keywords": ["graphe", "états", "LangChain", "agents", "framework"],
        "min_length": 100
    },
    {
        "query": "Quelle est la différence entre LangChain et LangGraph ?",
        "expected_keywords": ["LangChain", "LangGraph", "agents", "workflow"],
        "min_length": 100
    },
    {
        "query": "Qu'est-ce qu'un AI Agent ?",
        "expected_keywords": ["autonome", "outil", "décision", "LLM"],
        "min_length": 100
    },
]

ANALYST_DATASET = [
    {
        "query": "Quel produit génère le plus de chiffre d'affaires ?",
        "csv_path": "docs/sample_data.csv",
        "expected_keywords": ["Smartphone", "475", "chiffre"],
        "min_length": 50
    },
    {
        "query": "Quelle région performe le mieux ?",
        "csv_path": "docs/sample_data.csv",
        "expected_keywords": ["Paris", "région", "ventes"],
        "min_length": 50
    },
    {
        "query": "Combien y a-t-il de produits différents ?",
        "csv_path": "docs/sample_data.csv",
        "expected_keywords": ["6", "produits", "différents"],
        "min_length": 30
    },
]