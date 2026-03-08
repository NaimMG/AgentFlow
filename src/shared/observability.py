import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3000")
)


def trace_agent_run(agent_name: str, query: str, result: dict) -> None:
    """Trace un run d'agent dans Langfuse."""
    try:
        langfuse.trace(
            name=agent_name,
            input={"query": query},
            output={"result": str(result)[:500]},
            tags=["agentflow", agent_name]
        )
        langfuse.flush()
        print(f"[Langfuse] ✅ Trace envoyée : {agent_name}")
    except Exception as e:
        print(f"[Langfuse] ⚠️ Trace ignorée : {e}")