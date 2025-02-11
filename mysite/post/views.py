from django.shortcuts import render
from rest_framework.viewsets import generics
from .serializer import *
from .models import *


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer


class PostContentCreateAPIView(generics.CreateAPIView):
    serializer_class = PostContentPostSerializer


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
