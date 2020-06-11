from django_tenants.test.cases import FastTenantTestCase

from ..models import MyUser

_email = 'user@user.com'


def create_user():
    user = MyUser.objects.create_user(
        email=_email,
        password='demodemo'
    )
    return user


class UserModelTest(FastTenantTestCase):
    def setUp(self):
        self.user = create_user()

    def test_create(self):
        self.assertTrue(MyUser.objects.exists())

    def test_str(self):
        self.assertEqual(_email, str(self.user))
