from django.db import models
from wtforms.validators import Email

from app.server import db, flask_bcrypt

# Create your models here.
class ChatInfo(models.Model):
    _id =  models.AutoField(primary_key=True)
    ChatType = models.TextField()
    ChatRole = models.TextField()
    ChatDate = models.TextField()
    ChatTime = models.TextField()
    ChatFrom = models.TextField()
    ChatPersonal = models.BooleanField()
    Message = models.TextField()




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, info={'validators': Email()})
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.email


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.user_id = g.user.id

    def __repr__(self):
        return '<Post %r>' % self.title


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(120), nullable=False, default='Active')
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, text, is_complete, status):
        self.text = text
        self.is_complete = is_complete
        self.status = status

    def __repr__(self):
        return '<ToDo %r>' % self.text


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=True)
    icon_url = db.Column(db.String(120), nullable=True)
    is_selected = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, text, first_name, last_name, is_selected):
        self.text = text
        self.first_name = first_name
        self.last_name = last_name
        self.is_selected = is_selected

    def __repr__(self):
        return '<ToDo %r>' % self.text


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('Contact', backref='project')
    user_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return '<Project %r>' % self.name


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.relationship('Project', backref='issue')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    tag = db.relationship('Tag', backref='issue')
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=True)
    milestone = db.relationship('Milestone', backref='issue')
    milestone_id = db.Column(db.Integer, db.ForeignKey('milestone.id'), nullable=True)
    effort = db.relationship('Effort', backref='issue')
    effort_id = db.Column(db.Integer, db.ForeignKey('effort.id'), nullable=True)
    assigned_to = db.relationship('Contact', backref='issue')
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=True)
    column_id = db.Column(db.Integer, db.ForeignKey('column.id'), nullable=False, default=1)
    column = db.relationship('Column', backref='tasks')
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, title, description, project_id, column_id, tag_id, milestone_id, effort_id, assigned_to_id):
        self.title = title
        self.description = description
        self.project_id = project_id
        self.column_id = column_id
        self.tag_id = tag_id
        self.milestone_id = milestone_id
        self.effort_id = effort_id
        self.assigned_to_id = assigned_to_id

    def __repr__(self):
        return '<Issue %r>' % self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(32), nullable=False, default="ffffff")

    def __init__(self, name, description, color):
        self.name = name
        self.description = description
        self.color = color

    def __repr__(self):
        return '<Tag %r>' % self.name

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(120), nullable=False, default='Active')

    def __init__(self, name, description, due_date, status):
        self.name = name
        self.description = description
        self.due_date = due_date
        self.stats = status

    def __repr__(self):
        return '<Milestone %r>' % self.name

class Effort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Effort %r>' % self.name

class Column(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Column %r>' % self.name