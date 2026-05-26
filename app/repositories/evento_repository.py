from config.database import SessionLocal
from sqlalchemy import text

def listar_eventos():

    db = SessionLocal()

    result = db.execute(text("""
        SELECT *
        FROM evento
    """)).fetchall()

    db.close()

    return result