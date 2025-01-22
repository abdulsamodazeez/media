from celery import shared_task
from django.utils.timezone import now
from user_management.models import SocialMediaAccount
from .models import Post
import subprocess
import json
import os

@shared_task
def schedule_post(post_id, platform):
    try:
        post = Post.objects.get(id=post_id)
        
        # Fetch the social media account for the user and platform
        account = SocialMediaAccount.objects.filter(platform=platform, user=post.user).first()
        if not account:
            raise ValueError(f"No {platform} account registered for user {post.user.username}")

        email = account.username
        password = account.password

        # Prepare media path
        media_path = post.media.first().file.path if post.media.exists() else None

        # Prepare Playwright script arguments
        script_args = {
            "platform": platform,
            "message": post.content,
            "media_path": media_path,
            "email": email,
            "password": password,
        }

        # Path to the Playwright script
        python_path = "C:\\Users\\This  PC\\Documents\\admin folder\\admin\\Scripts\\python.exe"
        script_path = "C:\\Users\\This  PC\\Documents\\admin folder\\socialMedia.py"
        print(f"Script Path: {script_path}")

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script not found at {script_path}")

        # Execute Playwright script
        subprocess.run(
            [python_path, script_path, json.dumps(script_args)],
            check=True,
            text=True
        )

        # Update the status to 'published' after successful execution
        post.status = "published"
        post.save()

    except Exception as e:
        post.status = "failed"
        post.save()
        raise RuntimeError(f"Error executing Playwright script: {e}")

@shared_task
def bulk_schedule_posts():
    """
    Task to process all scheduled posts for the current time.
    """
    current_time = now()
    posts = Post.objects.filter(status="Scheduled", scheduled_time__lte=current_time)
    for post in posts:
        for platform in post.platforms:  # Iterate over platforms
            schedule_post.delay(post.id, platform)  # Trigger for each platform
        post.status = "Processing"
        post.save()
