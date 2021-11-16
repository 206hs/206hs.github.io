import sys
from flask import Flask, render_template,request, jsonify
from supersqlite import sqlite3
import string
import random
import os
from datetime import datetime
import platform
import pyotp
if platform.system()=='Linux': path='//var//www//html//hs.db'
else:path='hs.db'
app = Flask(__name__)
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/registered' , methods=['POST'])
def registered():
    conn = sqlite3.connect('hs.db')
    c=conn.cursor()
    key=''.join(random.choices(string.ascii_uppercase+'234567',k=16))
    c.execute("""INSERT INTO staff VALUES (?,?,?)""",(request.form['Username'],request.form['Password'],key))
    conn.commit()
    return jsonify({'url':pyotp.TOTP(key).provisioning_uri(name=request.form['Username'],issuer_name='HengSeng') })

@app.route('/check' , methods=['POST'])
def check():
    conn = sqlite3.connect('hs.db')
    c=conn.cursor()
    c.execute("SELECT * FROM staff WHERE username = ?",(request.form['Username'],))
    if pyotp.TOTP(c.fetchone()[2]).now()==request.form['Token']:return jsonify({'result':True })
    else:return jsonify({'result':False })




@app.route('/')
def hs():
    conn = sqlite3.connect(path, timeout=30)
    c = conn.cursor()
    c.execute("SELECT * FROM safe")
    safe=c.fetchall()
    c.close()
    conn = sqlite3.connect(path, timeout=30)
    c = conn.cursor()
    c.execute("SELECT * FROM staff")
    staff=c.fetchall()
    c.close()
    conn = sqlite3.connect(path, timeout=30)
    c = conn.cursor()
    c.execute("SELECT * FROM log")
    log=c.fetchall()
    return render_template('index.html',safe=safe,staff=staff,log=log)
@app.route('/temp')
def temp():
    return render_template('temp.html')
@app.route('/remove')
def remove():
    os.remove("hs.db")
@app.route('/create')
def create():
    conn = sqlite3.connect(path, timeout=30)
    c = conn.cursor()
    c.execute("CREATE TABLE safe(safe_id TEXT PRIMARY KEY,hkid TEXT,pin TEXT);")
    for i in range (65,67):
        for j in range (65,90):
            for num in range (1,21):
                tempnum=num
                if len(str(tempnum))==1: tempnum='0'+str(tempnum)
                if random.choice([True,False]): 
                    c.execute("""INSERT INTO safe VALUES (?,?,?)""",(chr(i)+chr(j)+str(tempnum),None,None))
                else:
                    hkid=random.choice(string.ascii_uppercase)+str(random.randint(100000, 999999))
                    remainder=(((ord(hkid[0])-55)*8+int(hkid[1])*7+int(hkid[2])*6+int(hkid[3])*5+int(hkid[4])*4+int(hkid[5])*3+int(hkid[6])*2)%11)
                    if remainder==0:check='0'
                    elif remainder==1:check='A'
                    else: check=(11-remainder)
                    c.execute("""INSERT INTO safe VALUES (?,?,?)""",(chr(i)+chr(j)+str(tempnum),str(hkid)+'('+str(check)+')','123456'))
                conn.commit()
    print('done')
@app.route('/create2')
def create2():
    conn = sqlite3.connect(path, timeout=30)
    c = conn.cursor()
    c.execute("CREATE TABLE staff(username TEXT PRIMARY KEY,password TEXT,key TEXT);")
    #for i in range (65,67):
    #    for j in range (65,90):
    #        for num in range (1,6):
    #            tempnum=num
    #            c.execute("""INSERT INTO staff VALUES (?,?)""",('staff'+chr(i)+chr(j)+str(tempnum),'123'))
    conn.commit()
    print('done')
@app.route('/create3')
def create3():
    conn = sqlite3.connect(path, timeout=30)
    c = conn.cursor()
    c.execute("CREATE TABLE log(time TEXT PRIMARY KEY,staff TEXT,event TEXT);")
    conn.commit()
    print('done')

@app.route('/save', methods=['GET', 'POST'])
def save():
    conn = sqlite3.connect(path, timeout=30)
    c = conn.cursor()
    if not request.form['Hkid']:hkid=None
    else:hkid=request.form['Hkid']
    if not request.form['Pin']:pin=None
    else:pin=request.form['Pin']
    c.execute("UPDATE safe SET hkid = ? , pin = ? WHERE safe_id = ?",(hkid,pin,request.form['Safeid']))
    conn.commit()
    c.close()
    conn = sqlite3.connect('hs.db')
    c=conn.cursor()
    c.execute("SELECT * FROM safe")
    safe=c.fetchall()
    c.close()
    conn = sqlite3.connect('hs.db')
    c=conn.cursor()
    c.execute("SELECT * FROM staff")
    staff=c.fetchall()
    c.close()
    return render_template('index.html',safe=safe,staff=staff,branchcookie=request.form['Branchcookie'])

@app.route('/log', methods=['POST'])
def log():
    conn = sqlite3.connect('hs.db', timeout=30)
    c=conn.cursor()
    c.execute('INSERT INTO log VALUES(?,?,?)',( datetime.now().strftime("%d/%m/%Y %H:%M:%S"),request.form['Staff'],request.form['Event']))
    conn.commit()
    c.close()
    return 'logged'

@app.route('/loop', methods=['POST'] )
def loop():
    conn = sqlite3.connect(path, timeout=30)
    c = conn.cursor()
    c.execute("SELECT * FROM safe")
    safe=c.fetchall()
    c.close()
    return jsonify({'safe':safe})


@app.route('/update', methods=['POST'] )
def update():
    conn = sqlite3.connect(path, timeout=30)
    c = conn.cursor()
    c.execute("UPDATE safe SET hkid = ? , pin = ? WHERE safe_id = ?",(request.form['Hkid'],request.form['Pin'],request.form['Safeid'],))
    conn.commit()
    c.close()
    return 'updated'
if __name__=='__main__':
    app.debug=True
    app.run(host="0.0.0.0",port=8000)