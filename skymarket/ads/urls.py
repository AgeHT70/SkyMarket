from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from ads.views import AdViewSet, CommentViewSet

# TODO настройка роутов для модели

ad_router = SimpleRouter()
ad_router.register("ads", AdViewSet)
comment_router = NestedSimpleRouter(ad_router, "ads", )
comment_router.register("comments", CommentViewSet)

urlpatterns = [
    path("", include(ad_router.urls)),
    path("", include(comment_router.urls))
]