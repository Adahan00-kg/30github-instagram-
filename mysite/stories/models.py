from django.db import models
from user.models import UserProfile

class Stories(models.Model):
    stories_author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='stories_connect_user')
    stories_content = models.FileField(upload_to='content_stories')
    created_date = models.DateTimeField(auto_now_add=True)

