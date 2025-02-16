from rest_framework import serializers
from .models import *

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password','first_name', 'last_name',
        'phone_number','profile_picture','status_acc','age']


        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    access = serializers.CharField()


class NetworkPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ['id','network_name','network_link',
                  'user_connect']


class UserProfileAllListSerializer(serializers.ModelSerializer):
    network = NetworkPostSerializer(many=True)
    post = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['username', 'email',  'first_name', 'last_name',
                  'phone_number', 'profile_picture', 'status_acc', 'age',
                  'bio', 'gender','network','post']

    def get_post(self, obj):
        from post.serializer import PostTitleListSerializer  # Локальный импорт, чтобы избежать циклического импорта
        posts = obj.post_user.all()  # Django автоматически создаёт `related_name` как `<model_name>_set`
        return PostTitleListSerializer(posts, many=True).data



class UserProfileAllPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['username', 'email','first_name', 'last_name',
                  'phone_number', 'profile_picture',
                  'status_acc', 'age', 'bio', 'gender','post']


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username','profile_picture']
