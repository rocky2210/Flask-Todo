from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app import db
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm

# Login Route
@bp.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Checking hash
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Login Successfully","success")
                return redirect(url_for('main.todos'))
            else:
                flash("Wrong Password - Try Again","danger")
        else:
            flash("That user not exist","danger")
    return render_template('auth/login.html',form=form)

# Register Route
@bp.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! Your are now able to log in.",'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

# Logout Route
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout successfully","success")
    return redirect(url_for('auth.login'))

