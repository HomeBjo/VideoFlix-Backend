from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Video_App.models import Video
from Video_App.serializers import VideoSerializer


class VideoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        all_videos = Video.objects.all()
        favorite_videos = user.favorite_videos.all()

        all_videos_serializer = VideoSerializer(all_videos, many=True)
        favorite_videos_serializer = VideoSerializer(favorite_videos, many=True)

        return Response({
            'all_videos': all_videos_serializer.data,
            'favorite_videos': favorite_videos_serializer.data,
        })
