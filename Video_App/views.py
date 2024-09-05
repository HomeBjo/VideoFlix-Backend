
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FavoriteVideo, Video
from .serializers import VideoSerializer, FavoriteVideoSerializer
from django.shortcuts import get_object_or_404, render
import redis
from rq.job import Job
from rest_framework.authentication import TokenAuthentication

from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class VideoViewSet(viewsets.ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    @method_decorator(cache_page(CACHE_TTL)) 


    @action(detail=False, methods=['get'])
    def get_videos(self, request):
        videos = Video.objects.all() 
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)
    
    
    @action(detail=False, methods=['get'])
    def favorites(self, request):
        user = request.user
        favorite_videos = Video.objects.filter(favoritevideo__user=user)
        serializer = VideoSerializer(favorite_videos, many=True, context={'request': request})
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def top5(self, request):
        top5_videos = Video.objects.order_by('-created_at')[:5]
        serializer = VideoSerializer(top5_videos, many=True, context={'request': request})
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='category/(?P<category>[^/.]+)')
    def category_videos(self, request, category=None):
        category_videos = Video.objects.filter(category=category)
        serializer = VideoSerializer(category_videos, many=True, context={'request': request})
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def toggle_favorite(self, request):
        print(request.headers.get('Authorization'))  # Füge dies hinzu
        user = request.user
        serializer = FavoriteVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({'status': 'Favorites set'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'], url_path='is_favorite/(?P<video_id>[^/.]+)')
    def is_favorite(self, request, video_id=None):
        user = request.user
        video = get_object_or_404(Video, id=video_id)
        is_favorite = FavoriteVideo.objects.filter(user=user, video=video).exists()
        return Response({'is_favorite': is_favorite}, status=status.HTTP_200_OK)
    

def failed_job_detail(request, job_id):
    job = Job.fetch(job_id, connection=redis.Redis(host='localhost', port=6379, db=0, password='foobared'))
    
    context = {
        'job_id': job.id,
        'status': job.get_status(),
        'result': job.result,
        'exc_info': job.exc_info,
    }
    return render(request, 'html/failed_job_detail.html', context)

