
from flask import render_template, url_for, session, redirect, request, flash
from app import webapp


@webapp.route('/')
def main():
    #if session.get('username'):
        #return redirect(url_for('dashboard', username=session.get('username')))
    return render_template("main.html")
