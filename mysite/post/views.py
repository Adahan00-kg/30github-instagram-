from django.shortcuts import render
from rest_framework.viewsets import generics
from .serializer import *
from .models import *

class PostImgPostAPIView(generics.CreateAPIView):
    serializer_class = PosImgSerializer


class PostTitlePostAPIView(generics.CreateAPIView):
    serializer_class = PostTitleSerializer


class PostTitleListAPIView(generics.ListAPIView):
    queryset = PostTitle.objects.all()
    serializer_class = PostTitleListSerializer


class PostDeleteAPIView(generics.DestroyAPIView):
    serializer_class = PostTitleSerializer
