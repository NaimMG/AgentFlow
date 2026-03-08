import gradio as gr
from dotenv import load_dotenv
from agent1_research.graph import build_graph
from agent1_research.nodes import get_llm
from langchain_core.messages import HumanMessage

load_dotenv()

graph = build_graph()
llm = get_llm()


def run_agent_streaming(query: str, max_iterations: int):
    """Lance le Research Agent avec streaming des tokens."""
    if not query.strip():
        yield "⚠️ Veuillez entrer une question."
        return

    # Étape 1 : feedback immédiat
    yield "🔍 **Recherche en cours...**\n\n"

    # Étape 2 : exécution du graphe
    result = graph.invoke({
        "query": query,
        "messages": [],
        "search_results": [],
        "synthesis": "",
        "iterations": 0,
        "max_iterations": int(max_iterations)
    })

    iterations = result.get("iterations", 0)
    synthesis = result.get("synthesis", "")

    yield f"🔍 **Recherche en cours...**\n\n✅ **Terminé en {iterations} itération(s)**\n\n---\n\n"

    # Étape 3 : streaming token par token via LLM
    prompt = f"""
    Voici une synthèse de recherche sur : "{query}"

    {synthesis}

    Présente cette synthèse de façon claire et structurée en markdown.
    """

    accumulated = f"🔍 **Recherche en cours...**\n\n✅ **Terminé en {iterations} itération(s)**\n\n---\n\n"

    for chunk in llm.stream([HumanMessage(content=prompt)]):
        accumulated += chunk.content
        yield accumulated


with gr.Blocks(title="AgentFlow — Research Agent (Streaming)") as demo:

    gr.Markdown("""
    # 🤖 AgentFlow — Research Agent
    ### ⚡ Streaming activé — Powered by LangGraph + Groq + DuckDuckGo
    Les réponses s'affichent en temps réel.
    """)

    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="💬 Votre question",
                placeholder="Ex: Quelles sont les dernières avancées de LangGraph en 2025 ?",
                lines=3
            )
        with gr.Column(scale=1):
            max_iter = gr.Slider(
                minimum=1,
                maximum=5,
                value=3,
                step=1,
                label="🔄 Itérations max"
            )

    run_btn = gr.Button("🚀 Lancer l'agent", variant="primary")
    output = gr.Markdown(label="Réponse en streaming")

    run_btn.click(
        fn=run_agent_streaming,
        inputs=[query_input, max_iter],
        outputs=output
    )

    gr.Examples(
        examples=[
            ["Quelles sont les dernières avancées de LangGraph en 2025 ?", 3],
            ["Comment fonctionne le RAG en NLP ?", 2],
            ["Quels sont les meilleurs modèles open-source en 2025 ?", 3],
        ],
        inputs=[query_input, max_iter]
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())