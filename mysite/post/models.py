from django.db import models

from register_user.models import UserProfile

class PostImg(models.Model):
    post_img1 = models.FileField(upload_to='post_img',null=True,blank=True)
    post_img2 = models.FileField(upload_to='post_img',null=True,blank=True)
    post_img3 = models.FileField(upload_to='post_img',null=True,blank=True)
    post_img4 = models.FileField(upload_to='post_img',null=True,blank=True)
    post_img5 = models.FileField(upload_to='post_img',null=True,blank=True)
    post_img6 = models.FileField(upload_to='post_img',null=True,blank=True)
    post_img7 = models.FileField(upload_to='post_img',null=True,blank=True)
    post_img8 = models.FileField(upload_to='post_img',null=True,blank=True)
    post_img9 = models.FileField(upload_to='post_img',null=True,blank=True)
    post_img10 = models.FileField(upload_to='post_img',null=True,blank=True)
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='post')

    def __str__(self):
        return f'{self.author}'


class PostTitle(models.Model):
    post_connect = models.ForeignKey(PostImg,on_delete=models.CASCADE,related_name='post_img_connect')
    text = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user_author')
    text = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(PostTitle,on_delete=models.CASCADE,related_name='comment')


class LikeComment(models.Model):
    author_like = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='comment_like')
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='like_comment')
    

class LikePosst(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='author_comment')
    post = models.ForeignKey(PostTitle,on_delete=models.CASCADE,related_name='like_post')
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('author','post')
