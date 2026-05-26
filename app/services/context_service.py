from app.services.finance_service import gerar_contexto_financeiro


def gerar_contexto_minimo(pergunta):

    return gerar_contexto_financeiro(pergunta)


def montar_prompt(pergunta):

    contexto = gerar_contexto_minimo(pergunta)

    prompt = f"""
Voce e um assistente financeiro especializado.

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}
""".strip()

    return prompt