def entrada_ou_saida(valor):

    valor = float(valor or 0)

    if valor >= 0:
        return "ENTRADA"

    return "SAIDA"