from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from config import *
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=DB_Connection
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =DB_COMMIT_TEAR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DB_TRACK
app.config['SECRET_KEY']=FLASK_SECRET_KEY

app.config['CKEDITOR_SERVE_LOCAL'] = CKEDITOR_LOCAL
app.config['CKEDITOR_HEIGHT'] = CK_HEIGHT
app.config['CKEDITOR_FILE_UPLOADER'] = CKEDITOR_UPLOAD_PATH

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PATH'] = os.path.join(basedir,'static','upload')
login_manager = LoginManager()
login_manager.init_app(app)

bootstrap=Bootstrap(app)
moment=Moment(app)
db=SQLAlchemy(app)
ckeditor = CKEditor(app)


