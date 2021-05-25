# -*- coding: utf-8 -*-
"""
@author: Adarsh
"""

import requests
import json
from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'a'

app.config["MYSQL_HOST"] = "remotemysql.com"
app.config["MYSQL_USER"] = "nqMuOdCOcu"
app.config["MYSQL_PASSWORD"] = "XrJrqijIk3"
app.config["MYSQL_DB"] = "nqMuOdCOcu"


mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods = ["POST"])
def register():
   if request.method == "POST":
       name = request.form["name"]
       email = request.form["email"]
       mobileno = request.form["mobileno"]
       password = request.form["password"]
       cursor = mysql.connection.cursor()
       cursor.execute('INSERT INTO registrationData VALUES (NULL,% s,% s,% s,% s)',(name,email,mobileno,password))
       mysql.connection.commit()
       msg = 'You have Successfully Registered!'
   return render_template('index.html', msg = msg)
  
@app.route('/login', methods = ["POST", "GET"])
def login():
    global userid
    global account
    msg = ""
    if request.method == "POST":
        user_name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM registrationData WHERE name = % s AND password = % s',(user_name, password),)
        account = cursor.fetchone()
        print (account)
        
        if account:
           session['loggedin'] = True
           session['id'] = account[0]
           userid = account[0]
           session['email'] = account[2]
           session['username'] = account[1]
           msg = 'You have Sucessfully Logged In!'
       
           return render_template('process.html', msg = msg)
   
        else:
            msg = 'Incorrect User Name / Password'

    return render_template('login.html', msg = msg)

"""
Attached OCR API for detectecting text from Images in many languages though it is currently set in english. See  list of available language codes can be found on https://ocr.space/OCRAPI
"""

def ocr_space_url(url, overlay=False, api_key='50d04a4f1288957', language='eng'):
   
    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()
     
@app.route('/upload', methods = ["POST"])
def upload_url():
    global output
    if request.method == "POST":
         url = request.form["url"]
         name = session["username"]
         email = session["email"]
         cursor = mysql.connection.cursor()
         cursor.execute('INSERT INTO saveURL VALUES(NULL,% s,% s,% s)',(name,email,url))
         mysql.connection.commit()
         test_url = ocr_space_url(url , language='eng')
         print(test_url)
         data=json.loads(test_url)
         output = data['ParsedResults'][0]['ParsedText']
         session['text'] = str(output)
    return render_template("process.html", output = output)
        


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True,port=8080)