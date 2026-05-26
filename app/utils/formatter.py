def moeda(valor):

    try:
        valor = float(valor)

        return f"R$ {valor:,.2f}" \
            .replace(",", "X") \
            .replace(".", ",") \
            .replace("X", ".")

    except:
        return "R$ 0,00"