from rest_framework import serializers
from django.contrib.auth.models import User  # Using Django's default User model
from .models import UserActivity, SocialMediaAccount, PostingConfiguration


# ------------------------
# User Serializer
# ------------------------
# Updated User Serializer with role logic
class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'role', 'status']  # Added 'status'

    def get_role(self, obj):
        return "admin" if obj.is_staff else "user"  # Assign role based on is_staff

    def get_status(self, obj):
        # Determine status based on the User model's `is_active` field and logic
        if obj.is_active:
            return "active"
        # Treat "suspended" as part of "inactive"
        elif not obj.is_active:
            # If no suspension logic exists, all inactive users can be considered "suspended"
            return "suspended"
        return "inactive"


# ------------------------
# User Activity Serializer
# ------------------------
class UserActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # To display the user's username instead of ID

    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'action', 'timestamp', 'ip_address']


# ------------------------
# Social Media Account Serializer
# ------------------------
class SocialMediaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaAccount
        fields = ['id', 'user', 'platform', 'account_name', 'username', 'password']
        extra_kwargs = {
            'user': {'required': False},  # Make the user field optional during serialization
        }


# ------------------------
# Posting Configuration Serializer
# ------------------------
class PostingConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostingConfiguration
        fields = ['platform', 'default_hashtags', 'character_limit']
