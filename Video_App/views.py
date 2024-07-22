from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Video_App.models import Video
from Video_App.serializers import VideoSerializer
from rest_framework import  viewsets

class VideoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

  
    def list(self, request, *args, **kwargs):
        all_videos = Video.objects.all()
        serializer = VideoSerializer(all_videos, many=True, context={'request': request})
        return Response(serializer.data)
