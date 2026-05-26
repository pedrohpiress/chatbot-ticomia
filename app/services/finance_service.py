from app.core.database import SessionLocal
from app.repositories.conta_repository import listar_contas
from app.repositories.despesa_repository import listar_despesas
from app.repositories.evento_repository import listar_eventos
from app.repositories.fluxo_repository import listar_fluxos
from sqlalchemy import text
from app.utils.formatter import moeda


def _get_value(item, key, default=""):
    if isinstance(item, dict):
        return item.get(key, default)

    return getattr(item, key, default)


def _normalizar_texto(valor, limite=48):
    texto = str(valor or "").strip()

    if len(texto) > limite:
        return texto[: limite - 3].rstrip() + "..."

    return texto


def _scalar(query):
    db = SessionLocal()

    try:
        return db.execute(text(query)).scalar() or 0
    finally:
        db.close()


def _resumo_indicadores():
    saldo_total = _scalar(
        """
        SELECT COALESCE(SUM(saldo_atual), 0)
        FROM contas_bancarias
        """
    )

    total_despesas = _scalar(
        """
        SELECT COALESCE(SUM(valor_total), 0)
        FROM despesas
        """
    )

    despesas_em_aberto = _scalar(
        """
        SELECT COALESCE(SUM(saldo_restante), 0)
        FROM despesas
        WHERE status IN ('ABERTA', 'PARCIAL')
        """
    )

    entradas = _scalar(
        """
        SELECT COALESCE(SUM(CASE WHEN tipo = 'ENTRADA' THEN valor ELSE 0 END), 0)
        FROM lancamentos
        """
    )

    saidas = _scalar(
        """
        SELECT COALESCE(SUM(CASE WHEN tipo = 'SAIDA' THEN valor ELSE 0 END), 0)
        FROM lancamentos
        """
    )

    return {
        "saldo_total": float(saldo_total or 0),
        "total_despesas": float(total_despesas or 0),
        "despesas_em_aberto": float(despesas_em_aberto or 0),
        "entradas": float(entradas or 0),
        "saidas": float(saidas or 0),
        "fluxo_liquido": float((entradas or 0) - (saidas or 0))
    }


def _resumir_contas():
    contas = listar_contas(limit=5)

    linhas = []

    for conta in contas:
        linhas.append(
            f"- {_normalizar_texto(_get_value(conta, 'nome'))}: {moeda(_get_value(conta, 'saldo'))}"
        )

    return linhas


def _resumir_despesas():
    despesas = listar_despesas(limit=5)

    linhas = []

    for despesa in despesas:
        descricao = _normalizar_texto(_get_value(despesa, 'descricao'))
        valor = moeda(_get_value(despesa, 'valor'))
        status = _normalizar_texto(_get_value(despesa, 'status'))

        linhas.append(f"- {descricao}: {valor} ({status})")

    return linhas


def _resumir_movimentos():
    movimentos = listar_fluxos(limit=10)

    linhas = []
    entradas = 0.0
    saidas = 0.0

    for movimento in movimentos:
        tipo = _normalizar_texto(_get_value(movimento, 'tipo'))
        valor = float(_get_value(movimento, 'valor') or 0)
        descricao = _normalizar_texto(_get_value(movimento, 'descricao'))

        if tipo == 'ENTRADA':
            entradas += valor
        elif tipo == 'SAIDA':
            saidas += valor

        linhas.append(f"- {tipo}: {moeda(valor)} | {descricao}")

    return linhas, entradas, saidas


def _resumir_evento_ativo():
    eventos = listar_eventos(limit=1)

    if not eventos:
        return "nenhum evento ativo encontrado"

    evento = eventos[0]

    nome = _normalizar_texto(
        _get_value(evento, "nome")
        or _get_value(evento, "descricao")
        or _get_value(evento, "titulo")
        or _get_value(evento, "id")
    )

    status = _normalizar_texto(_get_value(evento, "status"))

    if status:
        return f"{nome} ({status})"

    return nome


def _classificar_intencao(pergunta):
    texto = (pergunta or "").lower()
    secoes = set()

    if any(palavra in texto for palavra in ("saldo", "conta", "banco", "disponivel", "disponível")):
        secoes.update({"indicadores", "contas"})

    if any(palavra in texto for palavra in ("despesa", "gasto", "custo", "pagamento", "pagar")):
        secoes.update({"indicadores", "despesas", "movimentos"})

    if any(palavra in texto for palavra in ("fluxo", "caixa", "moviment", "entrada", "saida", "saída")):
        secoes.update({"indicadores", "movimentos"})

    if any(palavra in texto for palavra in ("evento", "obra", "projeto", "ativo", "campanha")):
        secoes.update({"indicadores", "eventos", "despesas"})

    if not secoes:
        secoes.update({"indicadores", "contas", "despesas", "movimentos", "eventos"})

    return secoes


def gerar_contexto_financeiro(pergunta=""):

    secoes = _classificar_intencao(pergunta)
    indicadores = _resumo_indicadores()
    linhas = []

    if "indicadores" in secoes:
        linhas.append("INDICADORES:")
        linhas.append(f"- saldo total: {moeda(indicadores['saldo_total'])}")
        linhas.append(f"- total despesas: {moeda(indicadores['total_despesas'])}")
        linhas.append(f"- despesas em aberto: {moeda(indicadores['despesas_em_aberto'])}")
        linhas.append(f"- entradas: {moeda(indicadores['entradas'])}")
        linhas.append(f"- saidas: {moeda(indicadores['saidas'])}")
        linhas.append(f"- fluxo liquido: {moeda(indicadores['fluxo_liquido'])}")

    if "contas" in secoes:
        linhas.append("TOP 5 CONTAS:")
        linhas.extend(_resumir_contas())

    if "despesas" in secoes:
        linhas.append("MAIORES DESPESAS:")
        linhas.extend(_resumir_despesas())

    if "movimentos" in secoes:
        movimentos, entradas, saidas = _resumir_movimentos()
        linhas.append("ULTIMAS MOVIMENTACOES:")
        linhas.extend(movimentos)
        linhas.append(f"- resumo recente: entradas {moeda(entradas)} | saidas {moeda(saidas)}")

    if "eventos" in secoes:
        linhas.append("EVENTO ATIVO:")
        linhas.append(f"- {_resumir_evento_ativo()}")

    return "\n".join(linhas)[:5000]