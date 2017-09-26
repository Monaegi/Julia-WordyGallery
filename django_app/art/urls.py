from django.conf.urls import url

from . import apis

urlpatterns = [
    # 작품 목록
    url(r'^gallery/$',
        apis.ArtListView.as_view(),
        name='art_list'
        ),
    # 작품 상세
    url(r'^(?P<art_pk>\d+)/$',
        apis.ArtDetailView.as_view(),
        name='art_detail'
        ),

    # 장르 목록
    url(r'^genre/$',
        apis.GenreListView.as_view(),
        name='genre_list'
        ),
    # 장르별 작품 목록
    url(r'^genre/(?P<genre_cate>.+)/$',
        apis.GenreArtListView.as_view(),
        name='genre_detail'
        ),
]