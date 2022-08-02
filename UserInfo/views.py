from django.http import HttpResponse
import json
from .models import UserInfo,UserTeamInfo
from Blakc_BackEnd.settings import SECRET_KEY
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
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




# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response