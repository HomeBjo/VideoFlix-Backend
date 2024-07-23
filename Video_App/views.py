from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Video, FavoriteVideo
from .serializers import VideoSerializer, FavoriteVideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

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

    @action(detail=False, methods=['get'])
    def get_favorites(self, request):
        user = request.user
        favorite_videos = Video.objects.filter(favoritevideo__user=user)
        serializer = VideoSerializer(favorite_videos, many=True, context={'request': request})
        return Response(serializer.data)
