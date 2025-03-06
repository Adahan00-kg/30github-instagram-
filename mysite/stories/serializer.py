from rest_framework import serializers
from .models import *


class StoriesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = ['stories_author', 'stories_content', 'created_date']


class StoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = ['stories_author','stories_content','created_date']


