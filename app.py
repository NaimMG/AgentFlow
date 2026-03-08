import gradio as gr
from dotenv import load_dotenv
from agent1_research.graph import build_graph

load_dotenv()

graph = build_graph()


def run_agent(query: str, max_iterations: int) -> str:
    """Lance le Research Agent et retourne la synthèse."""
    if not query.strip():
        return "⚠️ Veuillez entrer une question."

    result = graph.invoke({
        "query": query,
        "messages": [],
        "search_results": [],
        "synthesis": "",
        "iterations": 0,
        "max_iterations": int(max_iterations)
    })

    iterations = result.get("iterations", 0)
    synthesis = result.get("synthesis", "Aucune réponse générée.")

    return f"🔄 **Itérations effectuées : {iterations}**\n\n---\n\n{synthesis}"


with gr.Blocks(title="AgentFlow — Research Agent") as demo:

    gr.Markdown("""
    # 🤖 AgentFlow — Research Agent
    ### Powered by LangGraph + Groq (llama-3.3-70b) + DuckDuckGo
    Agent autonome de recherche web avec boucle d'itération intelligente.
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

    output = gr.Markdown(label="Résultat")

    run_btn.click(
        fn=run_agent,
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