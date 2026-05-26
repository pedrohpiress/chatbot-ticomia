from sqlalchemy import text

from app.core.database import engine


def listar_contas(limit=5):

    with engine.connect() as db:

        result = db.execute(text("""
            SELECT
                id,
                nome,
                saldo_atual
            FROM contas_bancarias
            ORDER BY saldo_atual DESC
            LIMIT :limit
        """), {"limit": limit})

        contas = []

        for row in result:
            contas.append({
                "id": row.id,
                "nome": row.nome,
                "saldo": float(row.saldo_atual or 0)
            })

        return contas