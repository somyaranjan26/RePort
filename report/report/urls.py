from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('home/', views.home, name="Home"),
    re_path(r'^logIn/', views.logIn, name="LogIn"),
    re_path(r'^signIn/', views.signIn, name="SignIn"),
    re_path(r'^logOut/', views.logOut, name="LogOut"),
    re_path(r'^signUp/', views.newUser, name="SignUp"),
    re_path(r'^addTask/', views.addTask, name="AddTask"),
    re_path(r'^addNewTask/', views.addNewTask, name="AddNewTask"),
    re_path(r'^viewTaskList/', views.viewTaskList, name="ViewTaskList"),
    re_path(r'^deleteTask/', views.deleteTask, name="DeleteTask"),
]
