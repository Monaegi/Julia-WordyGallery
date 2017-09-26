from django.contrib.auth import authenticate, login as django_login, get_user_model, logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.auth import CustomAuthTokenSerializers
from ..serializers.profile import UserInfoSerializers

User = get_user_model()

__all__ = (
    'CustomAuthTokenView',
    'UserLogoutView',
)


class CustomAuthTokenView(APIView):
    """
    사용자가 기입한 이메일, 비밀번호와
    일치하는 유저정보가 있으면 토큰, 유저정보 반환
    """
    # Token 인증 기반
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)
    serializer_class = CustomAuthTokenSerializers

    def post(self, request, format=None, *args, **kwargs):
        """
        유저가 입력한 이메일계정, 비밀번호를 받아와 일치하는 정보가 있을 경우
        토큰과 관련 정보를 json으로 돌려준다.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # username, password가 유효한 정보인지 확인
        if authenticate(
                username=request.data.get('username'),
                password=request.data.get('password')
        ):
            token, token_created = Token.objects.get_or_create(
                user=user
            )
            # validation을 통과한 user정보를 유저정보용 시리얼라이저에 넣음
            user_serializer = UserInfoSerializers(user)
            # 받은 정보로 장고 로그인
            django_login(request, user)
            content = {
                'token': token.key,
                'userInfo': user_serializer.data,
            }
            return Response(
                content,
                status=status.HTTP_200_OK
            )
        else:
            # authenticate()를 통과하지 못한 경우 400 코드 응답을 돌려줌
            content = {
                "detail": "이메일 또는 비밀번호가 일치하지 않습니다."
            }
            return Response(
                content,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserLogoutView(APIView):
    """
    로그인한 사용자가 로그아웃 버튼을 누르면 토큰을 삭제하고
    사용자를 로그아웃시킨다.
    """

    def logout(self, request):
        """인스턴스 메서드로 토큰을 지우는 logout 메서드 정의"""
        try:
            request.user.auth_token.delete()
        except (ObjectDoesNotExist, AttributeError):
            content = {
                "detail": "토큰이 존재하지 않습니다."
            }
            django_logout(request)
            return Response(content, status=status.HTTP_200_OK)
        django_logout(request)
        content = {
            "detail": "성공적으로 로그아웃되었습니다.",
        }
        return Response(content, status=status.HTTP_200_OK)

    def get(self, request):
        """
        get요청으로 logout 인스턴스 메서드를 실행.
        """
        return self.logout(request)
