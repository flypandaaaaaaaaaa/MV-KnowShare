from flask_mail import Mail,Message
from flask import render_template
from mvknow_init import app
from threading import Thread
from MySQL_Modules import user

app.config['MAIL_SERVER'] = 'xxxxxxxxxxx'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'xxxxxxxxxxx@qq.com'
app.config['MAIL_PASSWORD'] = 'xxxxxxxxxxxxx'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[IT知识分享平台通知]'
app.config['FLASKY_MAIL_SENDER'] = 'IT知识分享平台 <xxxxxxxx@qq.com>'
mail=Mail(app)


def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(subject,template,**kwargs):
    User_List=[]
    AllUser = user.query.all()
    for i in AllUser:
        User_List.append(i.email)
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'] ,recipients=User_List)
    msg.body=render_template(template + '.txt',**kwargs)
    msg.html=render_template(template + '.html',**kwargs)
    thr=Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr
