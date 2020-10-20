# 表单类们
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

from app import app

class LoginForm(FlaskForm):
    user_name = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class GradeinForm(FlaskForm):
    sign_id = StringField('选手序号', validators=[DataRequired()])
    # comp_id在app的全局变量中定义
#     comp_id = SelectField('比赛编码', choices=[(1, 'yay'), (2, 'ya')], render_kw={
#             'class': 'form-control'
#         },
#   validators=[DataRequired()])
    rround = IntegerField('轮次', validators=[DataRequired()])
    item = StringField('项目', validators=[DataRequired()])
    res1 = StringField('成绩1')
    res2 = StringField('成绩2')
    res3 = StringField('成绩3')
    res4 = StringField('成绩4')
    res5 = StringField('成绩5')
    submit = SubmitField('提交')

class LiveOptionForm(FlaskForm):
    # rround = IntegerField('轮次', validators=[DataRequired()])
    rround = SelectField(
        label='轮次', 
        choices=range(1, 3), 
        default=1
        )
    # item = StringField('项目', validators=[DataRequired()])
    events = app.config['COMP_EVENT']
    item = SelectField(
        label='项目', 
        choices=events,
        default='333'
        )
    submit = SubmitField('提交')

class GradedelForm(FlaskForm):
    sign_id = StringField('选手序号', validators=[DataRequired()])
    rround = IntegerField('轮次', validators=[DataRequired()])
    item = StringField('项目', validators=[DataRequired()])
    submit = SubmitField('确认删除')