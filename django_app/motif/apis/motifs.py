from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from art.models import Art
from art.serializers import ArtListSerializers
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
    serializer_class = MotifListCreateSerializers
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        # 해당 작품 정보
        art_info = Art.objects.get(id=kwargs['art_pk'])
        artinfo_serializer = ArtListSerializers(art_info)
        # 작품에 등록된 모티프 목록
        motif_list = art_info.motif_set.all()
        motiflist_serializer = self.serializer_class(
            motif_list,
            many=True
        )

        content = {
            "art_info": artinfo_serializer.data,
            "motifList": motiflist_serializer.data
        }
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        모티프 생성
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        motif = serializer.validated_data  # Ordered Dict

        motif_serializer = MotifListCreateSerializers(motif)
        # 새로운 모티프 저장
        motif_serializer.save(motif)
        content = {
            "detail": "새로운 모티프를 생성했습니다. 이야기를 시작하세요!",
            'motifInfo': motif_serializer.data
        }
        return Response(content, status=status.HTTP_200_OK)


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
