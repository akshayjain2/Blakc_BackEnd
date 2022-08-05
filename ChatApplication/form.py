from wtforms_alchemy import model_form_factory
from wtforms import StringField, BooleanField, IntegerField, DateTimeField
from wtforms.validators import DataRequired

from app.server import db
from app.models import User, Post, ToDo, Contact, Project, Issue, Tag, Milestone, Effort, Column

BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class UserCreateForm(ModelForm):
    class Meta:
        model = User


class SessionCreateForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class PostCreateForm(ModelForm):
    class Meta:
        model = Post


class ToDoCreateForm(ModelForm):
    class Meta:
        model = ToDo


class ToDoCompleteForm(Form):
    text = StringField('text')
    is_complete = BooleanField('is_complete')


class ContactCreateForm(ModelForm):
    class Meta:
        model = Contact


class ContactUpdateForm(Form):
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    text = StringField('text')


class ProjectCreateForm(ModelForm):
    name = StringField('name')
    description = StringField('description')
    user_id = IntegerField('user_id')


class ProjectUpdateForm(Form):
    name = StringField('name')
    description = StringField('description')
    user_id = IntegerField('user_id')


class IssueCreateForm(ModelForm):
    title = StringField('title')
    description = StringField('description')
    project_id = IntegerField('project_id')
    column_id = IntegerField('column_id')
    tag_id = IntegerField('tag_id')
    milestone_id = IntegerField('milestone_id')
    effort_id = IntegerField('effort_id')
    assigned_to_id = IntegerField('assigned_to_id')

class TagCreateForm(ModelForm):
    class Meta:
        model = Tag

class MilestoneCreateForm(ModelForm):
    name = StringField('name')
    description = StringField('description')
    due_date = DateTimeField('due_date', format='%Y-%m-%d %H:%M')
    status = StringField('status')

class EffortCreateForm(ModelForm):
    class Meta:
        model = Effort


class ColumnCreateForm(ModelForm):
    class Meta:
        model = Column