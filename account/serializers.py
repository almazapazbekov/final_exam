from rest_framework import serializers
from rest_framework.authtoken.views import obtain_auth_token

from account.models import Author, user


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(max_length=20, write_only=True)
    password_2 = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Author
        fields = "__all__"
        read_only_fields = ['user', ]

    def validate(self, data):
        if data['password'] != data['password_2']:
            raise serializers.ValidationError('пароли должны совпадать')
        return data

    def create(self, validated_data):
        try:
            new_user = user(
                username=validated_data['username'],
            )
            new_user.set_password(validated_data['password'])
            new_user.save()
        except Exception as e:
            raise serializers.ValidationError(f'Не удаётся создать пользователя. {e}')
        else:
            new_author = Author.objects.create(
                user=new_user
            )
            return new_author


# class TokenSerializer(serializers.ModelSerializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

