from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class MediaLibrary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to="media/")
    category = models.CharField(max_length=50)
    campaign = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = "Media File"
        verbose_name_plural = "Media Library"

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    media = models.ManyToManyField(MediaLibrary, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("draft", "Draft"), ("published", "Published"), ("scheduled", "Scheduled")],
        default="draft",
    )
    scheduled_time = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=50, null=True, blank=True)
    recurrence_pattern = models.JSONField(null=True, blank=True)
    platforms = models.JSONField(null=True, blank=True)  # Store selected platforms as a list
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    def clean(self):
        """
        Ensure recurrence_pattern is valid JSON if provided.
        """
        if self.recurrence_pattern and not isinstance(self.recurrence_pattern, dict):
            raise ValidationError("Recurrence pattern must be a valid JSON object.")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class ContentModeration(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending",
    )
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Moderation for {self.post.title}"

    class Meta:
        verbose_name = "Content Moderation"
        verbose_name_plural = "Content Moderations"


class BulkUpload(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # Allow NULL temporarily
        blank=True
    )
    file = models.FileField(upload_to="bulk_uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bulk upload by {self.user.username if self.user else 'Unknown User'} on {self.uploaded_at}"

    class Meta:
        verbose_name = "Bulk Upload"
        verbose_name_plural = "Bulk Uploads"

