from fastapi import FastAPI
from routes.chat_routes import router

app = FastAPI(
    title="Chatbot Financeiro Ticomia"
)

app.include_router(router)