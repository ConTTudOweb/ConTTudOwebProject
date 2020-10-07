import enum

from django.core.exceptions import ValidationError
from django.db import models

from conttudoweb.core.utils import federative_unit_verbose_name


class FederativeUnit(models.Model):
    initials = models.CharField('sigla', max_length=2, unique=True)
    name = models.CharField('nome', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = federative_unit_verbose_name
        ordering = ('name',)


class City(models.Model):
    name = models.CharField('nome', max_length=255)
    uf = models.ForeignKey('FederativeUnit', on_delete=models.PROTECT)

    def __str__(self):
        return "{}-{}".format(self.name, self.uf.initials)

    class Meta:
        verbose_name = 'cidade'
        unique_together = (('uf', 'name'),)
        ordering = ('name',)


# TODO: Colocar validação no cpf e maskara no telefone
# TODO: Após preencher o cep carregar o endereço
class People(models.Model):
    supplier_label = 'fornecedor'
    supplier_verbose_name = '%s?' % supplier_label
    customer_label = 'cliente'
    customer_verbose_name = '%s?' % customer_label

    class PersonTypes(enum.Enum):
        natural_person = 'F'
        juridical_person = 'J'

    customer = models.BooleanField(customer_verbose_name, default=False)
    supplier = models.BooleanField(supplier_verbose_name, default=False)
    name = models.CharField('nome', max_length=60, unique=True)
    person_type = models.CharField('tipo', max_length=1, null=True, blank=False, choices=[
        (PersonTypes.natural_person.value, 'Pessoa Física'),
        (PersonTypes.juridical_person.value, 'Pessoa Jurídica')
    ])
    federation_subscription_number = models.CharField('CPF/CNPJ', max_length=18, null=True, blank=True)
    state_subscription_number = models.CharField('RG/IE', max_length=18, null=True, blank=True)
    phone = models.CharField('telefone', max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    zip_code = models.CharField('CEP', max_length=10, null=True, blank=True)
    address = models.CharField('logradouro', max_length=255, null=True, blank=True)
    address_number = models.CharField('número', max_length=60, null=True, blank=True)
    complement = models.CharField('complemento', max_length=60, null=True, blank=True)
    neighborhood = models.CharField('bairro', max_length=60, null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name=City._meta.verbose_name, null=True,
                             blank=True)
    observation = models.TextField('observação', null=True, blank=True)

    def is_customer(self):
        return self.customer

    def is_supplier(self):
        return self.supplier

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        self._meta.get_field('person_type').default = self.PersonTypes.natural_person.value
        super().__init__(*args, **kwargs)

    def clean(self):
        # Ao menos uma das opções deve ser escolhida! "cliente" ou "fornecedor"
        if self.customer is False and self.supplier is False:
            _msg_error = 'Ao menos uma das opções deve ser escolhida. "Cliente" ou "Fornecedor"'
            raise ValidationError({
                'customer': [_msg_error],
                'supplier': [_msg_error]
            })

    class Meta:
        verbose_name = 'Cliente / Fornecedor'
        verbose_name_plural = 'Clientes / Fornecedores'
