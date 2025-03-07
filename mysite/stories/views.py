from django.shortcuts import render
from rest_framework import viewsets,generics
from .models import *
from .serializer import *


class StoriesCreateAPIView(generics.CreateAPIView):
    serializer_class = StoriesCreateSerializer

