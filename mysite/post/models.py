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


    def __str__(self):
        return f'{self.post_img1}'


class PostTitle(models.Model):
    post_connect = models.ForeignKey(PostImg, on_delete=models.CASCADE, related_name='post_img_connect')
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='post_user')


    def delete(self, *args, **kwargs):
        self.post_connect.delete()
        super().delete(*args, **kwargs)


    def __str__(self):
        return f'{self.author} - {self.text}'

    def get_count_like(self):
        count_like = self.like_post.all()
        if count_like.exists():
                return (count_like.count())
        return 0


class Comment(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='user_author')
    text = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(PostTitle,on_delete=models.CASCADE,related_name='comment')

    def __str__(self):
        return f'{self.author} - {self.text} - {self.post}'

    def get_count_like(self):
        count_like = self.like_comment.all()
        if count_like.exists():
                return (count_like.count())
        return 0


class LikeComment(models.Model):
    author_like = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='comment_like')
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='like_comment')
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('author_like','comment')



class LikePost(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='author_comment')
    post = models.ForeignKey(PostTitle,on_delete=models.CASCADE,related_name='like_post')
    like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('author','post')


