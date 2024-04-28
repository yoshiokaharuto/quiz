from flask import Blueprint,render_template,url_for,request,redirect,session
import db,string,random

quiz_bp = Blueprint('quiz',__name__,url_prefix='/quiz')

@quiz_bp.route('/quiz_register')
def quiz_register():
    return render_template('quiz/quiz_register.html')

@quiz_bp.route('/quiz_register_result' , methods=['POST'])
def quiz_register_result():
    
    id = request.form.get('id')
    question = request.form.get('question')
    answer  = request.form.get('answer')
    
    count = db.quiz_register(id,question,answer)
    
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('quiz/quiz_register_result.html' ,msg=msg)
    else:
        error = '登録に失敗しました。'
        return render_template('quiz/quiz_register.html' , error=error)
    
@quiz_bp.route('/quiz_list')
def quiz_list():
    quiz = db.quiz_list()
    return render_template('quiz/quiz_list.html' , list = quiz)


@quiz_bp.route('/search_page')
def search_page():
    return render_template('quiz/quiz_search.html')

@quiz_bp.route('/search_result',methods=['POST'])
def search_result():
    
    question = request.form.get('question')
    
    result = db.quiz_search(question)
    return render_template('quiz/quiz_search_result.html' ,list=result)

@quiz_bp.route('/quiz_detail')
def quiz_detail():
    
    id = request.args.get('id')
    result = db.quiz_select(id)
    session['quiz_answer'] = result[0][2]
    # print(session['quiz_answer'])
    # session['quiz_question'] = result[0]
    # session['quiz_question'] = result[1]
    return render_template('quiz/quiz_detail.html', result=result)

@quiz_bp.route('quiz_answer', methods=['post'])
def quiz_answer():
    
    answer = request.form.get('answer')
    print(session['quiz_answer'])
    
    if session['quiz_answer'] == answer:
        session.pop('quiz_answer')
        return render_template('quiz/quiz_true.html')
    else:
        session.pop('quiz_answer')
        return render_template('quiz/quiz_fail.html')
    
@quiz_bp.route('quiz_delete')
def quiz_delete():
    return render_template('quiz/quiz_delete.html')

@quiz_bp.route('quiz_delete_result',methods=['POST'])
def quiz_delete_result():
    
    id = request.form.get('id')
    result = db.quiz_delete(id)
    return render_template('quiz/quiz_delete_result.html', result = result)

@quiz_bp.route('/quiz_list_all')
def quiz_list_all():
    quiz = db.quiz_list_all()
    return render_template('quiz/quiz_list_all.html', list=quiz)

@quiz_bp.route('/quiz_search_all')
def quiz_search_all():
    return render_template('quiz/quiz_search_all.html')


@quiz_bp.route('/quiz_search_all_result',methods=['POST'])
def quiz_search_all_result():
    
    question = request.form.get('question')
    
    result = db.quiz_search_all(question)
    return render_template('quiz/quiz_search_all_result.html' ,list=result)




