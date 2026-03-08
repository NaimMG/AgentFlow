import gradio as gr
import os
from dotenv import load_dotenv
from agent2_analyst.graph import build_analyst_graph

load_dotenv()

graph = build_analyst_graph()


def run_analyst(csv_file, query: str, max_attempts: int):
    """Lance le Data Analyst Agent sur un CSV uploadé."""
    if csv_file is None:
        return "⚠️ Veuillez uploader un fichier CSV.", None
    if not query.strip():
        return "⚠️ Veuillez entrer une question.", None

    result = graph.invoke({
        "query": query,
        "messages": [],
        "csv_path": csv_file.name,
        "data_preview": "",
        "generated_code": "",
        "execution_result": "",
        "chart_path": None,
        "final_answer": "",
        "attempts": 0,
        "max_attempts": int(max_attempts)
    })

    answer = result.get("final_answer", "Aucune réponse générée.")
    chart = result.get("chart_path")

    code = result.get("generated_code", "")
    full_answer = f"{answer}\n\n---\n**Code généré :**\n```python\n{code}\n```"

    return full_answer, chart if chart and os.path.exists(chart) else None


with gr.Blocks(title="AgentFlow — Data Analyst Agent") as demo:

    gr.Markdown("""
    # 📊 AgentFlow — Data Analyst Agent
    ### Powered by LangGraph + Groq (llama-3.3-70b) + Pandas + Matplotlib
    Uploadez un CSV, posez une question en langage naturel — l'agent génère et exécute le code automatiquement.
    """)

    with gr.Row():
        csv_input = gr.File(label="📁 Upload CSV", file_types=[".csv"])
        max_att = gr.Slider(minimum=1, maximum=5, value=3, step=1, label="🔄 Tentatives max")

    query_input = gr.Textbox(
        label="💬 Votre question sur les données",
        placeholder="Ex: Quel produit génère le plus de chiffre d'affaires ?",
        lines=2
    )

    run_btn = gr.Button("🚀 Analyser", variant="primary")

    with gr.Row():
        answer_output = gr.Markdown(label="📝 Analyse")
        chart_output = gr.Image(label="📈 Visualisation")

    run_btn.click(
        fn=run_analyst,
        inputs=[csv_input, query_input, max_att],
        outputs=[answer_output, chart_output]
    )

    gr.Examples(
        examples=[
            ["docs/sample_data.csv", "Quel produit génère le plus de chiffre d'affaires ?", 3],
            ["docs/sample_data.csv", "Montre l'évolution des ventes par mois sous forme de graphique", 3],
            ["docs/sample_data.csv", "Quelle région performe le mieux ?", 3],
        ],
        inputs=[csv_input, query_input, max_att]
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())