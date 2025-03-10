from django.urls import path
from .views import *

urlpatterns = [
    path('stories_create/',StoriesCreateAPIView.as_view(),name = 'stories_create'),

    path('stories/',StoriesListAPIView.as_view(),name = 'stories_list'),

    path('stories/<int:pk>/',StoriesDetailAPIView.as_view(),name = 'stories_detail'),

    path('stories_comment_create/',StoriesCommentCreateAPIView.as_view(),name = 'comment_create'),

    path('stories_like_create',StoriesLikeCreate.as_view(),name = 'stories_like_create'),

]
