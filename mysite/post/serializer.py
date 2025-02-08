from rest_framework import serializers
from .models import *
from register_user.serializers import UserProfileListSerializer

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['description','author',]

class PostContentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['img','post_connect']

class PostContentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['id','img']


class PostListSerializer(serializers.ModelSerializer):
    post = PostContentListSerializer(many=True)
    author = UserProfileListSerializer()
    class Meta:
        model = Post
        fields = ['id','author','created_date','description','post']

