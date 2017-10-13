from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from art.serializers import ArtListSerializers
from utils.permissions.motif_perms import IsCommentOwnerOrReadOnly
from ..serializers import CommentDetailSerializers, CommentUpdateDestroySerializers
from ..serializers import MotifDetailSerializers
from utils.permissions import IsOwnerOrReadOnly
from ..serializers import CommentListCreateSerializers, MotifListCreateSerializers
from art.models import Art
from ..models import Motif, Comment

__all__ = (
    # 댓글 조회 및 생성
    'CommentListCreateView',

    # 댓글 수정 및 삭제
    'CommentDetailRetrieveUpdateDestroyView',
)


class CommentListCreateView(generics.CreateAPIView):
    """
    댓글 조회 및 생성
    """
    serializer_class = CommentListCreateSerializers
    permission_classes = IsOwnerOrReadOnly,

    def get(self, request, *args, **kwargs):
        """
        모티프 내의 댓글 목록 전체 조회
        """
        motif_info = Motif.objects.get(pk=kwargs['motif_pk'])
        motifinfo_serializer = MotifDetailSerializers(motif_info)
        comments = Comment.objects.all().filter(motif=motif_info)
        commentlist_serializer = CommentDetailSerializers(comments, many=True)
        content = {
            'commentList': commentlist_serializer.data,
            'motifInfo': motifinfo_serializer.data,
        }
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        댓글 생성
        """
        art = get_object_or_404(Art, pk=kwargs['art_pk'])
        motif = get_object_or_404(Motif, pk=kwargs['motif_pk'])

        newcomment_serializer = self.serializer_class(data=request.data)
        newcomment_serializer.is_valid(raise_exception=True)
        new_comment = newcomment_serializer.save()

        comment_serializer = CommentDetailSerializers(new_comment)
        content = {
            "detail": "댓글이 등록되었습니다.",
            "commentInfo": comment_serializer.data,
        }
        return Response(content, status=status.HTTP_200_OK)


class CommentDetailRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    댓글 수정 및 삭제
    """
    serializer_class = CommentUpdateDestroySerializers
    permission_classes = IsCommentOwnerOrReadOnly,
    parser_classes = (MultiPartParser, FormParser,)

    def put(self, request, *args, **kwargs):
        """
        댓글 수정
        """
        comment = Comment.objects.get(pk=kwargs['comment_pk'])
        if self.request.user.is_authenticated():
            if self.request.user == comment.comment_author:
                editcomment_serializer = self.serializer_class(comment, data=request.data, partial=True)
                editcomment_serializer.is_valid(raise_exception=True)
                new_comment = editcomment_serializer.save()

                changed_comment = CommentDetailSerializers(new_comment)
                content = {
                    "detail": "댓글 수정이 완료되었습니다.",
                    "commentInfo": changed_comment.data,
                }
                return Response(content, status=status.HTTP_200_OK)
            content = {
                "detail": "댓글을 작성한 사용자만 수정이 가능합니다."
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        content = {
            "detail": "댓글을 수정하려면 로그인해주세요."
        }
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        """
        댓글 삭제
        """
        comment = Comment.objects.get(pk=kwargs['comment_pk'])
        content = {
            "detail": "댓글이 삭제되었습니다."
        }
        comment.delete()
        return Response(content, status=status.HTTP_200_OK)
