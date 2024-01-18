from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import CommentViewSet, PostViewSet

router = routers.DefaultRouter()
router.register("", PostViewSet, basename="posts")

posts_router = routers.NestedDefaultRouter(router, "", lookup="post")
posts_router.register("comments", CommentViewSet, basename="post-comments")

urlpatterns = [path("", include(router.urls)), path("", include(posts_router.urls))]
