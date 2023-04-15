from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet, registration_view, verification_view
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', registration_view, name='signup'),
    path('v1/auth/token/', verification_view, name='token'),
]
