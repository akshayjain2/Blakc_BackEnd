from datetime import datetime
from Team.models import TeamInfo,TeamMember
from django.http import HttpResponse
import json

# Create your views here.

def createTeam(request):
    TeamName = request.POST.get('TeamName', None)
    createby = request.POST.get('Createby', None)
    teamDesc = request.POST.get('TeamDesc', None)
    today = datetime.now().strftime("%d-%b-%Y")
    time = datetime.now().strftime("%H:%M:%S")
    if TeamInfo.objects.filter(TeamName=TeamName):
        msg = {'status': 'failed', 'msg' : 'Duplcate Name'}
        return HttpResponse(json.dumps(msg), content_type="application/json")
    else:
        TeamInfo(TeamName = TeamName, CreateBy = createby,TeamDesc =teamDesc,
             CreatedDate = today,CreatedTime = time,TeamAdmin = createby).save()
        msg = {'status': 'success', 'msg': 'team Created'}
        return HttpResponse(json.dumps(msg), content_type="application/json")

def addMember(request):
    teamName = request.POST.get('TeamName', None)
    name = request.POST.get('Name', None)
    TeamMemberList = request.POST.get('TeamMemberList', None)
    if TeamInfo.objects.filter(TeamName=teamName,TeamAdmin = name):
        teamPresent = TeamMember.objects.filter(TeanName=teamName)
        if teamPresent:
            MembersName = teamPresent.MembersName +TeamMemberList
            TeamMember.objects.filter(TeanName=teamName).update(MembersName=MembersName)
        else:
            TeamMember(MembersName = TeamMemberList,TeanName = teamName,AddBy = name).save()
    else:
        msg = {'status': 'failed', 'msg': 'Only Admin can Add the menber'}
        return HttpResponse(json.dumps(msg), content_type="application/json")

def viewAcess(request):
    TeamName = request.POST.get('TeamName', None)
    member = request.POST.get('menber', None)
    if TeamInfo.objects.filter(TeamName = TeamName,TeamAdmin = member):
        msg = {'status': 'success', 'msg': 'User is Admin'}
    else:
        msg = {'status': 'success', 'msg': 'User is Non-Admin'}
    return HttpResponse(json.dumps(msg), content_type="application/json")

def deleteTeam(request):
    TeamName = request.POST.get('TeamName', None)
    member = request.POST.get('menber', None)
    if TeamInfo.objects.filter(TeamName=TeamName, TeamAdmin=member):
        TeamInfo.objects.filter(TeamName=TeamName).delete()
        msg = {'status': 'success', 'msg': 'Remove successful'}
    else:
        msg = {'status': 'Fail', 'msg': 'Only Admin Can remove group'}
    return HttpResponse(json.dumps(msg), content_type="application/json")

def modifyteammember(request):
    teamName = request.POST.get('TeamName', None)
    name = request.POST.get('Name', None)
    TeamMemberList = request.POST.get('TeamMemberList', None)
    if TeamInfo.objects.filter(TeamName=teamName, TeamAdmin=name):
        teamPresent = TeamMember.objects.filter(TeanName=teamName)
        if teamPresent:
            MembersName = teamPresent.MembersName + TeamMemberList
            TeamMember.objects.filter(TeanName=teamName).update(MembersName=MembersName)
        else:
            TeamMember(MembersName=TeamMemberList, TeanName=teamName, AddBy=name).save()
    else:
        msg = {'status': 'failed', 'msg': 'Only Admin can Add the menber'}
        return HttpResponse(json.dumps(msg), content_type="application/json")
def removeTeamMember(request):
    teamName = request.POST.get('TeamName', None)
    name = request.POST.get('Name', None)
    TeamMemberList = request.POST.get('TeamMemberList', None)
    if TeamInfo.objects.filter(TeamName=teamName, TeamAdmin=name):
        teamPresent = TeamMember.objects.filter(TeanName=teamName)
        if teamPresent:
            MembersName =list(teamPresent.MembersName)
            MembersName.remove(TeamMemberList)
            TeamMember.objects.filter(TeanName=teamName).update(MembersName=MembersName)
            msg = {'status': 'success', 'msg': 'Member are successfully removed'}
        else:
            msg = {'status': 'failed', 'msg': 'Error Occur may be the member is not present'}
        return HttpResponse(json.dumps(msg), content_type="application/json")

    else:
        msg = {'status': 'failed', 'msg': 'Only Admin can Add the menber'}
        return HttpResponse(json.dumps(msg), content_type="application/json")

