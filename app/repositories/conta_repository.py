from config.database import SessionLocal
from sqlalchemy import text

def listar_contas():

    db = SessionLocal()

    result = db.execute(text(\"\"\"
        SELECT *
        FROM conta
    \"\"\")).fetchall()

    db.close()

    return result