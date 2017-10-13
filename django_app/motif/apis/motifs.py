from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from art.models import Art
from art.serializers import ArtListSerializers
from utils.permissions import IsOwnerOrReadOnly, IsMotifOwnerOrReadOnly
from ..models import Motif
from ..serializers import MotifListCreateSerializers, MotifUpdateSerializers, MotifDetailSerializers

__all__ = (
    # 모티프 리스트 조회 및 생성
    'MotifListCreateView',

    # 모티프 세부페이지 조회
    'MotifDetailRetrieveView',

    # 모티프 세부페이지 수정 / 삭제
    # 'MotifDetailUpdateDestroyView',
)


class MotifListCreateView(generics.ListCreateAPIView):
    """
    모티브 리스트 조회 및 생성
    """
    serializer_class = MotifListCreateSerializers
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        # 해당 작품 정보
        art_info = Art.objects.get(id=kwargs['art_pk'])
        # 작품에 등록된 모티프 목록
        motif_list = art_info.motif_set.all()
        motiflist_serializer = MotifDetailSerializers(
            motif_list,
            many=True
        )

        content = {
            "motifList": motiflist_serializer.data
        }
        return Response(content, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        객체 생성 메서드
        """
        queryset = Motif.objects.filter(name_motif=self.kwargs['name_motif'])
        if queryset.exists():
            raise ValidationError({
                "detail": "이미 존재하는 모티프입니다. 새로운 주제를 생성해주세요."
            })
        serializer.save(data=self.request.data)

    def post(self, request, *args, **kwargs):
        """
        모티프 생성
        """
        newmotif_serializer = self.serializer_class(data=request.data)
        newmotif_serializer.is_valid(raise_exception=True)
        new_motif = newmotif_serializer.save()

        motif_serializer = MotifDetailSerializers(new_motif)
        # 새로운 모티프 저장
        content = {
            "detail": "새로운 모티프를 생성했습니다. 이야기를 시작하세요!",
            'motifInfo': motif_serializer.data
        }
        return Response(content, status=status.HTTP_200_OK)


class MotifDetailRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """
    모티프 세부페이지 조회
    """
    serializer_class = MotifDetailSerializers
    # 로그인한 사용자만 페이지 렌더, 작성자가 아니면 읽기 전용 권한.
    permission_classes = (IsMotifOwnerOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        """
        모티프 세부 정보와 연결된 작품 정보
        """
        motif_info = Motif.objects.get(pk=kwargs['motif_pk'])
        motifinfo_serializer = self.serializer_class(motif_info)

        content = {
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
        if self.request.user.is_authenticated:
            if self.request.user == motif_info.motif_author or self.request.user.is_admin:
                motifupdate_serializer = MotifUpdateSerializers
                motif_update = motifupdate_serializer(motif_info, data=request.data, partial=True)
                motif_update.is_valid(raise_exception=True)
                motif_update.save()

                changed_motif = MotifDetailSerializers(motif_update)
                content = {
                    "detail": "모티프가 변경되었습니다.",
                    "motifInfo": changed_motif.data
                }
                return Response(content, status=status.HTTP_200_OK)
            content = {
                "detail": "모티프를 수정할 권한이 없습니다."
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        content = {
            "detail": "수정하려면 로그인을 해주세요."
        }
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        """
        모티프 삭제
        """
        content = {
            "detail": "모티프가 삭제되었습니다."
        }
        super().destroy(self, request, *args, **kwargs)
        return Response(content, status=status.HTTP_200_OK)


# class MotifDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     모티프 세부페이지 수정, 삭제
#     """
#     serializer_class = MotifListCreateSerializers
#     permission_classes = (IsMotifOwnerOrReadOnly,)
#
#     def put(self, request, *args, **kwargs):
#         """
#         모티프 제목 수정
#         """
#         motif_info = Motif.objects.get(pk=kwargs['motif_pk'])
#         # 모티프 작성자만 제목 수정 가능.
#         if self.request.user == motif_info.name_user:
#             motifupdate_serializer = MotifUpdateSerializers
#             motif_update = motifupdate_serializer(motif_info, data=request.data, partial=True)
#             motif_update.is_valid(raise_exception=True)
#             motif_update.save()
#
#             changed_motif = MotifDetailSerializers(motif_update)
#             content = {
#                 "detail": "모티프가 변경되었습니다.",
#                 "motifInfo": changed_motif.data
#             }
#             return Response(content, status=status.HTTP_200_OK)
#         content = {
#             "detail": "모티프를 수정할 권한이 없습니다."
#         }
#         return Response(content, status=status.HTTP_401_UNAUTHORIZED)
#
#     def delete(self, request, *args, **kwargs):
#         """
#         모티프 삭제
#         """
#         content = {
#             "detail": "모티프가 삭제되었습니다."
#         }
#         super().destroy(self, request, *args, **kwargs)
#         return Response(content, status=status.HTTP_200_OK)
