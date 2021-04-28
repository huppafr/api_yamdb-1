from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from titles.api.views import CategoryViewSet, GanreViewSet, TitleViewSet

router = DefaultRouter()
router.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    r'genres',
    GanreViewSet,
    basename='genres'
)
router.register(
    r'titles',
    TitleViewSet,
    basename='gtitles'
)

urlpatterns = [
    # path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls))
]