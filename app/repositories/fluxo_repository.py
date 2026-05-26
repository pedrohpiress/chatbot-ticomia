from config.database import SessionLocal
from sqlalchemy import text

def listar_fluxos():

    db = SessionLocal()

    result = db.execute(text(\"\"\"
        SELECT *
        FROM fluxo_caixa
        ORDER BY id DESC
        LIMIT 200
    \"\"\")).fetchall()

    db.close()

    return result