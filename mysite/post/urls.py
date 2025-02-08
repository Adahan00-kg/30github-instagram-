from django.urls import path
from .views import *

urlpatterns = [
    path('post_create/',PostCreateAPIView.as_view(),name = 'post_create'),

    path('post_list',PostListAPIView.as_view(),name = 'post_list'),

    path('content_create/',PostContentCreateAPIView.as_view(),name = 'post_content_create'),


]