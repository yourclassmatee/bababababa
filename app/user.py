from flask import render_template, url_for, request, redirect, session, flash
from app import webapp
from app.timetable_db import find_user, create_user

@webapp.route('/user/new', methods=["GET", "POST"])
def new_user():
    if(request.method == 'POST'):
        return do_create_user(request.form)
    else:
        return render_template("user_form.html")

def do_create_user(form):
    if(form):
        #print(form)
        #check if user already exist
        username = form.get("username")
        try_find = find_user(username)
        if try_find:
            flash("Error: User: " + username + " already exists!")
            return render_template("user_form.html")

        usr = create_user(form.get("username"), form.get("password"))

        #print(usr)

        # set session
        session['username'] = username
        return redirect(url_for('dashboard', username=username))