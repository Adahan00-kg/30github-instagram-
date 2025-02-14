from django.urls import path
from .views import *

urlpatterns = [
    path('post_img/create/',PostImgPostAPIView.as_view(),name = 'post_img_create'),

    path('post_create/',PostTitlePostAPIView.as_view(),name = 'post_create'),

    path('post_list/',PostTitleListAPIView.as_view(),name = 'post_list'),

    path('post_delete/',PostDeleteAPIView.as_view(),name = 'post_delete')
]
