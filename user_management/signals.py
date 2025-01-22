from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UserActivity

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivity.objects.create(user=user, action='login', ip_address=request.META['REMOTE_ADDR'])
