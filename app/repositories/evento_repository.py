from app.core.database import SessionLocal
from sqlalchemy import text

def listar_eventos(limit=10):

    db = SessionLocal()

    result = db.execute(text("""
        SELECT *
        FROM eventos
        ORDER BY id DESC
        LIMIT :limit
    """), {"limit": limit}).fetchall()

    db.close()

    return result