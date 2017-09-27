from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from art.models import Art
from art.serializers import ArtListSerializers
from utils.permissions import IsMotifOwnerOrReadOnly
from ..models import Motif
from ..serializers import MotifListCreateSerializers, MotifUpdateSerializers

__all__ = (
    'MotifDetailRetrieveUpdateDestroyView',
)


class MotifDetailRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    모티프 세부페이지 조회 / 수정 / 삭제
    """
    # queryset = Motif.objects.get(pk=)
    serializer_class = MotifListCreateSerializers
    # 로그인한 사용자만 페이지 렌더, 작성자가 아니면 읽기 전용 권한.
    permission_classes = (IsAuthenticated, IsMotifOwnerOrReadOnly, )
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        """
        모티프 세부 정보와 연결된 작품 정보
        """
        art_info = Art.objects.get(pk=kwargs['art_pk'])
        artinfo_serializer = ArtListSerializers(art_info)
        motif_info = Motif.objects.get(pk=kwargs['motif_pk'])
        motifinfo_serializer = MotifListCreateSerializers(motif_info)

        content = {
            'artInfo': artinfo_serializer.data,
            'motifInfo': motifinfo_serializer.data
        }
        return Response(
            content,
            status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        """
        모티프 제목 수정
        """
        motif_info = Motif.objects.get(pk=kwargs['motif_pk'])
        # 모티프 작성자만 제목 수정 가능.
        if self.request.user == motif_info.motif_author:
            motifupdate_serializer = MotifUpdateSerializers
            motif_update = motifupdate_serializer(
                motif_info,
                data=request.data,
                partial=True
            )
            motif_update.is_valid(raise_exception=True)
            changed_motif = motif_update.save()

            changedmotif_serializer = MotifListCreateSerializers(changed_motif)
            content = {
                "detail": "모티프가 변경되었습니다.",
                "motifInfo": changedmotif_serializer.data
            }
            return Response(content, status=status.HTTP_200_OK)
        content = {
            "detail": "모티프를 수정할 권한이 없습니다."
        }
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        """
        모티프 삭제
        """
        queryset = Motif.objects.get(pk=kwargs['motif_pk'])

        if queryset.motif_author == self.request.user:
            queryset.delete()
            content = {
                "detail": "모티프가 삭제되었습니다."
            }
            return Response(content, status=status.HTTP_200_OK)
        content = {
            "detail": "모티프를 삭제할 권한이 없습니다."
        }
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
