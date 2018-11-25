from flask import render_template, url_for, request, make_response, flash, redirect, session
from app import webapp

@webapp.route('/login', methods=["GET", "POST"])
def login():
        return render_template("login_form.html")
