from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Video_App.views import VideoListView



router = DefaultRouter()
router.register(r'get_videos',  VideoListView, basename='get_videos')

app_name = 'Video_App'

urlpatterns = [
    path('', include(router.urls)),
]