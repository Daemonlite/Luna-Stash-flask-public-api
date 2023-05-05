from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  

db = SQLAlchemy()

#user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile = db.Column(db.String(255))
    bio = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, email, password, profile):
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'profile': self.profile,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,nullable = False)
    title = db.Column(db.String(255),nullable=False)
    body = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,user_id,title,body):
        self.user_id = user_id
        self.title = title
        self.body = body

    def to_dict(self):
        return{
            'id':self.id,
            'user_id':self.user_id,
            'title':self.title,
            'body':self.body,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Comments(db.model):
    id = db.Column(db.Integer,primary_key = True)
    post_id = db.Column(db.Integer,nullable = False)
    username = db.Column(db.String(200),nulable=False)
    userprofile = db.Column(db.String(200),nulable=False)
    content = db.Column(db.String(200),nulable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,post_id,username,userprofile,content):
        self.post_id = post_id
        self.username = username
        self.userprofile = userprofile
        self.content = content

    def to_dict(self):
        return{
            'id':self.id,
            'post_id':self.post_id,
            'username':self.username,
            'userprofile':self.userprofile,
            'content':self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at

        }