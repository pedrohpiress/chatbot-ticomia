from services.context_service import montar_prompt
from services.llama_service import perguntar_llama
from services.memory_service import salvar_memoria

def responder_chat(pergunta):

    prompt = montar_prompt(pergunta)

    resposta = perguntar_llama(prompt)

    salvar_memoria(
        pergunta=pergunta,
        resposta=resposta
    )

    return resposta