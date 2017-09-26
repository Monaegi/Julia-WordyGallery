from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from member.permissions import IsOwnerOrReadOnly
from ..serializers import MotifListCreateSerializers

__all__ = (
    'MotifListCreateView',
    'MotifCreateUpdateDestroyView',
)


class MotifListCreateView(generics.ListCreateAPIView):
    """
    모티브 리스트 조회 및 생성
    """
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass


class MotifCreateUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    모티프 수정, 삭제
    """
    serializer_class = MotifListCreateSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
