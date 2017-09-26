from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from rest_framework import serializers

User = get_user_model()

__all__ = (
    'CustomAuthTokenSerializers',
)


class CustomAuthTokenSerializers(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=50,
        help_text="example@example.com",
    )
    password = serializers.CharField(
        max_length=50,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password'
        )
        read_only = (
            'username',
        )

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username:
            raise serializers.ValidationError({
                "detail": "이메일을 입력하세요."
            })
        elif validate_email(username):
            if data['username'].errors:
                raise serializers.ValidationError({
                    "detail": "유효한 이메일 계정을 입력하세요."
                })

        if username and password:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if not user.is_active:
                    msg = "계정이 비활성화 상태입니다. 이메일을 확인하세요."
                    raise serializers.ValidationError({
                        "detail": msg
                    })
            else:
                msg = "일치하는 계정정보가 없습니다."
                raise serializers.ValidationError({
                    "detail": msg
                })
        else:
            msg = "이메일과 비밀번호를 입력해주세요."
            raise serializers.ValidationError({
                "detail": msg
            })

        data['user'] = user
        return data
