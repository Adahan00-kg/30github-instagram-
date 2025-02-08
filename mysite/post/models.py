from django.db import models

from register_user.models import UserProfile

class Post(models.Model):
    description = models.CharField(max_length=150)
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class PostContent(models.Model):
    img = models.FileField(upload_to='post_content')
    post_connect = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post')
