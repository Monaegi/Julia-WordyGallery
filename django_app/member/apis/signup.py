from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserInfoSerializers
from ..serializers import UserSignupSerializers

__all__ = (
    "UserSignupView",
)


class UserSignupView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    # def get_serializer_class(self):
    #     if self.request == 'GET':
    #         return UserInfoSerializers
    #     elif self.request == 'POST':
    #         return UserSignupSerializers
    #
    # def get(self, request, format=None, *args, **kwargs):
    #     serializer = self.get_serializer_class()
    #     serializer.is_valid(raise_exception=True)
    #     content = {
    #         "UserList": serializer.data,
    #     }
    #     return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer_class = UserSignupSerializers
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)

        user_serializer = UserInfoSerializers(user)
        content = {
            'userInfo': user_serializer.data,
        }
        return Response(
            content,
            status=status.HTTP_201_CREATED
        )
