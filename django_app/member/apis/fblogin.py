import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserInfoSerializers

__all__ = (
    'FBTokenUserInfoAPIView',
    'FacebookLoginAPIView',
)

User = get_user_model()


class FBTokenUserInfoAPIView(APIView):
    """
    페이스북으로 로그인한 유저의 토큰값과 정보를 반환
    """

    def post(self, request):
        token_string = request.data.get('token')
        try:
            token = Token.objects.get(key=token_string)
        except Token.DoesNotExist:
            raise APIException('토큰이 유효하지 않습니다.')
        user = token.user
        user_serializer = UserInfoSerializers(user)
        content = {
            'token': token.key,
            'userInfo': user_serializer.data
        }
        return Response(content, status=status.HTTP_200_OK)


class FacebookLoginAPIView(APIView):
    FACEBOOK_APP_ID = settings.FACEBOOK_APP_ID
    FACEBOOK_SECRET_CODE = settings.FACEBOOK_API_SECRET_CODE

    # 앱 액세스 토큰 생성
    APP_ACCESS_TOKEN = '{}|{}'.format(
        FACEBOOK_APP_ID,
        FACEBOOK_SECRET_CODE
    )

    def post(self, request):
        """
        페이스북 로그인 API를 사용하여 받아온 사용자정보로
        장고에 로그인시킨다.
        """
        fb_token = request.data.get('token')
        if not fb_token:
            raise APIException({
                "detail": "액세스 토큰이 필요합니다."
            })
        # 프론트로부터 받은 액세스 토큰을 페이스북의 debug_token API로 전송
        self.debug_token(fb_token)
        # 토큰을 사용하여 유저의 정보를 받아온다.
        user_info = self.get_user_info(fb_token=fb_token)

        if User.objects.filter(username=user_info['id']).exists():
            user = User.objects.get(username=user_info['id'])

        # 모델 매니저를 통해 페이스북 사용자 정보를 저장하고 유저 생성
        else:
            user = User.objects.get_or_create_facebook_user(user_info)

        # 장고 로그인용 토큰 생성
        dj_token, djtoken_created = Token.objects.get_or_create(user=user)
        user_serializer = UserInfoSerializers(user)

        # 토큰과 사용자정보 반환
        content = {
            'token': dj_token.key,
            'userInfo': user_serializer.data
        }
        return Response(
            content,
            status=status.HTTP_200_OK
        )

    def debug_token(self, fb_token):
        """
        액세스 토큰을 디버그용 URL로 보내 유효성 검사를 실시
        """
        # 디버그할 액세스 토큰을 보낼 URL
        url_debug_token = "https://graph.facebook.com/debug_token"
        # 액세스 토큰과 앱 아이디를 파라미터로 보내기 위해 딕셔너리에 삽입
        url_debug_token_params = {
            'input_token': fb_token,
            'access_token': self.APP_ACCESS_TOKEN
        }

        # requests 모듈을 사용하여 response를 받음
        response = requests.get(
            url_debug_token,
            url_debug_token_params
        )
        # 받은 response를 json 구조로 출력
        result = response.json()
        if 'error' in result or 'error' in result['data']:
            raise APIException({
                "detail": "토큰이 유효하지 않습니다."
            })
        return result

    def get_user_info(self, fb_token):
        """
        액세스 토큰을 사용하여 페이스북에 등록된 사용자 정보를 불러온다
        """
        url_user_info = "https://graph.facebook.com/v2.9/me"
        url_user_info_params = {
            "access_token": fb_token,
            # 받아올 정보항목의 스코프를 생성
            "fields": ','.join([
                'id',
                'name',
                'first_name',
                'last_name',
                'picture.type(large)',
            ])
        }
        # 요청을 보내 response 반환
        response = requests.get(
            url_user_info,
            url_user_info_params
        )
        result = response.json()
        return result
