from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer, FavoriteVideoSerializer
from django.shortcuts import render
import redis
from rq import Queue
from rq.job import Job
from rest_framework.authentication import TokenAuthentication



class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [TokenAuthentication]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

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
    def set_favorites(self, request):
        user = request.user
        serializer = FavoriteVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({'status': 'Favorites set'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def failed_job_detail(request, job_id):
    job = Job.fetch(job_id, connection=redis.Redis(host='localhost', port=6379, db=0, password='foobared'))
    
    context = {
        'job_id': job.id,
        'status': job.get_status(),
        'result': job.result,
        'exc_info': job.exc_info,
    }
    return render(request, 'html/failed_job_detail.html', context)

