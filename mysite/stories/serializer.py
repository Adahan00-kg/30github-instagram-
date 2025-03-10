from rest_framework import serializers
from .models import *
from register_user.serializers import UserProfileListSerializer

#################Stories Create
class StoriesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = ['id','stories_author', 'stories_content', 'created_date']
################# Stories List

class StoriesListSerializer(serializers.ModelSerializer):
    stories_author = UserProfileListSerializer()
    class Meta:
        model = Stories
        fields = ['id','stories_author', 'created_date']

####################### comment create
class StoriesCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriesText
        fields = ['id','stories_connect','text','created_date']

####################### like create
class StoriesLikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoriesLike
        fields = ['id','author','like','stories_connect',]

####################### like list
class StoriesLikeListSerializer(serializers.ModelSerializer):
    author = UserProfileListSerializer()
    class Meta:
        model = StoriesLike
        fields = ['id','author','like','stories_connect','created_date']

####################### stories detail
class StoriesDetailSerializer(serializers.ModelSerializer):
    stories_comment = StoriesCommentCreateSerializer(many=True)
    count_stories = serializers.SerializerMethodField()
    like_stories = StoriesLikeListSerializer(many=True)
    class Meta:
        model = Stories
        fields = ['id','stories_author','stories_content',
                  'created_date','count_stories','like_stories','stories_comment']


    def get_count_stories(self,obj):
        return obj.count_stories()
# class PostDetailSerializer(serializers.ModelSerializer):
#     comment = CommentListSerializer(many=True)
#     post_connect = PosImgSerializer()
#     author = UserProfileListSerializer()
#     count_like = serializers.SerializerMethodField()
#
#     class Meta:
#         model = PostTitle
#         fields = ['id', 'author', 'post_connect', 'text', 'created_date', 'comment', 'count_like']
#
#     def get_count_like(self, obj):
#         return obj.get_count_like()