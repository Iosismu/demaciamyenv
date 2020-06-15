from flask import Flask, request, render_template, redirect, url_for, abort, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import pymysql
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import socket
import smtplib
import random
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'school.mingky.me'
app.config['MYSQL_USER'] = 'team02'
app.config['MYSQL_PASSWORD'] = 'KIT'
app.config['MYSQL_DB'] = 'team02'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'



mysql = MySQL(app)
conn = pymysql.connect(host = 'school.mingky.me', user='team02', password='KIT', db = 'team02', charset='utf8')



@app.route('/')
def index():
    return render_template("index.html")

#@app.route('/pro', methods=['GET','POST'])
#def pro():
    #teer = ""
   # if request.method == 'GET':
       # return render_template("profile2.html")
   # else:
        #if request.form['top']:
       #     switch request.form[a]:
              #  case ''
            


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
    
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM usertbl WHERE email = '"+email+"'")

        user = cursor.fetchone()

        if len(user) is 1:
            return render_template("index.html")
        else:
            return render_template("Login.html")
    else:
        return render_template("Login.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")

@app.route('/fin')
def fin():
     return render_template('finPassword.html')

@app.route('/cer', methods=["GET", "POST"])
def cer():
    ret = ()
    if request.method == 'GET':
        return render_template('Certification.html')
    else:
        cer = request.form['cernum']
        
        db = conn.cursor()
        db.execute("SELECT cer_num FROM usertbl WHERE cer_num = %s",(int(cer)))
        
        conn.commit()
        ret = db.fetchone()
        db.close()
        if len(ret) is 1:    
            return render_template("Login.html")
        else:
            return render_template("Certification.html")
        

@app.route('/sign', methods=["GET","POST"])
def sign():
    if request.method == 'GET':
        return render_template('Signup.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        session['email'] = request.form['email']
        session['name'] = request.form['name']
        session['password'] = request.form['password']
        
        
        num = random_num()
        contents = "Certification Number is :{}".format(num)
        message = MIMEText(contents, _charset='euc-kr')
        message['Subject'] = "Demacia 인증번호"
        message['From'] = 'seongbinpark0309@gmail.com'
        message['To'] = email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("seongbinpark0309@gmail.com", "Kgb8220!")
        server.sendmail("seongbinpark0309@gmail.com", email, message.as_string())
        server.quit()

        db = conn.cursor()
        db.execute("INSERT INTO usertbl (email,pw,nickname,cer_num) VALUES (%s,%s,%s,%s)",(email,password,name,int(num)))
        conn.commit()
        db.close()

        return render_template("Certification.html", testdata = email)



        #token = s.dumps(email, salt='email-confirm')
        #msg = Message('Confirm Email', sender='evanpark333@gmail.com', recipients=[email])

        #link = url_for('confirm_email', token=token, _external=True)

        #msg.body = 'Your link is {}'.format(link)

        
        #mail.send(msg)

        #return '<h1> The email you entered is {}. The token is {}<h1>'.format(email, token)
      
    
        
        



#@app.route('/confirm_email/<token>')
#def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return 'The token is expired!'
    return 'The token works!'



def random_num():

    ran_num = random.randrange(000000,999999)

    return ran_num

if __name__ == '__main__':
    app.config['SECRET_KEY'] = '1651dfdf5461af561ad321-reg561efgr6g51_fewf3651'
    app.run(debug=True)
    





