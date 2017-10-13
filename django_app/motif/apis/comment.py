from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from art.serializers import ArtListSerializers
from ..serializers import CommentDetailSerializers
from ..serializers import MotifDetailSerializers
from utils.permissions import IsOwnerOrReadOnly
from ..serializers import CommentListCreateSerializers, MotifListCreateSerializers
from art.models import Art
from ..models import Motif, Comment

__all__ = (
    'CommentListCreateView',
)


class CommentListCreateView(generics.CreateAPIView):
    serializer_class = CommentListCreateSerializers
    permission_classes = IsOwnerOrReadOnly,

    def get(self, request, *args, **kwargs):
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
        art = get_object_or_404(Art, pk=kwargs['art_pk'])
        motif = get_object_or_404(Motif, pk=kwargs['motif_pk'])

        newcomment_serializer = self.serializer_class(data=request.data)
        newcomment_serializer.is_valid(raise_exception=True)
        new_comment = newcomment_serializer.save()

        comment_serializer = CommentDetailSerializers(new_comment)
        content = {
            "detail": "댓글이 등록되었습니다.",
            "commentContent": comment_serializer.data,
        }
        return Response(content, status=status.HTTP_200_OK)


class CommentUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    #  serializer_class = CommentUpdateDestroySerializers
    pass