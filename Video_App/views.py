from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Video, FavoriteVideo
from .serializers import VideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    @action(detail=True, methods=['post'])
    def toggle_favorite(self, request, pk=None):
        video = self.get_object()  # Verwende self.get_object() um das Video zu holen
        user = request.user
        favorite, created = FavoriteVideo.objects.get_or_create(user=user, video=video)
        if created:
            return Response({'status': 'Video added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            favorite.delete()
            return Response({'status': 'Video removed from favorites'}, status=status.HTTP_204_NO_CONTENT)







