from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    followers_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_followers(self):
        followers_count = self.followed.all().count()
        if self.followers_count != followers_count:
            self.followers_count = followers_count
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_total_followers()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.calculate_total_followers()

    def __str__(self):
        return self.username
    


class Follow(models.Model):
    follower = models.ForeignKey(get_user_model(), related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followed', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
    
    
class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    book = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=500)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_likes(self):
        likes_count = self.likes_relation.all().count()
        if self.likes != likes_count:
            self.likes = likes_count
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_total_likes()

    def delete(self, *args, **kwargs):
        self.calculate_total_likes()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title    
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on "{self.post.title}"'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_relation')
    user = models.ForeignKey(get_user_model(), related_name='liked_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked "{self.post.title}"'
    





    


