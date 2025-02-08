from django.contrib import admin
from .models import Post, PostContent


class ContentInline(admin.TabularInline):
    model = PostContent
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [ContentInline]


admin.site.register(Post,PostAdmin)
