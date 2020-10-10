from django.apps import AppConfig


class SaleConfig(AppConfig):
    name = 'conttudoweb.sale'
    verbose_name = 'Vendas'

    def ready(self):
        import conttudoweb.sale.signals
