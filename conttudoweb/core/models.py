from django.core.exceptions import ValidationError
from django.db import models


class Entity(models.Model):
    name = models.CharField('nome', max_length=30, unique=True,
                            help_text='Algo como "Controle Pessoal" ou "Nome da Minha empresa".')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'entidade'


class People(models.Model):
    customer = models.BooleanField('cliente?', default=False)
    supplier = models.BooleanField('fornecedor?', default=False)
    name = models.CharField('nome', max_length=30, unique=True)

    def is_customer(self):
        return self.customer

    def is_supplier(self):
        return self.supplier

    def __str__(self):
        return self.name

    def clean(self):
        # Ao menos uma das opções deve ser escolhida! "cliente" ou "fornecedor"
        if self.customer is False and self.supplier is False:
            _msg_error = 'Ao menos uma das opções deve ser escolhida. "Cliente" ou "Fornecedor"'
            raise ValidationError({
                'customer': [_msg_error],
                'supplier': [_msg_error]
            })

    class Meta:
        verbose_name = 'pessoa'
