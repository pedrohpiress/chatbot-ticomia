from services.finance_service import gerar_contexto_financeiro

def montar_prompt(pergunta):

    contexto = gerar_contexto_financeiro()

    system = open(
        "prompts/financeiro_prompt.txt",
        encoding="utf-8"
    ).read()

    prompt = f"""
{system}

DADOS FINANCEIROS:

{contexto}

PERGUNTA:
{pergunta}
"""

    return prompt