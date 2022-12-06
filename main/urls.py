
from django.urls import path
from .import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('home/',views.home,name = 'home'),
    path('dashboard/<str:pk>',views.dashboard,name = 'dashboard'),
    path('login/',LoginView.as_view(),name = 'login'),
    path('register/',views.register,name = 'register'),
    path('logout',views.logout,name='logout'),
    # path('logout/',LogoutView.as_view(),name = 'logout'),
    
    path('page/',views.page,name='page'),
    path('search',views.searchpage,name='search'),
    path('users/<str:pk>',views.users,name='users'),
    path('addpost/',views.AddPost,name='addpost'),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name = 'password.html',success_url ='/logout/'),name='change-password'),
    path('profile/',views.profile,name='profile'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('like',views.like,name='like'),
    path('follow',views.follow,name='follow'),
    path('mycontact',views.mycontact,name='mycontact'),
    path('projects',views.projects,name='projects'),
    path('music',views.music,name='music'),
    path('viewpp/<str:pk>',views.viewpp,name='viewpp'),
    path('delete/<str:pk>/',views.delete,name='delete')
    
]