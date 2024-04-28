import os,psycopg2,string,random,hashlib

def get_connection():
    url = os.environ['DATABASE_URL1']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset,k=30))
    return salt

def get_hash(password,salt):
    b_pw = bytes(password,'utf-8')
    b_salt = bytes(salt,'utf-8')
    
    hashed_pw = hashlib.pbkdf2_hmac("sha256",b_pw,b_salt,1000).hex()
    
    return hashed_pw

def login(mail,password):
    sql = "SELECT hashed_password , salt FROM quiz_user WHERE mail = %s"
    flg = False
    
    try:
        connection = get_connection()
        cusor = connection.cursor()
        cusor.execute(sql , (mail,))
        user = cusor.fetchone()
        
        if user != None:
            salt = user[1]
            
            hashed_pw = get_hash(password,salt)
            
            if hashed_pw == user[0]:
                flg = True
    
    except psycopg2.DatabaseError:
        flg = True
    finally:
        cusor.close()
        connection.close()
    
    return flg

def register(name,mail,pw):
    sql = "INSERT INTO quiz_user VALUES(default,%s,%s,%s,%s)"
    salt = get_salt()
    hashed_pw = get_hash(pw,salt)
    
    try:
        connecton = get_connection()
        cursor = connecton.cursor()
        
        cursor.execute(sql,(name,mail,hashed_pw,salt))
        count = cursor.rowcount
        connecton.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connecton.close()
    return count

def select_user(mail):
    
    connecton = get_connection()
    cursor = connecton.cursor()
    
    sql = "SELECT id,name FROM quiz_user WHERE mail = %s"
    
    cursor.execute(sql,(mail,))
    result = cursor.fetchone()
    
    cursor.close()
    connecton.close()
    
    return result

def select_mail(mail):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT mail FROM users WHERE mail = %s"
    
    cursor.execute(sql,(mail,))
    row = cursor.fetchone()
    
    print(row)
    if row != None:
        flg = True
    else:
        flg = False
    cursor.close()
    connection.close()
    
    return flg

def quiz_list():
    connection = get_connection()
    cursor  = connection.cursor()
    
    sql = "SELECT quiz_id,question FROM quiz_question"
    
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def quiz_search(question):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT quiz_id,question FROM quiz_question WHERE question LIKE %s "
    key = '%' + question + '%'
    
    cursor.execute(sql,(key,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows 

def quiz_select(id):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT quiz_id,question,answer FROM quiz_question WHERE quiz_id = %s "
    
    cursor.execute(sql,(id,))
    
    rows = cursor.fetchall()
    
    connection.close()
    cursor.close()
    
    return rows


def quiz_list_all():
    
    connection = get_connection()
    cursor  = connection.cursor()
    
    sql = "SELECT quiz_id,question,answer FROM quiz_question"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def quiz_search_all(question):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT quiz_id,question,answer FROM quiz_question WHERE question LIKE %s "
    key = '%' + question + '%'
    
    cursor.execute(sql,(key,))
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows

def quiz_delete(id):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "DELETE FROM quiz_question WHERE quiz_id = %s"
    
    cursor.execute(sql,(id,))
    
    connection.commit()
    
    connection.close()
    cursor.close()


def quiz_register(id,question,answer):
      
    sql = "INSERT INTO quiz_question VALUES(default,%s,%s,%s)"
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(id,question,answer))
        count = cursor.rowcount
        connection.commit()
    
    except psycopg2.DatabaseError:
        count = 0
    
    finally:
        connection.close()
        cursor.close()
    
    return count

def user_list():
    
    connection = get_connection()
    cursor  = connection.cursor()
    
    sql = "SELECT name,mail FROM quiz_user"
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rows