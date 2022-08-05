from django.shortcuts import render
from django.http import HttpResponse
import json
from rest_framework.views import APIView
from .models import User, Post, ToDo, Contact, Project, Issue, Tag, Milestone, Effort, Column,ChatInfo
from ChatApplication.form import UserCreateForm, SessionCreateForm, PostCreateForm, ToDoCreateForm, ToDoCompleteForm, \
    ContactCreateForm, ContactUpdateForm, ProjectCreateForm, ProjectUpdateForm, IssueCreateForm, TagCreateForm, MilestoneCreateForm, EffortCreateForm, ColumnCreateForm
from .serializers import UserSerializer, PostSerializer, ToDoSerializer, ContactSerializer, ProjectSerializer, IssueSerializer, \
    TagSerializer, MilestoneSerializer, EffortSerializer, ColumnSerializer
# Create your views here.
import mimetypes
from datetime import datetime
import os

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from minio import Minio
from minio.error import InvalidXMLError, InvalidEndpointError, NoSuchKey, NoSuchBucket
from urllib3.exceptions import MaxRetryError


def setting(name, default=None):
    """
    Helper function to get a Django setting by name or (optionally) return
    a default (or else ``None``).
    """
    return getattr(settings, name, default)


@deconstructible
class MinioStorage(Storage):

    server = setting('MINIO_SERVER')
    access_key = setting('MINIO_ACCESSKEY')
    secret_key = setting('MINIO_SECRET')
    bucket = setting('MINIO_BUCKET')
    secure = setting('MINIO_SECURE')

    def __init__(self, *args, **kwargs):
        super(MinioStorage, self).__init__(*args, **kwargs)
        self._connection = None

    @property
    def connection(self,request):
        if not self._connection:
            try:
                self._connection = Minio(
                    self.server, self.access_key, self.secret_key, self.secure)
            except InvalidEndpointError:
                self._connection = None
        return self._connection

    def _save(self, name, content):
        pathname, ext = os.path.splitext(name)
        dir_path, _ = os.path.split(pathname)
        hashed_name = f'{dir_path}/{hash(content)}{ext}'

        content_type = content.content_type if hasattr(content, 'content_type') else mimetypes.guess_type(name)[0]

        if self.connection:
            if not self.connection.bucket_exists(self.bucket):
                self.connection.make_bucket(self.bucket)
            try:
                self.connection.put_object(
                    self.bucket,
                    hashed_name,
                    content,
                    content.size,
                    content_type=content_type,
                )
            except InvalidXMLError:
                pass
            except MaxRetryError:
                pass
        return hashed_name

    def url(self, name):
        if self.connection:
            try:
                if self.connection.bucket_exists(self.bucket):
                    return self.connection.presigned_get_object(self.bucket, name)
                else:
                    return 'image_not_found'
            except MaxRetryError:
                return 'image_not_found'
        return 'could_not_establish_connection'

    def exists(self, name):
        try:
            self.connection.stat_object(self.bucket, name)
        except (NoSuchKey, NoSuchBucket):
            return False
        except Exception as err:
            raise IOError(f'Could not stat file {name} {err}')
        else:
            return True

    def size(self, name):
        return self.connection.stat_object(self.bucket, name).size


def sendChat(request):
    type =request.Post.get("ChatType")
    msg = request.Post.get("Message")
    fromId = request.Post.get("From")
    toId = request.Post.get("TO")
    if type == "attachment":
        #upload the attachment to minio server
        pass
    else:
        ChatInfo(ChatType = "nornal",
    ChatDate = datetime.now().strftime("%d-%b-%Y"),
    ChatTime = datetime.now().strftime("%H:%M:%S"),
    ChatFrom =fromId,
    ChatPersonal = False,
    Message = msg ).save()


def viewChat(request):
    # ChatInfo.objects.all()
    return ChatInfo.objects.all()




def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    return True


class UserView(APIView):
    def post(self,request):
        form = UserCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User(form.email.data, form.password.data)
        request.session.add(user)
        request.session.commit()
        return UserSerializer(user).data


class SessionView(APIView):
    def post(self,request):
        form = SessionCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User.query.filter_by(email=form.email.data).first()
        if user :
            return UserSerializer(user).data, 201
        return '', 401


class PostListView(APIView):
    def get(self,request):
        posts = Post.query.all()
        return PostSerializer(posts, many=True).data

    
    def post(self,request):
        form = PostCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        post = Post(form.title.data, form.body.data)
        request.session.add(post)
        request.session.commit()
        return PostSerializer(post).data, 201


