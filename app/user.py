from flask import render_template, url_for, request, redirect, session, flash
from app import webapp

@webapp.route('/user/new', methods=["GET", "POST"])
def new_user():
    return render_template("user_form.html")

