# import locale


def format_currency(value):
    # TODO: Falta descobrir porque não funciona no heroku
    #       https://github.com/heroku/heroku-buildpack-locale/issues/13
    # return locale.currency(value, grouping=True)
    return value
