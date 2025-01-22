from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import logging

from .models import UserActivity, SocialMediaAccount, PostingConfiguration
from .serializers import (
    UserActivitySerializer,
    SocialMediaAccountSerializer,
    PostingConfigurationSerializer,
    UserSerializer
)

logger = logging.getLogger(__name__)

# ------------------------
# User Management
# ------------------------
@method_decorator(csrf_exempt, name='dispatch')
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=403)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=403)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserActivity.objects.create(
                user=request.user,
                action=f"Created user {user.username}",
                ip_address=request.META.get('REMOTE_ADDR'),
            )
            logger.info(f"Admin {request.user.username} created user {user.username}")
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UserEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=403)
        user = get_object_or_404(User, pk=pk)

        if "status" in request.data:
            status_value = request.data["status"]
            if status_value == "active":
                user.is_active = True
            elif status_value in ["inactive", "suspended"]:
                user.is_active = False
            else:
                return Response({"error": "Invalid status value"}, status=400)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UserActivityLogsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=403)
        logs = UserActivity.objects.all()
        serializer = UserActivitySerializer(logs, many=True)
        return Response(serializer.data)


# ------------------------
# Social Media Accounts
# ------------------------
@method_decorator(csrf_exempt, name='dispatch')
class SocialMediaAccountsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all accounts or filter by user/platform.
        """
        user = request.user
        platform = request.query_params.get("platform")
        if user.is_staff:
            accounts = SocialMediaAccount.objects.all()
        else:
            accounts = SocialMediaAccount.objects.filter(user=user)
        
        if platform:
            accounts = accounts.filter(platform=platform)
        
        serializer = SocialMediaAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Add a new social media account.
        """
        serializer = SocialMediaAccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        """
        Remove a social media account.
        """
        account = get_object_or_404(SocialMediaAccount, pk=pk)
        if account.user != request.user and not request.user.is_staff:
            return Response({"error": "Permission denied."}, status=403)
        account.delete()
        return Response({"message": "Account removed successfully."}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class HealthCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=403)
        accounts = SocialMediaAccount.objects.all()
        health_status = {
            account.account_name: {
                "platform": account.platform,
                "status": "Healthy",
                "username": account.username,
            }
            for account in accounts
        }
        return Response(health_status)


# ------------------------
# Posting Configurations
# ------------------------
@method_decorator(csrf_exempt, name='dispatch')
class PostingConfigurationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=403)
        configs = PostingConfiguration.objects.all()
        serializer = PostingConfigurationSerializer(configs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=403)
        serializer = PostingConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            config, created = PostingConfiguration.objects.update_or_create(
                platform=serializer.validated_data['platform'],
                defaults=serializer.validated_data,
            )
            logger.info(f"Admin {request.user.username} updated configuration for {config.platform}")
            return Response(PostingConfigurationSerializer(config).data)
        return Response(serializer.errors, status=400)
