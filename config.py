import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # 设置默认值是个好习惯
    SECRET_KEY = os.environ.get('SECRET_KEY') or '社团部傻逼，脑子全是屎'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER =  'smtp.163.com'
    MAIL_PORT =  465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'yfast_send@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'KZXYSNSKSKWUJILA'
    ADMINS = ['yfast_send@163.com']


    CSV_PATH = "./data/working.csv"
    # 比赛设置
    COMP_ID = 0
    COMP_EVENT = [
        '333', 
        '222', 
        '333of', 
        '444', 
        '333oh', 
        'py', 
        'sk'
    ]
    COMP_EVENT_CHINESE = [
        '三阶速拧', 
        '二阶速拧', 
        '三阶单面', 
        '四阶速拧', 
        '三阶单手',
        '金字塔',
        '斜转'
    ]
    COMP_ROUND_NUM = [
        2,
        2,
        1,
        1,
        1,
        1,
        1
    ]
    COMP_ROUND_COMPUTE_WAY = [
        ['bo3', 'ao5'],
        ['bo3', 'ao5'],
        ['bo3'],
        ['ao5'],
        ['ao5'],
        ['ao5'],
        ['ao5']
    ]
