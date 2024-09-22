
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



# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class VideoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing video-related actions.

    This ViewSet provides various endpoints for listing, filtering, and favoriting videos.
    It uses token-based authentication and requires the user to be authenticated for all actions.

    Attributes:
    -----------
    - authentication_classes (list): Specifies the authentication method (TokenAuthentication).
    - permission_classes (list): Specifies the permissions (IsAuthenticated) for all actions.
    - queryset (QuerySet): The queryset of Video objects to work with.
    - serializer_class (Serializer): Specifies the serializer for the Video model (VideoSerializer).

    Actions:
    --------
    - get_videos: Returns all videos, with caching applied.
    - favorites: Returns all videos favorited by the current user.
    - top5: Returns the top 5 most recent videos, with caching applied.
    - category_videos: Returns videos filtered by category, with caching applied.
    - toggle_favorite: Adds or removes a video from the user's favorites.
    - is_favorite: Checks if a specific video is in the user's favorites.
    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    

    # @method_decorator(cache_page(CACHE_TTL)) 
    @action(detail=False, methods=['get'])
    def get_videos(self, request):
        """
        Retrieves all videos, with caching applied to improve performance.

        Returns:
        --------
        Response: A list of all videos serialized into JSON format.
        """
        videos = Video.objects.all() 
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)
    
    
    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """
        Retrieves all videos that the current user has marked as favorites.

        Returns:
        --------
        Response: A list of the user's favorite videos serialized into JSON format.
        """
        user = request.user
        favorite_videos = Video.objects.filter(favoritevideo__user=user)
        serializer = VideoSerializer(favorite_videos, many=True, context={'request': request})
        return Response(serializer.data)

    # @method_decorator(cache_page(CACHE_TTL)) 
    @action(detail=False, methods=['get'])
    def top5(self, request):
        """
        Retrieves the top 5 most recent videos, with caching applied.

        Returns:
        --------
        Response: A list of the top 5 most recent videos serialized into JSON format.
        """
        top5_videos = Video.objects.order_by('-created_at')[:5]
        serializer = VideoSerializer(top5_videos, many=True, context={'request': request})
        return Response(serializer.data)

    # @method_decorator(cache_page(CACHE_TTL)) 
    @action(detail=False, methods=['get'], url_path='category/(?P<category>[^/.]+)')
    def category_videos(self, request, category=None):
        """
        Retrieves videos filtered by category, with caching applied.

        Args:
        -----
        category (str): The category to filter videos by.

        Returns:
        --------
        Response: A list of videos filtered by category serialized into JSON format.
        """
        category_videos = Video.objects.filter(category=category)
        serializer = VideoSerializer(category_videos, many=True, context={'request': request})
        return Response(serializer.data)

    
    @action(detail=False, methods=['post'])
    def toggle_favorite(self, request):
        """
        Toggles the favorite status of a video for the current user.

        This action adds or removes the video from the user's favorites based on whether it's currently favorited.

        Returns:
        --------
        Response: A success message indicating the status of the favorite action.
        """
        user = request.user
        serializer = FavoriteVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({'status': 'Favorites set'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'], url_path='is_favorite/(?P<video_id>[^/.]+)')
    def is_favorite(self, request, video_id=None):
        """
        Checks if a specific video is in the user's favorites.

        Args:
        -----
        video_id (int): The ID of the video to check.

        Returns:
        --------
        Response: A boolean value indicating whether the video is favorited.
        """
        user = request.user
        video = get_object_or_404(Video, id=video_id)
        is_favorite = FavoriteVideo.objects.filter(user=user, video=video).exists()
        return Response({'is_favorite': is_favorite}, status=status.HTTP_200_OK)
    

def failed_job_detail(request, job_id):
    """
    View function for displaying details about a failed Redis job.

    This view fetches a job from Redis using the job ID and displays its status, result, and exception information.

    Args:
    -----
    job_id (str): The ID of the job to retrieve details for.

    Returns:
    --------
    Render: Renders the 'failed_job_detail.html' template with job details in the context.
    """
    job = Job.fetch(job_id, connection=redis.Redis(host='localhost', port=6379, db=0, password='foobared'))
    
    context = {
        'job_id': job.id,
        'status': job.get_status(),
        'result': job.result,
        'exc_info': job.exc_info,
    }
    return render(request, 'html/failed_job_detail.html', context)

