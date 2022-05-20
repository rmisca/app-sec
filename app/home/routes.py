from flask import request, render_template, session, redirect, url_for
from sqlalchemy import text, create_engine
import os, hashlib
from . import home

@home.route('/', methods = ['GET'])
def index():
    if "name" in session:
        name = session["name"]
    else:
        name = None

    if name is None:
        return redirect(url_for('login.login_index'))
    else:
        engine = create_engine(os.environ.get('DATABASE_URL'))
        sql1 = text("SELECT * FROM user")
        result1 = engine.execute(sql1).fetchall()
        sql2 = text("SELECT * FROM event")
        result2 = engine.execute(sql2).fetchall()
        if 'admin' in name:
            return render_template('home/admin.html', events=result2, users=result1)
        else:
            for record in result1:
                if name in record[1]:
                    if record[3] == 1:
                        return render_template('home/userlvl1.html', events=result2)
                    elif record[3] == 2:
                        return render_template('home/userlvl2.html', events=result2)

@home.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login.login_index'))

@home.route('/create_user')
def create_user():
    if "error" in request.args:
        return render_template('home/create_user.html', error=request.args["error"])
    else:
        return render_template('home/create_user.html')

@home.route("/handle_create_user", methods=['POST'])
def handle_register():
    if not request.form['inputName']:
        return redirect(url_for('home.create_user', error="No name was provided"))
    if not request.form['inputTeam']:
        return redirect(url_for('home.create_user', error="No team was provided"))
    if not request.form['inputLevel']:
        return redirect(url_for('home.create_user', error="No level was provided"))
    if not request.form['inputActive']:
        return redirect(url_for('home.create_user', error="No status was provided"))
    if not request.form['inputPassword']:
        return redirect(url_for('home.create_user', error="No password was provided"))
    
    name = request.form["inputName"]
    team = request.form["inputTeam"]
    level = request.form["inputLevel"]
    active = request.form["inputActive"]
    password = hashlib.md5(request.form["inputPassword"].encode()).hexdigest()

    engine = create_engine(os.environ.get('DATABASE_URL'))
    sql = text("INSERT INTO user (name, team, level, active, pass_hash) VALUES (:n, :t, :l, :a, :p)")
    sql2 = text("SELECT name FROM user")
    result2 = engine.execute(sql2).fetchall()
    
    for record in result2:
        if name in record[0]:
            return redirect(url_for('home.create_user', error="User already exists!"))    

    try:
        engine.execute(sql, n=name, t=team, l=level, a=active, p=password)
    except ValueError:
        return ValueError

    return redirect(url_for('home.index', error="Success"))

@home.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    engine = create_engine(os.environ.get('DATABASE_URL'))
    if "nameInput" in request.form:
        name = request.form["nameInput"]
        sql = text("DELETE FROM user WHERE name = '"+ name +"'")
        try:
            engine.execute(sql)
        except ValueError:
            return ValueError
        
        return redirect(url_for('home.index'))
    else:
        sql = text("SELECT name FROM user")
        result = engine.execute(sql).fetchall()
        return render_template('home/delete_user.html', users=result)

@home.route('/update_user')
def update_user():
    return render_template('home/update_user.html')

@home.route('/handle_update_user', methods=['GET', 'POST'])
def handle_update_user():
    if not request.form['inputName']:
        return redirect(url_for('home.update_user', error="No name was provided"))
    if not request.form['inputTeam']:
        return redirect(url_for('home.update_user', error="No team was provided"))
    if not request.form['inputLevel']:
        return redirect(url_for('home.update_user', error="No level was provided"))
    if not request.form['inputActive']:
        return redirect(url_for('home.update_user', error="No status was provided"))
    if not request.form['inputPassword']:
        return redirect(url_for('home.update_user', error="No password was provided"))
    
    name = request.form["inputName"]
    team = request.form["inputTeam"]
    level = request.form["inputLevel"]
    active = request.form["inputActive"]
    password = hashlib.md5(request.form["inputPassword"].encode()).hexdigest()

    engine = create_engine(os.environ.get('DATABASE_URL'))
    sql = text("UPDATE user SET name = '"+ name +"', team='"+ team +"', level='"+ level +"', active='"+ active +"', pass_hash='"+ password +"' WHERE name='"+ name +"'")
    sql2 = text("SELECT name FROM user")
    result2 = engine.execute(sql2).fetchall()
    for record in result2:
        if name in record[0]:
            engine.execute(sql)
    return redirect(url_for('home.index', error="Success"))

@home.route('/create_event')
def insert_event():
    if "error" in request.args:
        return render_template('home/create_event.html', error=request.args["error"])
    else:
        return render_template('home/create_event.html')

@home.route('/handle_create_event', methods=['POST'])
def handle_create_event():
    if not request.form['nameInput']:
        return redirect(url_for('home.insert_event', error="No name was provided"))
    if not request.form['descriptionInput']:
        return redirect(url_for('home.insert_event', error="No description was provided"))
    if not request.form['priorityInput']:
        return redirect(url_for('home.insert_event', error="No priority was provided"))
    
    name = request.form["nameInput"]
    description = request.form["descriptionInput"]
    priority = request.form["priorityInput"]

    engine = create_engine(os.environ.get('DATABASE_URL'))
    sql = text("INSERT INTO event (name, description, prio) VALUES (:n, :d, :p)")
    sql2 = text("SELECT name FROM event")
    result2 = engine.execute(sql2).fetchall()
    
    for record in result2:
        if name in record[0]:
            return redirect(url_for('home.insert_event', error="Event already exists!"))
    try:
        engine.execute(sql, n=name, d=description, p=priority)
    except ValueError:
        return ValueError

@home.route('/delete_event', methods=['GET', 'POST'])
def delete_event():
    engine = create_engine(os.environ.get('DATABASE_URL'))
    if "nameInput" in request.form:
        name = request.form["nameInput"]
        sql = text("DELETE FROM event WHERE name = '"+ name +"'")
        try:
            engine.execute(sql)
        except ValueError:
            return ValueError
        
        return redirect(url_for('home.index'))
    else:
        sql = text("SELECT name FROM event")
        result = engine.execute(sql).fetchall()
        return render_template('home/delete_event.html', events=result)