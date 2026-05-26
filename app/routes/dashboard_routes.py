from fastapi import APIRouter
from app.services.dashboard_service import resumo_dashboard

router = APIRouter(
    prefix="/dashboard-ai",
    tags=["Dashboard IA"]
)

@router.get("/resumo")
def resumo():

    return resumo_dashboard()