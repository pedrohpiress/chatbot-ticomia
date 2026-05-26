from app.core.database import SessionLocal
from sqlalchemy import text

def listar_borderos(limit=10):

    db = SessionLocal()

    result = db.execute(text("""
        SELECT *
        FROM pagamentos_despesa
        ORDER BY id DESC
        LIMIT :limit
    """), {"limit": limit}).fetchall()

    db.close()

    return result