class PostView(APIView):
    def get(self, id,request):
        posts = Post.query.filter_by(id=id).first()
        return PostSerializer(posts).data


class ToDoListView(APIView):
    def get(self,request):
        todos = ToDo.query.all()
        return ToDoSerializer(todos, many=True).data

    def post(self,request):
        form = ToDoCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        todo = ToDo(form.text.data, form.is_complete.data, 'Active')
        request.session.add(todo)
        request.session.commit()
        return ToDoSerializer(todo).data, 201

    def delete(self,request):
        toDelete = ToDo.query.filter(ToDo.is_complete == True).all()
        for todo in toDelete:
            request.session.delete(todo)
        request.session.commit()
        todos = ToDo.query.all()
        return ToDoSerializer(todos, many=True).data, 201


class ToDoView(APIView):
    def get(self, id,request):
        todos = ToDo.query.filter_by(id=id).first()
        return ToDoSerializer(todos).data

    def put(self, id,request):
        form = ToDoCompleteForm()
        if not form.validate_on_submit():
            return form.errors, 422
        todo = ToDo.query.filter_by(id=id).first()
        todo.is_complete = form.is_complete.data
        if todo.is_complete:
            todo.status = 'Completed'
        else:
            todo.status = 'Active'
        request.session.commit()
        return ToDoSerializer(todo).data, 201


class ContactListView(APIView):
    def get(self,request):
        contacts = Contact.query.all()
        return ContactSerializer(contacts, many=True).data

    def post(self,request):
        form = ContactCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        contact = Contact(form.text.data, form.first_name.data, form.last_name.data, form.is_selected.data)
        request.session.add(contact)
        request.session.commit()
        return ContactSerializer(contact).data, 201

    def delete(self,request):
        toDelete = Contact.query.filter(Contact.is_selected == True).all()
        for contact in toDelete:
            request.session.delete(contact)
        request.session.commit()
        contacts = Contact.query.all()
        return ContactSerializer(contacts, many=True).data, 201


class ContactView(APIView):
    def get(self, id,request):
        contacts = Contact.query.filter_by(id=id).first()
        return ContactSerializer(contacts).data

    def put(self, id,request):
        form = ContactUpdateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        contact = Contact.query.filter_by(id=id).first()
        contact.first_name = form.first_name.data
        contact.last_name = form.last_name.data
        contact.text = form.text.data
        request.session.commit()
        return ContactSerializer(contact).data, 201

    def delete(self, id,request):
        contact = Contact.query.filter_by(id=id).first()
        request.session.delete(contact)
        request.session.commit()
        contacts = Contact.query.all()
        return ContactSerializer(contacts, many=True).data


class ProjectListView(APIView):
    def get(self,request):
        projects = Project.query.all()
        return ProjectSerializer(projects, many=True).data

    def post(self,request):
        form = ProjectCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        project = Project(form.name.data, form.description.data, form.user_id.data)
        request.session.add(project)
        request.session.commit()
        return ProjectSerializer(project).data, 201

class ProjectView(APIView):
    def get(self, id,request):
        projects = Project.query.filter_by(id=id).first()
        return ProjectSerializer(projects).data

    def put(self, id,request):
        form = ProjectUpdateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        project = Project.query.filter_by(id=id).first()
        project.name = form.name.data
        project.description = form.description.data
        project.user_id = form.user_id.data
        request.session.commit()
        return ProjectSerializer(project).data, 201

    def delete(self, id,request):
        project = Project.query.filter_by(id=id).first()
        request.session.delete(project)
        request.session.commit()
        projects = Project.query.all()
        return ProjectSerializer(projects, many=True).data


class IssueListView(APIView):
    def get(self,request):
        issues = Issue.query.all()
        return IssueSerializer(issues, many=True).data

    def post(self,request):
        form = IssueCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        issue = Issue(form.title.data, form.description.data, form.project_id.data, form.column_id.data,
                      form.tag_id.data, form.milestone_id.data, form.effort_id.data, form.assigned_to_id.data)
        request.session.add(issue)
        request.session.commit()
        return IssueSerializer(issue).data, 201


