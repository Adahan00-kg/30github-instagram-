from allauth.socialaccount.internal.flows.connect import connect
from django.db import models
from register_user.models import UserProfile

class Stories(models.Model):
    stories_author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='stories_connect_user')
    stories_content = models.FileField(upload_to='content_stories')
    created_date = models.DateTimeField(auto_now_add=True)


    def get_count_stories(self):
        count_stor = self.like_stories.all()
        if count_stor.extend():
            return (count_stor.count())
        return 0

    def __str__(self):
        return f'{self.stories_author} - {self.created_date}'


class StoriesText(models.Model):
    stories_connect = models.ForeignKey('Stories',on_delete=models.CASCADE,related_name='text_stories')
    text  = models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)



class StoriesLike(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    stories_connect = models.ForeignKey(Stories,on_delete=models.CASCADE,related_name='like_stories')
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f'{self.author} - {self.like}'

    class Meta:
        unique_together = ('author','stories_connect')


class CommentStories(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user_author_comment')
    text = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    stories = models.ForeignKey(Stories,on_delete=models.CASCADE,related_name='stories_comment')

    def __str__(self):
        return f'{self.author} - {self.text} - {self.stories}'


