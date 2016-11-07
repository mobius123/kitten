import os
from compute import compute as compute_function

from flask import Flask, render_template, request, redirect, url_for
from forms import ComputeForm
from db_models import db, User, Compute
from flask.ext.login import LoginManager, current_user, \
     login_user, logout_user, login_required
from app import app


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import login_form
    form = login_form(request.form)
    if request.method == 'POST' and form.validate():
        ConsumerKey = form.get_user()
        login_user(user)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)
    

login_manager = LoginManager()
login_manager.init_app(app)