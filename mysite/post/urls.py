from django.urls import path
from .views import *

urlpatterns = [
    path('post_img/create/',PostImgPostAPIView.as_view(),name = 'post_img_create'),

    path('post_create/',PostTitlePostAPIView.as_view(),name = 'post_create'),

    path('post_list/',PostTitleListAPIView.as_view(),name = 'post_list'),

    path('post_delete/<int:pk>/',PostDeleteAPIView.as_view(),name = 'post_delete'),

    path('comment_create/',CommentCreateAPIView.as_view(),name = 'comment_create'),

    path('comment_delete/<int:pk>/',CommentDeleteAPIView.as_view(),name = 'comment_delete'),

    path('like_comment/create/',LikeCommentCreateAPIView.as_view(),name = 'like_comment'),

    path('like_comment/update/<int:pk>/',LikeCommentUpdateAPIView.as_view(),name = 'like_comment_update'),

    path('like_post/create/',PostLikeAPIView.as_view(),name = 'like_post'),

    path('like_post/update/<int:pk>/',PostLikeUpdateAPIView.as_view(),name = 'like_post_update'),

    path('like/',PostLikeAPIView.as_view(),name = 'lkdlw')
]

