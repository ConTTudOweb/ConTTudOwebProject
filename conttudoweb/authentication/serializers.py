from rest_auth.models import TokenModel
from rest_framework import serializers

from .models import MyUser


class UserSerializer(serializers.ModelSerializer):
    # user_permissions = serializers.SerializerMethodField()
    #
    # def get_user_permissions(self, user: MyUser):
    #     if hasattr(user, 'user_permissions'):
    #         return user.user_permissions.all().values_list('content_type__app_label', 'codename')
    #     return []

    class Meta:
        model = MyUser
        exclude = ('password',)


class TokenSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = TokenModel
        fields = '__all__'
