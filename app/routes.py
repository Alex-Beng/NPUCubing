from app import app
from app.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    # return "Hello, World!"
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():    
    # 已经登录
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # 实例化表单
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效用户名或密码')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='登录', form=form)


@app.route('/gradein')
def gradein():
    return '瞅啥，还没写好'


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/living')
def living():
    return '瞅啥，还没写好'