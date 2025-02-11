from rest_framework import serializers
from .models import *
from register_user.serializers import UserProfileListSerializer



class PostContentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['img']

class PostContentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['id','img']

class PostCreateSerializer(serializers.ModelSerializer):
    post = PostContentListSerializer(many=True, write_only=True)

    class Meta:
        model = Post
        fields = ['description', 'author', 'post']

    def create(self, validated_data):
        post_content_data = validated_data.pop('post', [])  # Извлекаем вложенные изображения
        post = Post.objects.create(**validated_data)  # Создаем сам пост

        # Создаем изображения, связанные с этим постом
        for content in post_content_data:
            PostContent.objects.create(post_connect=post, **content)

        return post

class PostListSerializer(serializers.ModelSerializer):
    post = PostContentListSerializer(many=True)
    author = UserProfileListSerializer()
    class Meta:
        model = Post
        fields = ['id','author','created_date','description','post']

