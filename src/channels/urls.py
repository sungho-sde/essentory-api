from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import ChannelMemberViewSet, ChannelViewSet, LinkViewSet

router = DefaultRouter()
router.register(r"", ChannelViewSet, basename="channels")

channels_router = routers.NestedDefaultRouter(router, r"", lookup="channel")
channels_router.register(
    r"channelmembers", ChannelMemberViewSet, basename="channel-channelmembers"
)
channels_router.register(r"links", LinkViewSet, basename="channel-link")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(channels_router.urls)),
]
