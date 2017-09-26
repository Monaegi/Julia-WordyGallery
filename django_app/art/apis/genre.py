from rest_framework import generics, status
from rest_framework.response import Response

from member.permissions import IsOwnerOrReadOnly
from ..models import Genre
from ..serializers import GenreListSerializers, ArtListSerializers


class GenreListView(generics.ListAPIView):
    """
    장르 목록 페이지
    클릭하면 장르별 작품목록 페이지로 가게끔 처리(template)
    """
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializers
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        genre_list = self.get_queryset()
        genre_serializer = self.serializer_class(genre_list, many=True)

        content = {
            'genreList': genre_serializer.data
        }
        return Response(content, status=status.HTTP_200_OK)


class GenreArtListView(generics.ListAPIView):
    """
    장르별 작품 목록 페이지
    작품을 클릭하면 작품상세페이지로 가게끔 처리(template)
    """
    serializer_class = ArtListSerializers
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        """
        장르명 별로 url을 보내면 해당 이름에 페이지를 보내준다.
        """
        genre_info = Genre.objects.get(name_genre=kwargs['genre_cate'])
        genre_artlist = genre_info.art
        genreinfo_serializer = GenreListSerializers(genre_info)
        genreart_serializer = self.serializer_class(genre_artlist, many=True)

        content = {
            "genreInfo": genreinfo_serializer.data,
            "genreArtList": genreart_serializer.data
        }
        return Response(content, status=status.HTTP_200_OK)
