from rest_auth.models import TokenModel
from rest_framework import serializers

from .models import MyUser


class UserDetailsSerializer(serializers.ModelSerializer):
    user_permissions = serializers.SerializerMethodField('get_user_permissions')

    def get_user_permissions(self, user: MyUser):
        return user.get_all_permissions()

    class Meta:
        model = MyUser
        fields = ['pk', 'first_name', 'last_name', 'email', 'date_of_birth', 'user_permissions']
        read_only_fields = ['email', 'user_permissions']


class TokenSerializer(serializers.ModelSerializer):
    # user = UserDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = TokenModel
        fields = '__all__'
