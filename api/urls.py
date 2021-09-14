from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views as vs
from .serializers import MyTokenObtainPairView
from .views import email_auth

router_v1 = routers.DefaultRouter()

router_v1.register(r'categories', vs.CategoryModelViewSet, basename='category')
router_v1.register(r'titles', vs.TitleModelViewSet, basename='title')
router_v1.register(r'genres', vs.GenreModelViewSet, basename='genre')
router_v1.register(r'titles/(?P<title_id>[0-9]+)/reviews',
                   vs.ReviewModelViewSet, basename='review')

router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews', vs.ReviewModelViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    vs.CommentModelViewSet,
    basename='comment',
)
router_v1.register('users', vs.UserModelViewSet, basename='users')

urlpatterns = [
    re_path(r'^v1/', include(router_v1.urls)),
    path('v1/auth/email/', email_auth, name='email_auth'),
    path(
        'v1/auth/token/',
        MyTokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
]
