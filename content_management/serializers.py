from rest_framework import serializers
from .models import MediaLibrary, Post, ContentModeration, BulkUpload

class MediaLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaLibrary
        fields = ["id", "user", "file", "category", "campaign", "created_at"]
        extra_kwargs = {"user": {"read_only": True}}

class PostSerializer(serializers.ModelSerializer):
    media = MediaLibrarySerializer(many=True, read_only=True)
    media_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    platforms = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=True
    )  # Ensure platforms are provided

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "title",
            "content",
            "media",
            "media_ids",
            "status",
            "scheduled_time",
            "timezone",
            "recurrence_pattern",
            "platforms",
            "created_at",
        ]
        extra_kwargs = {"user": {"read_only": True},
                        'content': {'required': False},
        }

    def create(self, validated_data):
        media_ids = validated_data.pop("media_ids", [])
        platforms = validated_data.pop("platforms", [])
        post = super().create(validated_data)
        if media_ids:
            post.media.set(media_ids)
        post.platforms = platforms  # Store platforms
        post.save()
        return post


    def validate_recurrence_pattern(self, value):
        """
        Validate that the recurrence pattern, if provided, is valid JSON.
        """
        if value is not None and not isinstance(value, dict):
            raise serializers.ValidationError("Recurrence pattern must be a valid JSON object.")
        return value

    def update(self, instance, validated_data):
        """
        Handle `media_ids` for update operations.
        """
        media_ids = validated_data.pop("media_ids", [])
        instance = super().update(instance, validated_data)
        if media_ids:
            instance.media.set(media_ids)
        return instance

class BulkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkUpload
        fields = ["id", "user", "file", "uploaded_at"]
        extra_kwargs = {"user": {"read_only": True}}

class ContentModerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentModeration
        fields = ["id", "post", "status", "reviewed_by", "reviewed_at"]
        extra_kwargs = {"reviewed_by": {"read_only": True}}
