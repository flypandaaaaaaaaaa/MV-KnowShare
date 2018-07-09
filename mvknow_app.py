import os,hashlib
from flask import render_template,request,url_for,send_from_directory,redirect
from flask_login import login_required,login_user,logout_user,current_user
from MySQL_Modules import article,del_article,user
from mvknow_init import db,app,ckeditor,login_manager
from mvknow_contact_mail import send_mail
from mvknow_form import PostForm,LoginForm,AdminInfoForm
from mvknow_func import GetNowTime,GetIDList
from Get_article_list import Get_article
from move_article import move_article

@app.route('/',methods=['GET'])
def Home():
    FirstPageID=GetIDList(1,7)
    get_article=Get_article(FirstPageID,5)
    Article_list = get_article.Get_article_page_list_desc_id()
    Article_list_recent = get_article.Get_article_list_recent_desc()
    Article_list_most = get_article.Get_article_list_most_desc()
    return render_template('index.html',Article_list=Article_list,Article_list_recent=Article_list_recent,Article_list_most=Article_list_most,lastpage='#',nextpage='2')

@app.route('/page/<page>',methods=['GET'])
def page(page):
    PageID = GetIDList(int(page),7)
    get_article=Get_article(PageID,5)
    Article_list = get_article.Get_article_page_list_desc_id()
    Article_list_recent = get_article.Get_article_list_recent_desc()
    Article_list_most = get_article.Get_article_list_most_desc()
    if int(page) <= 1:
        lastpage='#'
        nextpage=2
    else:
        lastpage=int(page)-1
        nextpage=int(page)+1
    return render_template('index.html',Article_list=Article_list,Article_list_recent=Article_list_recent,Article_list_most=Article_list_most,lastpage=lastpage,nextpage=nextpage)

@app.route('/readall',methods=['GET'])
def readall():
    PageID = GetIDList(1,5)
    get_article=Get_article(PageID,5)
    Article_list = get_article.Get_article_page_list_desc_id()
    return render_template('full-width.html',Article_list=Article_list,lastpage='#',nextpage='2')

@app.route('/readallpage/<page>',methods=['GET'])
def readallpage(page):
    PageID = GetIDList(int(page),5)
    get_article=Get_article(PageID,5)
    Article_list = get_article.Get_article_page_list_desc_id()
    if int(page) <= 1:
        lastpage='#'
        nextpage=2
    else:
        lastpage=int(page)-1
        nextpage=int(page)+1
    return render_template('full-width.html',Article_list=Article_list,lastpage=lastpage,nextpage=nextpage)

@app.route('/readall/<art_number>',methods=['GET'])
def readone(art_number):
    Article= article.query.filter_by(id=art_number).first()
    Article.read_num=Article.read_num+1
    db.session.commit()
    return render_template('single.html', Article=Article)

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method=='POST':
        send_mail(request.form.get('subject'), 'mail/contact', context=request.form.get('message'))
    return render_template('contact.html')

@app.route('/newarticle', methods=['GET', 'POST'])
@login_required
def newarticle():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        abstract=form.abstract.data
        read_limit=form.read_limit.data
        read_public=form.read_public.data
        new_article=article(title=title,body=body,created_date=GetNowTime(),author=current_user.name,read_num=0,abstract=abstract,read_limit=read_limit,read_public=read_public)
        db.session.add(new_article)
        db.session.commit()
        return render_template('post.html',title=title,body=body)
    return render_template('editor.html', form=form)

@app.route('/edit/<art_number>', methods=['GET', 'POST'])
@login_required
def edit(art_number):
    form=PostForm()
    Article= article.query.filter_by(id=art_number).first()
    Del_Article = del_article.query.filter_by(id=art_number).first()
    if Article is None:
        Article_content=Del_Article
    else:
        Article_content=Article
    if form.validate_on_submit():
        Article_content.title=form.title.data
        Article_content.abstract=form.abstract.data
        Article_content.body=form.body.data
        Article_content.read_limit = form.read_limit.data
        Article_content.read_public=form.read_public.data
        db.session.commit()
        return render_template('post.html',title=form.title.data,body=form.body.data)
    form.title.data=Article_content.title
    form.abstract.data=Article_content.abstract
    form.body.data=Article_content.body
    form.read_limit.data=Article_content.read_limit
    form.read_public.data=Article_content.read_public
    return render_template('editor.html',form=form)

@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    Article_list = article.query.order_by(article.created_date.desc())
    del_Article_list = del_article.query.order_by(del_article.created_date.desc())
    return render_template('manage.html',Article_list=Article_list,del_Article_list=del_Article_list)

@app.route('/del/<art_number>', methods=['GET', 'POST'])
@login_required
def move_article(art_number):
    move_article(art_number).offline_article()
    return redirect(url_for('manage'))

@app.route('/online/<art_number>', methods=['GET', 'POST'])
@login_required
def online_article(art_number):
    move_article(art_number).online_article()
    return redirect(url_for('manage'))

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

@app.route('/login' ,methods=['GET', 'POST'])
def login():
    MVLoginForm=LoginForm()
    if MVLoginForm.validate_on_submit():
        FormUserName=MVLoginForm.username.data
        FormPassword=MVLoginForm.password.data
        EncryptFormPassword = hashlib.md5(FormPassword.encode('utf-8')).hexdigest()
        DBUserInfo = user.query.filter_by(name=FormUserName).first()
        if DBUserInfo is None:
            MVLoginForm.username.data='用户名不存在!'
            return render_template('login.html',MVLoginForm=MVLoginForm)
        elif EncryptFormPassword != DBUserInfo.password:
            MVLoginForm.username.data='密码错误!'
            return render_template('login.html',MVLoginForm=MVLoginForm)
        elif EncryptFormPassword == DBUserInfo.password:
            login_user(DBUserInfo)
            return redirect(url_for('manage'))
    return render_template('login.html',MVLoginForm=MVLoginForm)

@login_manager.user_loader
def user_loader(id):
    Adminuser = user.query.filter_by(id=id).first()
    return Adminuser

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Home'))

@app.route('/regadmin' ,methods=['GET', 'POST'])
@login_required
def regadmin():
    MVAdminInfoForm=AdminInfoForm()
    FormUsername=MVAdminInfoForm.username.data
    FormPassword=MVAdminInfoForm.password.data
    FormEmail=MVAdminInfoForm.mail.data
    if request.method=='POST':
        DBuserInfo = user.query.filter_by(name=FormUsername).first()
        if DBuserInfo:
            MVAdminInfoForm.username.data='用户已经存在，录入失败！'
            return render_template('regadmin.html',MVAdminInfoForm=MVAdminInfoForm)
        else:
            EncryptFormPassword=hashlib.md5(FormPassword.encode('utf-8')).hexdigest()
            UserInfoRow=user(name=FormUsername,password=EncryptFormPassword,email=FormEmail)
            db.session.add(UserInfoRow)
            db.session.commit()
            return redirect(url_for('manage'))
    else:
        return render_template('regadmin.html', MVAdminInfoForm=MVAdminInfoForm)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,threaded=True)

