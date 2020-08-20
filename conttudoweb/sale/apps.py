from django.apps import AppConfig


class SaleConfig(AppConfig):
    name = 'conttudoweb.sale'
    verbose_name = 'vendas'

    def ready(self):
        import conttudoweb.sale.signals
