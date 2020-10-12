# import locale


def format_currency(value):
    # TODO: Falta descobrir porque não funciona no heroku
    #       https://github.com/heroku/heroku-buildpack-locale/issues/13
    # return locale.currency(value, grouping=True)

    if value:
        value = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return value


# String models

# core
federative_unit_verbose_name = 'unidade federativa'

# sale
sale_order_verbose_name = 'ordem de venda'
sale_order_verbose_name_plural = 'ordens de venda'

# purchase
purchase_order_verbose_name = 'ordem de compra'
purchase_order_verbose_name_plural = 'ordens de compra'
