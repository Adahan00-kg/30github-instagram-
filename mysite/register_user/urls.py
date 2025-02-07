from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('network/create/',NetworkCreateAPIView.as_view(),name = 'network_create'),

    path('profile/',UserProfileListAPIView.as_view(),name = 'user_profile_list'),

    path('profile/<int:pk>/',UserProfileRetrieveAPIView.as_view(),name = 'user_profile_detail'),

    path('updated/<int:pk>/',UserProfileUpdatedAPIView.as_view(),name = 'user_profile_update')
]
