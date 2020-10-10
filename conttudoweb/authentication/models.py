from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin, Permission as authPermission, Group as authGroup)
from django.db import models
from django.utils.translation import gettext_lazy as _


class Group(authGroup):
    class Meta:
        proxy = True


class Permission(authPermission):
    class Meta:
        proxy = True
        verbose_name = 'permissão'
        verbose_name_plural = 'permissões'


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Os usuários devem ter um endereço de e-mail')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='endereço de e-mail',
        max_length=255,
        unique=True,
    )
    password = models.CharField('senha', max_length=128)
    date_of_birth = models.DateField('data de nascimento', null=True, blank=True)
    is_active = models.BooleanField('ativo?', default=True)
    is_staff = models.BooleanField('funcionário?', default=False)

    first_name = models.CharField('primeiro nome', max_length=30, blank=True)
    last_name = models.CharField('sobrenome', max_length=150, blank=True)

    # entity = models.ForeignKey('core.Entity', on_delete=models.SET_NULL, null=True,
    #                            verbose_name=Entity._meta.verbose_name+' atual')

    @property
    def username(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name() or self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class User(MyUser):
    class Meta:
        proxy = True
        verbose_name = _('user')
        verbose_name_plural = _('users')
