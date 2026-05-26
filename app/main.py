from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat_routes import router as chat_router

main = FastAPI()

main.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://localhost:3039",
		"http://127.0.0.1:3039"
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

main.include_router(chat_router)