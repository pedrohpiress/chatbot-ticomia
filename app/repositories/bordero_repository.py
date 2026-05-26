from config.database import SessionLocal
from sqlalchemy import text

def listar_borderos():

    db = SessionLocal()

    result = db.execute(text("""
        SELECT *
        FROM bordero
    """)).fetchall()

    db.close()

    return result