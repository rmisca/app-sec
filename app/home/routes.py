from flask import request, render_template, session, redirect, url_for
from sqlalchemy import text, create_engine
import os
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
        for record in result1:
            if 'admin' in record[1]:
                return render_template('home/admin.html', events=result2, users=result1)
            else:
                if 'admin' not in record[1] and record[3] == 1:
                    return render_template('home/userlvl1.html', events=result2)
                elif 'admin' not in record[1] and record[3] == 2:
                    return render_template('home/userlvl2.html', events=result2)

@home.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login.login_index'))