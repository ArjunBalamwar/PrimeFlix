from django.contrib import admin
from .models import Post, WatchLater, Like

admin.site.register(Post)
admin.site.register(WatchLater)
admin.site.register(Like)