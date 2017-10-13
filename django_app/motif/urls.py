from django.conf.urls import url

from . import apis

urlpatterns = [
    # 작품별 모티프 목록
    url(r'^(?P<art_pk>\d+)/motifs/$',
        apis.MotifListCreateView.as_view(),
        name='motif_list'
        ),

    # 모티프 생성
    url(r'^(?P<art_pk>\d+)/motifs/add/$',
        apis.MotifListCreateView.as_view(),
        name='motid_add'
        ),

    # 모티프 세부
    url(r'^(?P<art_pk>\d+)/motifs/(?P<motif_pk>\d+)/$',
        apis.MotifDetailRetrieveUpdateDestroyView.as_view(),
        name='motif_detail'
        ),

    # 모티프 수정 및 삭제
    url(r'^(?P<art_pk>\d+)/motifs/(?P<motif_pk>\d+)/edit/$',
        apis.MotifDetailRetrieveUpdateDestroyView.as_view()
        ),

    # 댓글 조회 및 생성
    url(r'^(?P<art_pk>\d+)/motifs/(?P<motif_pk>\d+)/comments/$',
        apis.CommentListCreateView.as_view(),
        name='commentlist'),

    # 댓글 수정 및 삭제
    url(r'^(?P<art_pk>\d+)/motifs/(?P<motif_pk>\d+)/comments/(?P<comment_pk>\d+)/edit/$',
        apis.CommentDetailRetrieveUpdateDestroyView.as_view(),
        name='comment_edit',)
]