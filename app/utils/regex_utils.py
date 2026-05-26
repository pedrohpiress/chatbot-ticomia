import re

def limpar_moeda(valor):

    if valor is None:
        return 0

    valor = str(valor)

    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    valor = re.sub(r"[^0-9.-]", "", valor)

    try:
        return float(valor)
    except:
        return 0