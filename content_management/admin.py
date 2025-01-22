from django.contrib import admin
from .models import MediaLibrary, Post, ContentModeration

admin.site.register(MediaLibrary)
admin.site.register(Post)
admin.site.register(ContentModeration)
