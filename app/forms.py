# 表单类们
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_name = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class GradeinForm(FlaskForm):
    player_id = StringField('学号', validators=[DataRequired()])
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
    rround = IntegerField('轮次', validators=[DataRequired()])
    item = StringField('项目', validators=[DataRequired()])
    submit = SubmitField('提交')