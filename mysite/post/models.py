from django.db import models

from register_user.models import UserProfile

class Post(models.Model):
    description = models.CharField(max_length=150)
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class PostContent(models.Model):
    img = models.FileField(upload_to='post_content')
    post_connect = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post')


class Comment(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user_author')
    text = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment')

class LikeComment(models.Model):
    author_like = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='comment_like')
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='like_comment')
    

class LikePosst(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='author_comment')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='like_post')
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('author','post')
