from config.database import SessionLocal
from sqlalchemy import text

def salvar_memoria(pergunta, resposta):

    db = SessionLocal()

    db.execute(text("""
        INSERT INTO chatbot_memoria
        (pergunta, resposta)
        VALUES
        (:p, :r)
    """), {
        "p": pergunta,
        "r": resposta
    })

    db.commit()
    db.close()


def listar_memorias(limit=10):

    db = SessionLocal()

    result = db.execute(text(f"""
        SELECT *
        FROM chatbot_memoria
        ORDER BY id DESC
        LIMIT {limit}
    """)).fetchall()

    db.close()

    return result