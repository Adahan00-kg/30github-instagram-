from django.shortcuts import render
from rest_framework import viewsets,generics
from .models import *
from .serializer import *


####################stories
class StoriesListAPIView(generics.ListAPIView):
    queryset = Stories.objects.all()
    serializer_class = StoriesListSerializer


class StoriesCreateAPIView(generics.CreateAPIView):
    serializer_class = StoriesCreateSerializer


class StoriesDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Stories.objects.all()
    serializer_class = StoriesDetailSerializer


#################### comment create

class StoriesCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = StoriesCommentCreateSerializer


class StoriesLikeCreate(generics.CreateAPIView):
    serializer_class = StoriesLikeCreateSerializer
