from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

__all__ = (
    'UserInfoSerializers',
    'UserInfoUpdateSerializers',
)


class UserInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'name',
            'img_profile',
            'email',
            'password',
            'is_active',
            'is_admin'
        )
        read_only = (
            'username'
        )
        write_only = (
            'password'
        )


class UserInfoUpdateSerializers(serializers.ModelSerializer):
    new_password1 = serializers.CharField(
        max_length=50,
        style={'input_type': 'password'},
    )
    new_password2 = serializers.CharField(
        max_length=50,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'name',
            'img_profile',
            'password',
            'new_password1',
            'new_password2'
        )
        read_only_fields = (
            'username',
        )

    # 입력값의 검증만 실시.
    def validate(self, data):
        password = data.get('password')
        if data.get('new_password1') == '' and data.get('new_password2') == '':
            data.pop('password')
            data.pop('new_password1')
            data.pop('new_password2')
        elif data.get('new_password1') != data.get('new_password2'):
            return serializers.ValidationError(
                "새로운 비밀번호와 확인용 비밀번호가 일치하지 않습니다."
            )
        return data
