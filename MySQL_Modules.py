from mvknow_init import db
from flask_login import UserMixin

class article(db.Model):
    __tablename__='article'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.String(19000))
    created_date=db.Column(db.Date)
    author=db.Column(db.String(100))
    read_num=db.Column(db.Integer)
    abstract=db.Column(db.String(1000))
    read_limit = db.Column(db.Integer)
    read_public=db.Column(db.String(10))
    def __repr__(self):
        return '<article %r>' % self.title

class del_article(db.Model):
    __tablename__ = 'del_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body=db.Column(db.String(19000))
    created_date = db.Column(db.Date)
    author = db.Column(db.String(100))
    read_num = db.Column(db.Integer)
    abstract = db.Column(db.String(1000))
    read_limit = db.Column(db.Integer)
    read_public = db.Column(db.String(10))
    def __repr__(self):
        return '<del_article %r>' % self.title

class user(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    def __repr__(self):
        return '<user %r>' % self.name
