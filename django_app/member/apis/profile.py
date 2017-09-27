from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from ..serializers import UserInfoSerializers, UserInfoUpdateSerializers
from utils.permissions import IsOwnerOrReadOnly

User = get_user_model()

__all__ = (
    'UserInfoView',
)


class UserInfoView(generics.RetrieveUpdateDestroyAPIView):
    """
    사용자 프로필 페이지 뷰
    get : 모든 사용자가 다른 사용자의 프로필 정보를 볼 수 있다.
    update : 자기자신의 프로필만 수정할 수 있다.
    delete : 자기자신의 프로필(계정)만 삭제할 수 있다.
    """
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,  # 객체가 자기자신일 경우에는 수정, 삭제 가능.
    )
    serializer_class = UserInfoSerializers

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        # print(user.has_object_permission())

        serializer_class = self.serializer_class
        serializer = serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        content = {
            'userInfo': serializer.data,
        }
        return Response(content, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        serializer_class = UserInfoUpdateSerializers
        serializer = serializer_class(user, data=request.data, partial=True)
        parser_classes = (MultiPartParser, FormParser,)

        # (1) 비밀번호가 다 있을 경우
        if request.data.get('password', default=None) and request.data.get(
                'new_password1', default=None) and request.data.get('new_password2', default=None):
            # 비번 체크 후 새로 설정
            if user.check_password(request.data.get('password')):
                user.set_password(request.data.get('new_password2'))
                serializer.is_valid(raise_exception=True)
                update_userinfo = serializer.save()

                # 이름 저장(수정하지 않으면 본래값)
                update_userinfo.name = user.name if not request.data.get(
                    'name', default=None) else request.data.get('name')

                # 이미지 저장(수정하지 않으면 본래값)
                update_userinfo.img_profile = user.img_profile if not request.data.get(
                    'img_profile', default=None) else request.data.get('img_profile')
                update_userinfo.save()

                # 유저 저장
                user_serializer = UserInfoSerializers(update_userinfo, partial=True)
                content = {
                    "detail": "회원정보가 변경되었습니다. 재로그인해주세요.",
                    "userInfo": user_serializer.data,
                }
                return Response(content, status=status.HTTP_200_OK)

            # 기존 비번이 일치하지 않을 경우 - 400
            else:
                content = {
                    "detail": "기존 비밀번호가 일치하지 않습니다."
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # (2) 비번 입력했으나 하나라도 없을 경우
        elif request.data.get('password', default=None) or request.data.get(
                'new_password1', default=None) or request.data.get('new_password2', default=None):
            content = {
                "detail": "비밀번호를 변경하시려면 기존 비밀번호와 새 비밀번호 필드를 모두 입력해주세요."
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # (3) 비번 값이 하나도 없을 경우 (이름, 프로필이미지만 변경하는 경우)
        else:
            serializer.is_valid(raise_exception=True)
            update_userinfo = serializer.save()
            # 닉네임 및 이미지 저장
            update_userinfo.name = user.name if not request.data.get(
                'name', default=None) else request.data.get('name')
            update_userinfo.save()

            update_userinfo.img_profile = user.img_profile if not request.data.get(
                'img_profile', default=None) else request.data.get('img_profile')

            # 유저 저장
            update_userinfo.save()
            user_serializer = UserInfoSerializers(update_userinfo, partial=True)
            content = {
                "detail": "사용자 정보가 변경되었습니다.",
                "userInfo": user_serializer.data,
            }
            return Response(content, status=status.HTTP_200_OK)

    # 계정 탈퇴
    def delete(self, request, *args, **kwargs):
        content = {
            "detail": "계정이 삭제되었습니다."
        }
        super().destroy(self, request, *args, **kwargs)
        return Response(content, status=status.HTTP_200_OK)
