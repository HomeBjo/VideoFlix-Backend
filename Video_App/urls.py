from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Video_App.views import VideoViewSet, failed_job_detail
from django.conf.urls.static import static
from django.conf import settings



router = DefaultRouter()
router.register(r'get_videos',  VideoViewSet, basename='get_videos')

app_name = 'Video_App'

urlpatterns = [
    path('', include(router.urls)),
    # path('set_favorites/', VideoViewSet.as_view({'post': 'set_favorites'}), name='set-favorites'),
    # path('favorites/', VideoViewSet.as_view({'get': 'favorites'}), name='favorites'),
    path('failed-job/<str:job_id>/', failed_job_detail, name='failed_job_detail'),
    path('category/<str:category>/', VideoViewSet.as_view({'get': 'category_videos'}), name='category_videos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# http://127.0.0.1:8000/media/videos/sand/sand_master.m3u8  zugriff auf server