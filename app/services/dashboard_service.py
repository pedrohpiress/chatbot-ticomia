from app.core.database import SessionLocal
from app.repositories.conta_repository import listar_contas
from app.repositories.despesa_repository import listar_despesas
from app.repositories.fluxo_repository import listar_fluxos
from app.repositories.evento_repository import listar_eventos
from app.repositories.bordero_repository import listar_borderos
from sqlalchemy import text


def _get_value(item, key, default=0):
    if isinstance(item, dict):
        return item.get(key, default)

    return getattr(item, key, default)

def resumo_dashboard():

    db = SessionLocal()

    try:
        total_contas = db.execute(
            text("""
            SELECT COALESCE(SUM(saldo_atual), 0)
            FROM contas_bancarias
            """)
        ).scalar() or 0

        total_despesas = db.execute(
            text("""
            SELECT COALESCE(SUM(valor_total), 0)
            FROM despesas
            """)
        ).scalar() or 0

        total_entradas = db.execute(
            text("""
            SELECT COALESCE(SUM(CASE WHEN tipo = 'ENTRADA' THEN valor ELSE 0 END), 0)
            FROM lancamentos
            """)
        ).scalar() or 0

        total_saidas = db.execute(
            text("""
            SELECT COALESCE(SUM(CASE WHEN tipo = 'SAIDA' THEN valor ELSE 0 END), 0)
            FROM lancamentos
            """)
        ).scalar() or 0

        total_eventos = db.execute(
            text("SELECT COUNT(*) FROM eventos")
        ).scalar() or 0

        total_borderos = db.execute(
            text("SELECT COUNT(*) FROM pagamentos_despesa")
        ).scalar() or 0
    finally:
        db.close()

    return {
        "saldo_total": float(total_contas or 0),
        "total_despesas": float(total_despesas or 0),
        "total_entradas": float(total_entradas or 0),
        "total_saidas": float(total_saidas or 0),
        "eventos": int(total_eventos or 0),
        "borderos": int(total_borderos or 0)
    }