from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from requests import delete
from .forms import RegisterForm
from .models import Profile,Post,Like,Followers
from itertools import chain
from django.db.models import Q



# Create your views here.

def home(request):
    
    return render(request,'home.html')



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user = user)
            profile.save()
            login(request,user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})

def logout(request):
    return render(request,'registration/logout.html')

# @login_required(login_url="/login")   
# def page(request):
#     form = Post.objects.all().values
    
#     if request.method == "POST":
#         post_id = request.POST.get("post-id")
#         post = Post.objects.filter(id = post_id).first()
#         if post and post.author == request.user:
#             post.delete()
#     return render(request,'page.html',{"form":form})

@login_required(login_url="/login")
def profile(request):
    user_profile = Profile.objects.get(user = request.user)
    
    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.image
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
        
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('page')
    return render(request,'profile.html',{'user_profile':user_profile})

@login_required(login_url="/login")
def page(request):
    
    # return redirect('/login')
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    
    user_following_list = []
    feed = []

    user_following = Followers.objects.filter(follower = request.user.username)
    for users in  user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user = usernames)
        feed.append(feed_lists)
    
    feed_lists = list(chain(*feed))
    
    posts = Post.objects.all()
    return render(request,'page.html',{'user_profile':user_profile,'posts':feed_lists})

# def search(request):
#     user_object = User.objects.get(username = request.user.username)
#     user_profile = Profile.objects.get(user = user_object)
#     if request.method == 'POST':
#         searched = request.POST['searched']
#         username_object = User.objects.filter(username__icontains = searched)

#         username_profile = []
#         username_profile_list = []

#         for users in username_object:
#             username_profile.append(users.id)
    
#         for ids in username_profile:
#             profile_lists = Profile.objects.filter(id_user= ids)
#             username_profile_list.append(profile_lists)

#         username_profile_list = list(chain(*username_profile_list))
#     return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})

# def searchpage(request):
    
#     if request.method == "POST":
#         searched_user = request.POST['searched_user']
#         searched_name = User.objects.filter(username__contains = searched_user).first()
#         info = Profile.objects.get(user = searched_name)
#         return render(request,'search.html',{'searched':searched_user,'searched_name':searched_name,'info':info})
#     else:    
#         return render(request,'search.html',{'searched':searched_user})
@login_required(login_url="/login")
def searchpage(request):
    if request.method == 'POST':
        searched_user = request.POST['searched_user']
        searched_name = Post.objects.filter(caption__contains = searched_user)
        
        return render(request,'search.html',{'info':searched_name,'searched':searched_user})
        
        
    else:
        return render(request,'search.html',{'info':searched_name,'searched':searched_user})

@login_required(login_url="/login")
def AddPost(request):
    if request.method == 'POST':
       user = request.user.username
       image = request.FILES.get('image_upload')
       caption = request.POST['caption']
    #    return HttpResponse(image)
       if image is not None:
           new_post = Post.objects.create(user = user, image = image,caption = caption)
           new_post.save()
    
       else:
            
            new_post = Post.objects.create(user = user, caption = caption,image = None)
            new_post.save()

       return redirect('page')

    else:
        return render(request,'addpost.html')

def delete(request,pk):
    
    user = request.user.username
    # del_post = Post.objects.get(id = pk)
    del_post = get_object_or_404(Post,id = pk)
        
    del_post.delete()
    return redirect('/dashboard/'+user)
    # return redirect('/dashboard/'+user)
            

@login_required(login_url="/login")
def like(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id = post_id)

    like_filter = Like.objects.filter(post_id=post_id,username =username).first()

    if like_filter == None:
        new_like = Like.objects.create(post_id=post_id,username =username)
        new_like.save()
        post.no_of_likes = post.no_of_likes +1
        post.save()
        return HttpResponseRedirect('page')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('page')
    


@login_required(login_url="/login")
def dashboard(request,pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user = pk)
    user_post_length = len(user_posts)
    follower = request.user.username
    user = pk
    if Followers.objects.filter(follower=follower,user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
        
    follower = Followers.objects.filter(user=pk)
    follower_length = len(follower)
    following = Followers.objects.filter(follower = pk)
    following_length = len(following)
    context = {
        "user_object":user_object,
        "user_profile":user_profile,
        "user_posts":user_posts,
        "user_post_length":user_post_length,
        "follower_length":follower_length,
        "following_length":following_length,
        "button_text" : button_text,
    }
    # user_object = User.objects.get(username= request.user.username)
    # user_profile = Profile.objects.get(user = user_object)
    return render(request,'dashboard.html',context)

@login_required(login_url="/login")
def users(request,pk):
    accounts = User.objects.all().exclude(is_staff = True)
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    
    context = {
        "accounts":accounts,
        "user_object":user_object,
        "user_profile":user_profile,
        
    }
    return render(request,'users.html',context)

def about(request):
    return render(request,'owner.html')
def mycontact(request):
    return render(request,'mycontact.html')
def projects(request):
    return render(request,'projects.html')

def contact(request):
    return render(request,'contact.html')

@login_required(login_url="/login")
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower,user =user):
            delete_follower = Followers.objects.get(follower=follower,user=user)
            delete_follower.delete()
            
            return redirect('/dashboard/'+ user)

        else:
            new_follower = Followers.objects.create(follower = follower,user = user)
            new_follower.save()
            return redirect('/dashboard/'+user)
    else:
        return redirect('page')

@login_required(login_url="/login")
def music(request):
    return render(request,'music.html')

@login_required(login_url="/login")
def viewpp(request,pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    return render(request,'viewpp.html',{'user_profile':user_profile})

