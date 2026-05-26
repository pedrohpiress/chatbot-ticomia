from repositories.conta_repository import listar_contas
from repositories.despesa_repository import listar_despesas
from repositories.fluxo_repository import listar_fluxos
from repositories.evento_repository import listar_eventos
from repositories.bordero_repository import listar_borderos

def resumo_dashboard():

    contas = listar_contas()
    despesas = listar_despesas()
    fluxos = listar_fluxos()
    eventos = listar_eventos()
    borderos = listar_borderos()

    total_contas = sum([
        float(c.saldo or 0)
        for c in contas
    ])

    total_despesas = sum([
        float(d.valor or 0)
        for d in despesas
    ])

    total_entradas = sum([
        float(f.valor or 0)
        for f in fluxos
        if f.tipo == "ENTRADA"
    ])

    total_saidas = sum([
        float(f.valor or 0)
        for f in fluxos
        if f.tipo == "SAIDA"
    ])

    return {
        "saldo_total": total_contas,
        "total_despesas": total_despesas,
        "total_entradas": total_entradas,
        "total_saidas": total_saidas,
        "eventos": len(eventos),
        "borderos": len(borderos)
    }