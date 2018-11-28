from flask import render_template, url_for, request, make_response, flash, redirect, session
from app import webapp
from app.timetable_db import *


@webapp.route('/login', methods=["GET", "POST"])
def login():
    if(request.method == 'POST'):
        return do_login(request.form)
    else:
        return render_template("login_form.html")

@webapp.route('/logout/<username>', methods=["GET"])
def logout(username):
    return do_logout(username)

def do_login(form):
    if(form):
        username = form.get("username")
        password = form.get("password")

        response = check_password(username, password)
        if response == 0:
            #set session
            session['username'] = username
            if not check_photo_exist(username):
                return redirect(url_for("dashboard", username=username))
            else:
                return redirect(url_for("display_table",username=username))
        elif response == 1:
            flash("ERROR: wrong password")
            return redirect(url_for("login"))
        else:
            flash("ERROR: user does not exist")
            return redirect(url_for("login"))

def do_logout(username):
    if(check_session(username)):
        session.pop('username', None)
        flash("INFO: logout successful")
        return redirect(url_for('login'))

def check_session(username):
    if(session.get('username')):
        if username == session['username']:
            return True
    return False