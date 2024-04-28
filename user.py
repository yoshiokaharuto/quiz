from flask import Flask , render_template , redirect, url_for,request,session,Blueprint
import db,string,random
from datetime import timedelta
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os,email.utils

user_bp = Blueprint('user',__name__,url_prefix='/user')

@user_bp.route('/sign_up')
def sign_up():
    return render_template('user/sign_up.html')

@user_bp.route('sign_up_confirm',methods=["POST"])  
def sign_up_confirm():
    
    name = request.form.get('name')
    mail = request.form.get('mail')
    pw   = request.form.get('pw')
    
    if name == '':
        error = 'ユーザ名が未入力です'
        return render_template('user/sign_up.html',error=error,mail=mail,pw=pw)
    if mail == '':
        error = 'メールアドレスが未入力です'
        return render_template('user/sign_up.html',error=error,name=name,pw=pw)    
    if pw == '':
        error = 'パスワードが未入力です'
        return render_template('user/sign_up.html',error=error,name=name,mail=mail)
    
    session['name'] = name
    session['mail'] = mail
    session['pw']   = pw
    
    return render_template('user/sign_up_confirm.html',name=name,mail=mail)
    
@user_bp.route('/sign_up_execute')
def sign_up_execute():
    
    name = session['name']
    mail  = session['mail']
    pw    = session['pw']
    count = db.register(name,mail,pw)
    print(count)
    
    if count == 1:
        return redirect(url_for('user.user_conclusion'))
    else:
        error = '登録に失敗しました。'
        return render_template('user/sign_up.html',error = error)

@user_bp.route('/user_conclusion')
def user_conclusion():
    return render_template('user/user_conclusion.html')


@user_bp.route('/send_page')
def send_page():
    return render_template('user/mail_send.html',login=0)

@user_bp.route('/send_mail',methods=['POST'])
def send_mail():
    to = request.form.get('to')
    session['mail'] = to
    if db.select_mail(to):
        mail_send(to)
        return redirect(url_for('user.navigateSend'))
    else:
        error = 'メールアドレスが間違ってします。もう一度入力してください'
        return render_template('user/mail_send.html',error = error)

@user_bp.route('/send', methods=['GET'])
def navigateSend():
    return render_template('user/mail_send_execute.html',login=0)

@user_bp.route('/edit_page')
def edit_page():
    return render_template('user/pw_edit.html',login=0)

@user_bp.route('/edit_password' , methods=['POST'])
def edit_password():
    pw = request.form.get('password')
    
    count = db.edit_password(pw)
    
    if count == 1:
        return render_template('user/pw_edit_complete.html',login=0)
    else:
        return render_template('user/pw_edit.html',login=0)
    



def mail_send(to):
    ID = 'h.yoshioka.sys22@morijyobi.ac.jp'
    PASS = os.environ['MAIL_PASS']
    HOST = 'smtp.gmail.com'
    PORT = 587
    
    
    subject = 'パスワード再設定'
    message = 'パスワード変更手続きのお申し込みがありました。<br>下記のURLへアクセスして、手続きを続行してください。<br>'
    url    =  'http://127.0.0.1:5000/user/edit_page'
    body = message + url
    
    msg = MIMEMultipart()
    
    msg.attach(MIMEText(body,'html'))
    
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr(('システム',ID))
    msg['To']   = email.utils.formataddr(('ユーザ様',to))
    
    server = SMTP(HOST,PORT)
    server.starttls()
    
    server.login(ID,PASS)
    server.send_message(msg)
    
    server.quit()
    
@user_bp.route('/user_list')
def user_list():
    
    user = db.user_list()
    
    return render_template('user/user_list.html', user_list = user)