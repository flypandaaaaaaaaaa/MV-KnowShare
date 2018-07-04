from flask_mail import Mail,Message
from flask import render_template
from mvknow_init import app
from threading import Thread
from MySQL_Modules import user
from config import *
app.config['MAIL_SERVER'] = Mail_Sender_Server
app.config['MAIL_PORT'] = Mail_Sender_Port
app.config['MAIL_USE_TLS'] = Mail_TLS
app.config['MAIL_USE_SSL'] = Mail_SSL
app.config['MAIL_USERNAME'] = Mail_Sender_Username
app.config['MAIL_PASSWORD'] = Mail_Sender_Password
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = Mail_Subject
app.config['FLASKY_MAIL_SENDER'] = Mail_Sender
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
