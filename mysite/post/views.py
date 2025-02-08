from django.shortcuts import render
from rest_framework.viewsets import generics
from .serializer import *
from .models import *

class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostContentCreateAPIView(generics.CreateAPIView):
    serializer_class = PostContentPostSerializer
#
#
# class PostContentListAPIView(generics.ListAPIView):
#     queryset = PostContent.objects.all()
#     serializer_class = PostContentListSerializer

