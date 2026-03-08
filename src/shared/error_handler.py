import time
import logging
from functools import wraps
from typing import Callable, Any

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("agentflow")


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    exceptions: tuple = (Exception,)
):
    """
    Décorateur : retry automatique avec délai exponentiel.
    Utile pour DuckDuckGo rate limits et Groq API errors.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        f"[{func.__name__}] Tentative {attempt + 1}/{max_retries} "
                        f"échouée : {e}. Retry dans {delay:.1f}s..."
                    )
                    time.sleep(delay)
            logger.error(
                f"[{func.__name__}] Échec après {max_retries} tentatives."
            )
            raise last_exception
        return wrapper
    return decorator


def safe_node(fallback_message: str = "Une erreur est survenue."):
    """
    Décorateur : capture les exceptions dans un node LangGraph
    et retourne un message d'erreur propre sans crasher le graphe.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(state: dict, *args, **kwargs) -> dict:
            try:
                return func(state, *args, **kwargs)
            except Exception as e:
                logger.error(f"[{func.__name__}] Erreur : {e}")
                return {
                    "synthesis": f"⚠️ {fallback_message} Détail : {str(e)}",
                    "final_answer": f"⚠️ {fallback_message} Détail : {str(e)}",
                    "execution_result": f"ERREUR : {str(e)}"
                }
        return wrapper
    return decorator