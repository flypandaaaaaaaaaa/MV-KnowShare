from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email
from flask_ckeditor import  CKEditorField

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    abstract = StringField('abstract',validators=[DataRequired()])
    read_limit = StringField('limit')
    read_public = StringField('read_public')
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('提交')

class LoginForm(FlaskForm):
	username = StringField('用户名',validators=[DataRequired('请输入用户名')])
	password = PasswordField('密码',validators=[DataRequired('请输入密码')])
	submit = SubmitField('登陆')

class AdminInfoForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired('请输入用户名')])
    password = PasswordField('密码',validators=[DataRequired('请输入密码')])
    mail=StringField('邮箱',validators=[DataRequired('请输入邮箱地址'),Email('邮箱地址不正确')])
    submit = SubmitField('录入信息')