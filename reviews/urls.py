from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, CommentsViewSet, TitleViewSet
router = DefaultRouter()


router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='CommentView')

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet,
                basename='ReviewsView')

router.register(r'titles',
                TitleViewSet,
                basename='ReviewsView')

urlpatterns = [
    path('v1/', include(router.urls)),

]
