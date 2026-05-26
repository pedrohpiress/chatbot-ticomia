from fastapi import APIRouter
from models.chat_request import ChatRequest
from models.chat_response import ChatResponse
from services.chat_service import responder_chat

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/", response_model=ChatResponse)
def conversar(request: ChatRequest):

    resposta = responder_chat(request.pergunta)

    return ChatResponse(
        resposta=resposta
    )