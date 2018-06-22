from django.test import TestCase

from ..models import User


_email = 'user@user.com'


def create_user():
    user = User.objects.create_user(
        email=_email,
        password='demodemo'
    )
    return user


class UserModelTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_str(self):
        self.assertEqual(_email, str(self.user))
