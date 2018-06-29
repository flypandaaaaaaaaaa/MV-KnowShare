from flask_mail import Mail,Message
from flask import render_template
from mvknow_init import app
from threading import Thread

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'example@qq.com'
app.config['MAIL_PASSWORD'] = 'xxxxxxxxxxxxxxxx'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <example@qq.com>'
mail=Mail(app)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject,template,**kwargs):
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'] ,recipients=['example@163.com'])
    msg.body=render_template(template + '.txt',**kwargs)
    msg.html=render_template(template + '.html',**kwargs)
    thr=Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr
