from repositories.conta_repository import listar_contas
from repositories.despesa_repository import listar_despesas
from repositories.fluxo_repository import listar_fluxos

def gerar_contexto_financeiro():

    contas = listar_contas()
    despesas = listar_despesas()
    fluxos = listar_fluxos()

    contexto = ""

    contexto += "\\nCONTAS:\\n"

    for c in contas:
        contexto += (
            f"Conta: {c.nome} | "
            f"Saldo: {c.saldo}\\n"
        )

    contexto += "\\nDESPESAS:\\n"

    for d in despesas:
        contexto += (
            f"{d.descricao} | "
            f"{d.valor} | "
            f"{d.status}\\n"
        )

    contexto += "\\nFLUXOS:\\n"

    for f in fluxos:
        contexto += (
            f"{f.tipo} | "
            f"{f.valor} | "
            f"{f.descricao}\\n"
        )

    return contexto