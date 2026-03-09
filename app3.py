import gradio as gr
import os
from dotenv import load_dotenv
from agent3_orchestrator.graph import build_orchestrator_graph

load_dotenv()

graph = build_orchestrator_graph()


def run_orchestrator(query: str, csv_file):
    """Lance l'Orchestrateur et retourne la réponse + l'agent utilisé."""
    if not query.strip():
        return "⚠️ Veuillez entrer une question.", "", ""

    csv_path = csv_file.name if csv_file else None

    result = graph.invoke({
        "query": query,
        "messages": [],
        "csv_path": csv_path,
        "selected_agent": "",
        "agent_result": "",
        "final_response": "",
        "routing_reason": ""
    })

    selected = result.get("selected_agent", "")
    reason = result.get("routing_reason", "")
    response = result.get("final_response", "")

    agent_label = {
        "research": "🔍 Research Agent",
        "analyst": "📊 Data Analyst Agent"
    }.get(selected, selected)

    routing_info = f"**Agent sélectionné :** {agent_label}\n\n**Raison :** {reason}"

    return response, routing_info


with gr.Blocks(title="AgentFlow — Orchestrator") as demo:

    gr.Markdown("""
    # 🎭 AgentFlow — Multi-Agent Orchestrator
    ### Powered by LangGraph + Groq (llama-3.3-70b)
    
    Le **Supervisor** analyse ta question et route automatiquement vers le bon agent :
    - 🔍 **Research Agent** — recherche web, actualités, questions générales
    - 📊 **Data Analyst Agent** — analyse CSV, statistiques, visualisations
    """)

    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="💬 Votre question",
                placeholder="Posez n'importe quelle question...",
                lines=3
            )
        with gr.Column(scale=1):
            csv_input = gr.File(
                label="📁 CSV (optionnel)",
                file_types=[".csv"]
            )

    run_btn = gr.Button("🚀 Lancer l'Orchestrateur", variant="primary")

    routing_output = gr.Markdown(label="🧭 Décision du Supervisor")
    response_output = gr.Markdown(label="📝 Réponse finale")

    run_btn.click(
        fn=run_orchestrator,
        inputs=[query_input, csv_input],
        outputs=[response_output, routing_output]
    )

    gr.Examples(
        examples=[
            ["Quelles sont les dernières avancées de l'IA en 2025 ?", None],
            ["Quel est le meilleur framework pour construire des AI Agents ?", None],
            ["Quel produit génère le plus de chiffre d'affaires ?", "docs/sample_data.csv"],
            ["Montre l'évolution des ventes par mois", "docs/sample_data.csv"],
        ],
        inputs=[query_input, csv_input]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())