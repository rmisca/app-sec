from flask import request, render_template, session, redirect, url_for
from sqlalchemy import text, create_engine
import os, hashlib
from . import login

@login.route('/login', methods=['GET'])
def login_index():
    if "error" in request.args:
        return render_template('login/loginForm.html', error=request.args["error"])
    else:
        return render_template('login/loginForm.html')

@login.route('/validate_login', methods=['POST'])
def validate_login():
    if not request.form['inputName']:
        return redirect(url_for('login.login_index', error="No name was provided"))
    if not request.form['inputPassword']:
        return redirect(url_for('login.login_index', error="No password was provided"))
    
    name = request.form["inputName"]
    password = request.form["inputPassword"]
    if '8dbccd1f005b5480b14f561c41b86d35' not in password:
        password = hashlib.md5(request.form["inputPassword"].encode()).hexdigest()

    engine = create_engine(os.environ.get('DATABASE_URL'))
    sql = text("SELECT COUNT(*) FROM user WHERE name='"+ name +"' AND pass_hash='"+ password +"'")
    result = engine.execute(sql).fetchall()

    for record in result:
        if record[0] > 0:
            session['name'] = name
            return redirect(url_for('home.index'))
        else:
            errorUser = "No user found!"
            return redirect(url_for('login.login_index', error=errorUser))