from flask import render_template, redirect, url_for, flash, make_response
from app.main.forms import LoginForm
from ..models import Role,User
from . import main

@main.route("/")
@main.route("/home")
def index():
    roles = Role.query.all()
    return render_template('index.html', roles = roles)

@main.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  
        user = User.query.filter_by(username=form.usr.data).first()
        if user is None:
            flash('login failed for {}'.format(form.usr.data))
        else:   
            flash('login success.. for {}'.format(form.usr.data))
            return redirect(url_for('main.index'))
    return render_template('login.html', title='Login', form = form)

@main.route('/dummy')
def dummy():
    return str(User.query.get_or_404(1))   
