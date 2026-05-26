from app.core.database import SessionLocal
from sqlalchemy import text

def listar_fluxos(limit=10):

    db = SessionLocal()

    result = db.execute(text("""
        SELECT
            id,
            data_lancamento AS data,
            data_efetivacao,
            descricao,
            status,
            tipo,
            valor,
            conta_id,
            evento_id
        FROM lancamentos
        ORDER BY id DESC
        LIMIT :limit
    """), {"limit": limit}).fetchall()

    db.close()

    return result