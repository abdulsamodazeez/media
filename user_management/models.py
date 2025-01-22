from django.db import models
from django.contrib.auth.models import User  # Use the default User model
from django.conf import settings  # For AUTH_USER_MODEL

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.action} at {self.timestamp}"


class SocialMediaAccount(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    platform = models.CharField(max_length=50, choices=[
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('snapchat', 'Snapchat'),
    ])
    account_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.account_name} ({self.platform})"


class PostingConfiguration(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('snapchat', 'Snapchat'),
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True)
    default_hashtags = models.TextField(blank=True)
    character_limit = models.IntegerField(default=280)

    def __str__(self):
        return self.platform
