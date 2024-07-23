from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Video_App.views import VideoViewSet



router = DefaultRouter()
router.register(r'get_videos',  VideoViewSet, basename='get_videos')

app_name = 'Video_App'

urlpatterns = [
    path('', include(router.urls)),
    path('set_favorites/', VideoViewSet.as_view({'post': 'set_favorites'}), name='set-favorites'),
    path('favorites/', VideoViewSet.as_view({'get': 'favorites'}), name='favorites'),
]
