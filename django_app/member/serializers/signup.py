from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from rest_framework import serializers

User = get_user_model()

__all__ = (
    'UserSignupSerializers',
)


class UserSignupSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(
        max_length=50,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        max_length=50,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'img_profile',
            'password1',
            'password2',
        )

    def validate(self, data):
        username = data.get('username')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # 계정 존재여부 검증
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "detail": "이미 존재하는 계정입니다."
            })
        # 이메일 계정 검증
        elif not username:
            raise serializers.ValidationError({
                "detail": "이메일을 입력하세요."
            })
        elif validate_email(username):
            raise serializers.ValidationError({
                "detail": "유효한 이메일 계정을 입력하세요."
            })

        # 비밀번호 일치여부 검증
        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError({
                    "detail": "비밀번호와 확인용 비밀번호가 일치하지 않습니다."
                })
        else:
            raise serializers.ValidationError({
                "detail": "비밀번호와 확인용 비밀번호를 모두 입력해주세요."
            })
        return data

    def save(self):
        """
        입력한 정보로 DB에 사용자 정보를 저장
        """
        user = User.objects.create_user(
            username=self.validated_data.get('username'),
            password=self.validated_data.get('password2'),
            name=self.validated_data.get('name'),
            img_profile=self.validated_data.get('img_profile', ''),
            email=self.validated_data.get('email', '')
        )
        return user
