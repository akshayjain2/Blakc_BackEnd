from django.shortcuts import render

# Create your views here.

def createUser(request):
    name = request.Post.get("UserInfo")
    emailId = request.Post.get("UserEmailId")
    teamName = request.Post.get("TeamName")
    empId = request.Post.get("empId")
    password = request.Post.get("password")


