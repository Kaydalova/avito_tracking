from . import app
from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash

from . import app, db
from .forms import LoginForm, RegisterForm
from .models import User

@app.route('/')
def index_view():
    '''
    Функция для отображения главной страницы.
    '''
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    """
    Страница с формой регистрации.
    Если форма валидна создается пользователь
    и происходит редирект в профиль пользователя.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('profile_view'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    """
    Страница авторизации пользователя.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile_view'))
        flash('Неверные учетные данные', 'error')
        return redirect(url_for('login_view'))
    return render_template('login.html', form=form)


@app.route('/profile')
@login_required
def profile_view():
    """
    Профиль пользователя.
    """
    return render_template('profile.html')


@app.route('/logout/')
@login_required
def logout_view():
    """
    Выход из профиля и редирект на страницу авторизации.
    """
    logout_user()
    flash('Вы вышли из профиля.')
    return redirect(url_for('login_view'))