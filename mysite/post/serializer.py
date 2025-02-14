from rest_framework import serializers
from .models import *
from register_user.serializers import UserProfileListSerializer


class PosImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImg
        fields = ['post_img1','post_img2','post_img3','post_img4','post_img5',
                  'post_img6','post_img7','post_img8','post_img9','post_img10','author']


class PostTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTitle
        fields = ['post_connect','text']


class PostTitleListSerializer(serializers.ModelSerializer):
    post_connect = PosImgSerializer()
    class Meta:
        model = PostTitle
        fields = ['id','post_connect','text','created_date']



