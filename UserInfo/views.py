from django.shortcuts import render
from django.http import HttpResponse
import json
from models import UserInfo,UserTeamInfo
import datetime
from Blakc_BackEnd.settings import SECRET_KEY
import jwt  # import jwt library
# Create your views here.
def createUser(request):
    name = request.Post.get("UserInfo")
    emailId = request.Post.get("UserEmailId")
    teamName = request.Post.get("TeamName")
    empId = request.Post.get("empId")
    password = request.Post.get("password")
    repassword = request.Post.get("repassword")
    if password == repassword:
        UserInfo(Name = name , emailId = emailId, teamName =teamName,empId = empId,password = password).save()
    else:
        msg = {'status': 'failed', 'msg': 'Only Admin can Add the menber'}
        return HttpResponse(json.dumps(msg), content_type="application/json")
def login(request):
    if (UserInfo.objects.filter(Name=request.Post.get("username"), password=request.Post.get("password"))):
        json_data = {
            "sender": "Blakc JWT",
            "message": "Session jwt token",
            "date": str(datetime.datetime.now())
        }
        encode_data = jwt.encode(payload=json_data, \
                                 key=SECRET_KEY, algorithm="HS256")
        msg = {'status': 'success', 'msg': encode_data}
    else:
        msg ={'status': 'Fail', 'msg': "wrong Username or password"}
    return HttpResponse(json.dumps(msg), content_type="application/json")


def getTeams(request):
    name = request.Post.get("UserInfo")
    UserTeamInfo.objects.filter(Name = name)
    msg = {'status': 'success', 'msg': UserTeamInfo.AssociateTeam}
    return HttpResponse(json.dumps(msg), content_type="application/json")

def userlist(request):
    userlist = list(UserInfo.object.all().select('Name'))
    msg = {'status': 'success', 'msg': userlist}
    return HttpResponse(json.dumps(msg), content_type="application/json")

