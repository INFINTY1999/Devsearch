from django.urls import path 
from . import  views

urlpatterns = [
    path('login/',views.loginuser,name="login"),
    path('logout/',views.logoutuser,name="logout"),
    path('register/',views.registeruser,name="register"),
    
    path('',views.profiles,name="profiles"),
    path('profile/<str:pk>',views.userprofile,name="user-profile"),
    path('userAccount/',views.userAccount,name="account"),
    path('editAccount/',views.editAccount,name="editAccount"),
    path('createskill/',views.createskill,name="createskill"),
    path('editskill/<str:pk>',views.editskill,name="editskill"),
    path('deleteskill/<str:pk>',views.deleteskill,name = "deleteskill"),

    path('inbox',views.inbox,name="inbox"),
    path('messages/<str:pk>',views.mess,name="message"),
    path('messageform/<str:pk>',views.messageform,name="messageform"),

]