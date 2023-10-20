from flask import render_template, redirect, url_for, flash
from app.main.forms import LoginForm
from . import main

@main.route("/")
@main.route("/home")
def index():
    user = {'username' : 'rossi'}
    posts = [
        {'author':'mario', 'message':'ciao'},
        {'author':'anna', 'message':'welcome'},
    ]
    return render_template('index.html', posts = posts, user=user)

@main.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  
        flash('login success.. for {}'.format(form.usr.data))
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Login', form = form)