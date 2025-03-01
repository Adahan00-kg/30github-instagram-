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
    queryset = PostTitle.objects.all()

class PostDetailListAPIView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    queryset = PostTitle.objects.all()


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer


class CommentDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()

class LikeCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = LikeCommentSerializer

class LikeCommentUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = LikeCommentSerializer
    queryset = LikeComment.objects.all()


class PostLikeAPIView(generics.CreateAPIView):
    serializer_class = LikePostSerializer


class PostLikeUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer

