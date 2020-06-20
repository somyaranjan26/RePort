from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('home/', views.home, name="Home"),
    url(r'^logIn/', views.logIn, name="LogIn"),
    url(r'^signIn/', views.signIn, name="SignIn"),
    url(r'^logOut/', views.logOut, name="LogOut"),
    url(r'^signUp/', views.newUser, name="SignUp"),
    url(r'^addTask/', views.addTask, name="AddTask"),
    url(r'^addNewTask/', views.addNewTask, name="AddNewTask"),
    url(r'^viewTaskList/', views.viewTaskList, name="ViewTaskList"),
    url(r'^deleteTask/', views.deleteTask, name="DeleteTask"),
]
