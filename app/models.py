from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.user_name)
    
    # 密码儿
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Player(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    player_name = db.Column(db.String(64), index=True)
    player_gender = db.Column(db.String(5))

    def __repr__(self):
        return '<Player {}>'.format(self.player_name)

class Comp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comp_name = db.Column(db.String(128), index=True)
    comp_date = db.Column(db.Date)

class Result(db.Model):
    player_id = db.Column(db.String(15), db.ForeignKey('player.id'), primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('comp.id'), primary_key=True)
    round = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(10), primary_key=True)
    # 用毫秒数表示成绩，同wca db
    res1 = db.Column(db.BigInteger)
    res2 = db.Column(db.BigInteger)
    res3 = db.Column(db.BigInteger)
    res4 = db.Column(db.BigInteger)
    res5 = db.Column(db.BigInteger)

# 参赛关系
entry = db.Table('entry',
    db.Column('comp_id', db.Integer, db.ForeignKey('comp.id'), primary_key=True),
    db.Column('player_id', db.String(15), db.ForeignKey('player.id'), primary_key=True)
)

