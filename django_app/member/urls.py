from django.conf.urls import url
from rest_framework.authtoken import views

from . import apis


app_name = 'member'

urlpatterns = [
    # 토큰 생성 뷰의 url
    url(
        r'api-token-auth/',
        views.obtain_auth_token)
    ,
    url(r'signup/$',
        apis.UserSignupView.as_view(),
        name='signup'
    ),
    url(
        r'^login/$',
        apis.CustomAuthTokenView.as_view(),
        name='login'
    ),
    url(
        r'^logout/$',
        apis.UserLogoutView.as_view(),
        name='logout'
    ),
    url(
        r'^profile/(?P<pk>\d+)$',
        apis.UserInfoView.as_view(),
        name='profile'
    ),
    url(
        r'^profile/(?P<pk>\d+)/edit$',
        apis.UserInfoView.as_view(),
        name='profile'
    ),
]
