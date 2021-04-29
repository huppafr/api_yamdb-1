from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import CommentViewSet, ReviewViewSet


router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='Review'
)
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='Comment'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
