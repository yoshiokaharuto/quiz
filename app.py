from flask import Flask , render_template , redirect, url_for,request,session
import db,string,random
from datetime import timedelta
from user import user_bp
from quiz import quiz_bp

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

app.register_blueprint(user_bp)
app.register_blueprint(quiz_bp)

@app.route('/')
def top():
    return render_template('index.html')


@app.route('/',methods = ['POST'])
def login():
    
    mail = request.form.get('mail')
    pw   = request.form.get('pw')
    
    if db.login(mail,pw):
        result = []
        result = db.select_user(mail)
        session['id'] = result[0]
        session['name'] = result[1]
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        if  mail == 'host@morijyobi.ac.jp':
            return redirect(url_for('host_top'))
        else:
            return redirect(url_for('user_top'))
    else:
        error = 'ログインに失敗しました。'
        
        input_data = {'mail':mail,
                      'pw':pw            
        }
        return render_template('top.html',error=error,data = input_data)
    
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('top'))

@app.route('/host_top',methods=['GET'])
def host_top():
    if 'user' in session:
        return render_template('host.html')
    else:
        return redirect(url_for('top'))
    

@app.route('/user_top',methods=['GET'])
def user_top():
    if 'user' in session:
        return render_template('user.html')
    else:
        return redirect(url_for('top'))
    
    
if __name__ == '__main__':
    app.run(debug=True)