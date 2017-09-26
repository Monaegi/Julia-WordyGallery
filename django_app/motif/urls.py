from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^(?P<art_pk>\d+)/motifs/$',
        apis.MotifListCreateView.as_view(),
        name='motif_list'
        ),

]