from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# 受保护页面重定向到'login'页面
# 需要保护的页面只需加上login_required的修饰器
# login_required重定向时还会加上next参数，可用这个参数登陆后返回！
login.login_view = 'login'



from app import routes, models
