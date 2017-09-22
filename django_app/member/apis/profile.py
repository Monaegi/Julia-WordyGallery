from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from ..permissions import IsOwnerOrReadOnly
from ..serializers import UserInfoSerializers, UserInfoUpdateSerializers

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
        serializer_class = UserInfoUpdateSerializers(data=request.data, partial=True)
