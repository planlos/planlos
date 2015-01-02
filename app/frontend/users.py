# coding: utf-8

from ..services import events,users
from ..services import locations as locations

from flask import render_template, abort, current_app, redirect, url_for, request, flash, Blueprint
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import Login_Form
from ..services.user_service import No_Such_User

mod = Blueprint('userpages', __name__,
                template_folder='templates')

#####
##### login, logout, signup, etc
#####

@mod.route("/logout", methods=['GET'])
@login_required
def logout():
    users.logout()
    return redirect(url_for('events.index'))


@mod.route("/login", methods=['GET', 'POST'])
def login():
    form = Login_Form(request.form)
    if form.validate_on_submit():
        try:
            users.login(form['uid'].data, form['password'].data, form['remember'].data)
            flash("Successfully logged in! Welcome ....%s" % request.args.get('next'))
            return redirect(request.args.get('next') or url_for( 'userpages.me'))
        except No_Such_User as e:
            flash(e)
    return render_template("login.html", form=form)

@mod.route("/me", methods=['GET'])
def me():
    return redirect(url_for('events.index'))


@mod.route("/signup", methods=['GET', 'POST'])
def signup():
    form = Signup_Form(username=request.args.get("username", None),
                       email=request.args.get("email", None),
                       next=request.args.get("next", None))
    if form.validate_on_submit():
        try: 
            request_user_account(form.username.data,
                                 form.password.data,
                                 form.email.data)
            flash("Thanks for signing up! An Activation mail has been sent to you (%s) please come back..." % (form.email.data) )
            return redirect( url_for('index') )
        except User_Exists:
            flash("Error: User already exists")
        except Email_Not_Unique:
            flash("Error: Email is already taken")
    return render_template('users/signup.html', form=form)

@mod.route("/resetpassword", methods=['GET'])
def resetpassword():
    return render_template("users/resetpassword.html")
