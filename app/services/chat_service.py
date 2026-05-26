import gc

from app.services.context_service import gerar_contexto_minimo
from app.services.llma_service import perguntar_llama

def responder_chat(pergunta):

    contexto = ""
    prompt = ""

    try:
        contexto = gerar_contexto_minimo(pergunta)

        prompt = f"""
Voce e um assistente financeiro especializado.

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}
""".strip()

        return perguntar_llama(prompt)
    finally:
        del contexto
        del prompt
        gc.collect()