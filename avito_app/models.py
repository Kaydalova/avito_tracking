import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager

from .constants import MAX_USERNAME_LENGTH

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    '''
    Модель пользователя.
    Attrs:
    - id: уникальный идентификатор пользователя
    - username: юзернейм пользователя, уникальное значение
    - email: почта пользователя, используется для отправки
    статуса добавленного вопроса
    - tg_username: имя пользователя в телеграм
    - password: пароль
    - created_on: дата создания профиля
    - is_confirmed: подтверждена ли почта
    - confirm_link: уникальная ссылка для подтверждения почты
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(MAX_USERNAME_LENGTH), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    tg_username = db.Column(db.String(20), nullable=True, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.Date, default=datetime.date.today)
    is_confirmed = db.Column(db.Boolean, default=False)
    confirm_link = db.Column(db.String(32), unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'{self.id} - {self.username}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()
    

class Account(db.Model):
    '''
    Модель акаунта в avito.
    - id: уникальный идентификатор аккаунта
    - user: пользователь
    - autoreply_on: включен ли автоответ
    - avito_token: токен доступа к API avito
    '''
    id = db.Column(db.Integer, primary_key=True)
    autoreply_on = db.Column(db.Boolean, default=False)

