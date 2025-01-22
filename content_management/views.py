from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import MediaLibrary, Post, ContentModeration
from .serializers import MediaLibrarySerializer, PostSerializer, ContentModerationSerializer
from .tasks import schedule_post
import pandas as pd
from django.utils.dateparse import parse_datetime
import logging
import requests
import os
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


# Media Upload
@method_decorator(csrf_exempt, name='dispatch')

class UploadMediaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")
        image_url = request.data.get("image_url")
        
        if not file and not image_url:
            return Response({"error": "No file or image URL provided."}, status=400)

        if image_url:
            try:
                # Download the image from the URL
                response = requests.get(image_url, stream=True)
                if response.status_code != 200:
                    return Response({"error": "Failed to download image from URL."}, status=400)

                # Extract the filename from the URL
                filename = os.path.basename(image_url)

                # Check for duplicate file by name and user
                existing_file = MediaLibrary.objects.filter(file=filename, user=request.user).first()
                if existing_file:
                    return Response(
                        {"error": f"File '{filename}' already exists."},
                        status=400
                    )

                # Save the downloaded image file to MediaLibrary
                media = MediaLibrary(user=request.user)
                media.file.save(filename, ContentFile(response.content))
                media.save()

                serializer = MediaLibrarySerializer(media, context={"request": request})
                return Response(serializer.data, status=201)
            except Exception as e:
                return Response({"error": f"An error occurred: {str(e)}"}, status=500)

        elif file:
            # Check for duplicate file by name and user
            existing_file = MediaLibrary.objects.filter(file=file.name, user=request.user).first()
            if existing_file:
                return Response(
                    {"error": f"File '{file.name}' already exists."},
                    status=400
                )

            serializer = MediaLibrarySerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# Media Library
class MediaLibraryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        media_files = MediaLibrary.objects.all()
        serializer = MediaLibrarySerializer(media_files, many=True, context={'request': request})
        return Response(serializer.data)


# Post Management
class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save()
            media_ids = request.data.get("media_ids", [])
            post.media.set(media_ids)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ListPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


# Post Moderation
class ModeratePostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=404)

        moderation, created = ContentModeration.objects.get_or_create(post=post)
        serializer = ContentModerationSerializer(moderation)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=404)

        moderation, created = ContentModeration.objects.get_or_create(post=post)
        serializer = ContentModerationSerializer(moderation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(reviewed_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# Scheduling
@method_decorator(csrf_exempt, name='dispatch')
class SchedulePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            post = serializer.save(
                user=request.user,
                status="scheduled",
                recurrence_pattern=request.data.get("recurrence_pattern", None),
            )
            for platform in post.platforms:
                schedule_post.apply_async((post.id, platform), eta=post.scheduled_time)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ListScheduledPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(scheduled_time__isnull=False).order_by("scheduled_time")
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)


# class ListScheduledPostsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         posts = Post.objects.filter(scheduled_time__isnull=False).order_by("scheduled_time")
#         events = []
        
#         # Prepare events for FullCalendar
#         for post in posts:
#             media = post.media.first()  # Assuming one primary media file
#             events.append({
#                 "id": post.id,
#                 "title": post.title,
#                 "start": post.scheduled_time.isoformat(),
#                 "description": post.content,
#                 "image_url": media.file.url if media else None,  # Include the media file URL if available
#             })

#         return Response(events, status=200)

class BulkScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Bulk schedule posts from a CSV file.
        """
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided."}, status=400)

        try:
            df = pd.read_csv(file)

            # Validate required columns
            required_columns = {"title", "content", "status", "scheduled_time", "timezone", "media_ids"}
            missing_columns = required_columns - set(df.columns)
            if missing_columns:
                return Response({"error": f"Missing columns: {missing_columns}"}, status=400)

            # Bulk create posts
            for _, row in df.iterrows():
                try:
                    media_ids = [int(mid) for mid in str(row.get("media_ids", "")).split(",") if mid.isdigit()]
                    scheduled_time = parse_datetime(row["scheduled_time"])
                    if not scheduled_time:
                        return Response({"error": f"Invalid scheduled_time: {row['scheduled_time']}"}, status=400)

                    post = Post.objects.create(
                        user=request.user,
                        title=row["title"],
                        content=row["content"],
                        status=row["status"],
                        scheduled_time=scheduled_time,
                        timezone=row["timezone"],
                        recurrence_pattern=row.get("recurrence_pattern", None),  # Optional field
                    )
                    post.media.set(media_ids)
                except Exception as post_error:
                    logger.exception(f"Error creating post for row: {row.to_dict()}")
                    return Response({"error": str(post_error)}, status=400)

            return Response({"message": "Bulk scheduling successful."}, status=201)
        except Exception as e:
            logger.exception("Error in bulk_schedule.")
            return Response({"error": str(e)}, status=400)