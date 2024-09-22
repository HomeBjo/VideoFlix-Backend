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
    path('failed-job/<str:job_id>/', failed_job_detail, name='failed_job_detail'),
    path('category/<str:category>/', VideoViewSet.as_view({'get': 'category_videos'}), name='category_videos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
