from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://blog:AXY78$a1.@47.104.161.61:4306/blog'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='DADSSADSA'

app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PATH'] = basedir+'\\static\\upload'

bootstrap=Bootstrap(app)
moment=Moment(app)
db=SQLAlchemy(app)
ckeditor = CKEditor(app)


