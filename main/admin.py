import imp
from django.contrib import admin
from .models import Profile,Post,Like,Followers
# Register your models here.


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Followers)
