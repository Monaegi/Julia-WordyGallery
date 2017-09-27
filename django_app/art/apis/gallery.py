from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from art.models import Art
from member.permissions import IsOwnerOrReadOnly
from ..serializers import ArtListSerializers

__all__ = (
    'ArtListView',
    'ArtDetailView',
)


class ArtListView(generics.ListAPIView):
    """
    작품 리스트(gallery) 페이지
    """
    queryset = Art.objects.all().order_by('name_artist')
    serializer_class = ArtListSerializers
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        art_list = self.get_queryset()
        artlist_serializer = self.serializer_class(art_list, many=True)

        content = {
            'artList': artlist_serializer.data
        }
        return Response(content, status=status.HTTP_200_OK)


class ArtDetailView(generics.RetrieveAPIView):
    """
    작품 상세페이지
    """
    serializer_class = ArtListSerializers
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        art = Art.objects.get(pk=kwargs['art_pk'])
        art_serializer = self.serializer_class(art, partial=True)

        content = {
            'artInfo': art_serializer.data
        }
        return Response(content, status=status.HTTP_200_OK)
