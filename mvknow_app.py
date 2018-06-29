from flask import render_template,request,make_response,url_for,send_from_directory,Markup
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired
from MySQL_Modules import article
from mvknow_init import db,app,ckeditor
from mvknow_contact_mail import send_mail
from flask_ckeditor import  CKEditorField
import time

import datetime,os,random,json,re,urllib


class mail_form(FlaskForm):
    subject=StringField('subject',validators=[DataRequired()])
    message=TextAreaField('message',validators=[DataRequired()])
    submit=SubmitField('Submit')


@app.route('/',methods=['GET','POST'])
def Home():
    Article_list = article.query.all()
    Article_list_recent = article.query.order_by(article.created_date.desc()).limit(5).offset(0)
    Article_list_most = article.query.order_by(article.read_num.desc()).limit(5).offset(0)
    return render_template('index.html',Article_list=Article_list,Article_list_recent=Article_list_recent,Article_list_most=Article_list_most)

@app.route('/readall',methods=['GET','POST'])
def readall():
    Article_list = article.query.order_by(article.created_date.desc())
    return render_template('full-width.html',Article_list=Article_list)

# @app.route('/readall/<art_number>',methods=['GET','POST'])
# def readone(art_number):
#     Article= article.query.filter_by(id=art_number).first()
#     Article.read_num=Article.read_num+1
#     db.session.commit()
#     Article_list_recent = article.query.order_by(article.created_date.desc()).limit(5).offset(0)
#     Article_list_most = article.query.order_by(article.read_num.desc()).limit(5).offset(0)
#     return render_template('single.html_old', Article=Article, Article_list_recent=Article_list_recent, Article_list_most=Article_list_most)
@app.route('/readall/<art_number>',methods=['GET','POST'])
def readone(art_number):
    Article= article.query.filter_by(id=art_number).first()
    Article.read_num=Article.read_num+1
    db.session.commit()
    return render_template('single.html', Article=Article)



@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        send_mail(request.form.get('subject'), 'mail/contact', context=request.form.get('message'))
    return render_template('contact.html')



class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	body = CKEditorField('Body', validators=[DataRequired()])
	submit = SubmitField()
def GetNowTime():
    return time.strftime("%Y-%m-%d",time.localtime(time.time()))

@app.route('/editor', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        new_article=article(title=title,body=body,created_date=GetNowTime(),author='fangjianqi',read_num=0)
        db.session.add(new_article)
        db.session.commit()
        return render_template('post.html',title=title,body=body)
    return render_template('editor.html', form=form)


@app.route('/files/<filename>')
def files(filename):
	path = app.config['UPLOADED_PATH']
	return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
@ckeditor.uploader
def upload():
	f = request.files.get('upload')
	f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
	url = url_for('files', filename=f.filename)
	return url


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