class IssueView(APIView):
    def get(self, id,request):
        issues = Issue.query.filter_by(id=id).first()
        return IssueSerializer(issues).data

    def put(self, id,request):
        form = IssueCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        issue = Issue.query.filter_by(id=id).first()
        issue.title = form.title.data
        issue.description = form.description.data
        issue.project_id = form.project_id.data
        issue.column_id = form.column_id.data
        issue.tag_id = form.tag_id.data
        issue.milestone_id = form.milestone_id.data
        issue.effort_id = form.effort_id.data
        issue.assigned_to_id = form.assigned_to_id.data
        request.session.commit()
        return IssueSerializer(issue).data, 201

    def delete(self, id,request):
        issue = Issue.query.filter_by(id=id).first()
        request.session.delete(issue)
        request.session.commit()
        issues = Issue.query.all()
        return IssueSerializer(issues, many=True).data


class TagListView(APIView):
    def get(self,request):
        tags = Tag.query.all()
        return TagSerializer(tags, many=True).data

    def post(self,request):
        form = TagCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        tag = Tag(form.name.data, form.description.data, form.color.data)
        request.session.add(tag)
        request.session.commit()
        return TagSerializer(tag).data, 201


class TagView(APIView):
    def get(self, id,request):
        tags = Tag.query.filter_by(id=id).first()
        return TagSerializer(tags).data

    def put(self, id,request):
        form = TagCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        tag = Tag.query.filter_by(id=id).first()
        tag.name = form.name.data
        tag.description = form.description.data
        tag.color = form.color.data
        request.session.commit()
        return TagSerializer(tag).data, 201

    def delete(self, id,request):
        tag = Tag.query.filter_by(id=id).first()
        request.session.delete(tag)
        request.session.commit()
        tags = Tag.query.all()
        return TagSerializer(tags, many=True).data

class MilestoneView(APIView):
    def get(self, id,request):
        milestones = Milestone.query.filter_by(id=id).first()
        return MilestoneSerializer(milestones).data

    def put(self, id,request):
        form = MilestoneCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        milestone = Milestone.query.filter_by(id=id).first()
        milestone.name = form.name.data
        milestone.description = form.description.data
        milestone.due_date = form.due_date.data
        milestone.stats = form.status.data
        request.session.commit()
        return MilestoneSerializer(milestone).data, 201

    def delete(self, id,request):
        milestone = Milestone.query.filter_by(id=id).first()
        request.session.delete(milestone)
        request.session.commit()
        milestones = Milestone.query.all()
        return MilestoneSerializer(milestones, many=True).data

class MilestoneListView(APIView):
    def get(self,request):
        milestones = Milestone.query.all()
        return MilestoneSerializer(milestones, many=True).data

    def post(self,request):
        form = MilestoneCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        milestone = Milestone(form.name.data, form.description.data, form.due_date.data, form.status.data)
        request.session.add(milestone)
        request.session.commit()
        return MilestoneSerializer(milestone).data, 201

class EffortListView(APIView):
    def get(self,request):
        efforts = Effort.query.all()
        return EffortSerializer(efforts, many=True).data

    def post(self,request):
        form = EffortCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        effort = Effort(form.name.data, form.description.data)
        request.session.add(effort)
        request.session.commit()
        return EffortSerializer(effort).data, 201

class EffortView(APIView):
    def get(self, id,request):
        efforts = Effort.query.filter_by(id=id).first()
        return EffortSerializer(efforts).data

    def put(self, id,request):
        form = EffortCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        effort = Effort.query.filter_by(id=id).first()
        effort.name = form.name.data
        effort.description = form.description.data
        request.session.commit()
        return EffortSerializer(effort).data, 201

    def delete(self, id,request):
        effort = Effort.query.filter_by(id=id).first()
        request.session.delete(effort)
        request.session.commit()
        efforts = Effort.query.all()
        return TagSerializer(efforts, many=True).data

class ColumnListView(APIView):
    def get(self,request):
        columns = Column.query.all()
        return ColumnSerializer(columns, many=True).data

    def post(self,request):
        form = ColumnCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        column = Column(form.name.data, form.description.data)
        column.tasks = []
        request.session.add(column)
        request.session.commit()
        return ColumnSerializer(column).data, 201

class ColumnView(APIView):
    def get(self, id,request):
        column = Column.query.filter_by(id=id).first()
        return ColumnSerializer(column).data

    def put(self, id,request):
        form = ColumnCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        column = Column.query.filter_by(id=id).first()
        column.name = form.name.data
        column.description = form.description.data
        request.session.commit()
        return ColumnSerializer(column).data, 201

    def delete(self, id,request):
        column = Column.query.filter_by(id=id).first()
        request.session.delete(column)
        request.session.commit()
        columns = Column.query.all()
        return ColumnSerializer(columns, many=True).data
