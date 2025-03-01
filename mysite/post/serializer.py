from rest_framework import serializers
from .models import *


from register_user.serializers import UserProfileListSerializer

class CommentListSerializer(serializers.ModelSerializer):
    count_like = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','author','text','created_date',
                  'parent_review','post','count_like']


    def get_count_like(self,obj):
        return obj.get_count_like()


class PosImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImg
        fields = ['id','post_img1','post_img2','post_img3','post_img4','post_img5',
                  'post_img6','post_img7','post_img8','post_img9','post_img10']


class PostTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTitle
        fields = ['id','post_connect','text','author']


class PostDetailSerializer(serializers.ModelSerializer):
    comment = CommentListSerializer(many=True)
    post_connect = PosImgSerializer()
    author = UserProfileListSerializer()
    count_like = serializers.SerializerMethodField()

    class Meta:
        model = PostTitle
        fields = ['id', 'author', 'post_connect', 'text', 'created_date', 'comment', 'count_like']

    def get_count_like(self, obj):
        return obj.get_count_like()


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','author','text','parent_review','post']




class PostTitleListSerializer(serializers.ModelSerializer):
    comment = CommentListSerializer(many=True)
    post_connect = PosImgSerializer()
    author = UserProfileListSerializer()
    count_like = serializers.SerializerMethodField()
    class Meta:
        model = PostTitle
        fields = ['id','author','post_connect','text','created_date','comment','count_like']

    def get_count_like(self,obj):
        return obj.get_count_like()

class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = ['id','author_like','comment','like']



class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields= ['id','author','post','like']

