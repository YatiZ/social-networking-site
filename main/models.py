from email.policy import default
from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    id = models.UUIDField(primary_key = True,default= uuid.uuid4)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to = 'profiles',default='Logo.jpg')
    location = models.CharField(max_length = 100,blank = True)
    


    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key = True,default= uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images',default = 'll', null=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default = datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

# class Status(models.Model):
#     id = models.UUIDField(primary_key = True, default = uuid.uuid4)
#     user = models.CharField(max_length=100)
#     text = models.TextField()
#     created_at = models.DateTimeField(default = datetime.now)
#     no_of_likes = models.IntegerField(default = 0)

class Like(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Followers(models.Model):
    user = models.CharField(max_length=100)
    follower = models.CharField(max_length = 100)

    def __str__(self):
        return self.user