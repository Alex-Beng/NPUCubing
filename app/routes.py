from app import app, db
from app.forms import LoginForm, GradeinForm, LiveOptionForm
from app.models import User, Player, Comp, CompEvents, Events, Result, Entry
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, send_file
from werkzeug.urls import url_parse

# 去尾平均
def ao5(res):
    performs = list(res[-5:])
    for idx,perf in enumerate(performs):
        if perf < 0:
            performs[idx] = float("inf")
    del performs[performs.index(max(performs))]
    del performs[performs.index(min(performs))]
    print(performs)
    return sum(performs)/3


@app.route('/')
@app.route('/index')
def index():
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


@app.route('/gradein', methods=['GET', 'POST'])
@login_required
def gradein():
    form = GradeinForm()
    # 提交成功，插入数据库
    if form.validate_on_submit():
        # 获得当前comp_id
        comp_id = app.config['COMP_ID']
        
        # 验证选手报名了比赛
        form_sign_id = form.sign_id.data
        db_players = db.session.query(Entry).get((comp_id, form_sign_id))
        # print(db_players, type(db_players))
        if not db_players:
            flash("选手不存在或未参加，请核对后重新录入")
            return redirect(url_for('gradein'))
        
        # 验证项目及轮次是否正确
        form_round = form.rround.data
        form_event = form.item.data

        db_compevent = db.session.query(CompEvents).get((comp_id, form_event))
        if not db_compevent:
            flash("赛事未开设此项目")
            return redirect(url_for('gradein'))
        
        db_round = db_compevent.round_num
        if db_round < form_round or form_round < 1:
            flash("项目轮次不正确")
            return redirect(url_for('gradein'))
        
        # 验证成绩有效
        form_res = []
        form_res.append(form.res1.data)
        form_res.append(form.res2.data)
        form_res.append(form.res3.data)
        form_res.append(form.res4.data)
        form_res.append(form.res5.data)
        # print(form_res)
        form_parsed_res = []
        try:
            for res in form_res:
                if res != '':
                    # 只要别输入负数就行
                    form_parsed_res.append(int(res))
        except Exception as e:
            flash("成绩不符合规范")
            
            return redirect(url_for('gradein'))
        res_num = len(form_parsed_res)
        if res_num==1 or res_num==3 or res_num==5:
            pass
        else:
            flash("成绩数量不对鸭")
            
        # print(form_parsed_res)
        
        # 插入数据库库
        result = Result(
            player_id=db_players.player_id, 
            comp_id=comp_id,
            round=form_round,
            item=form_event
            )
        
        if res_num >= 1:
            result.res1=form_parsed_res[0]
        if res_num >= 3:
            result.res2=form_parsed_res[1]
            result.res3=form_parsed_res[2]
        if res_num == 5:
            result.res4=form_parsed_res[3]
            result.res5=form_parsed_res[4]
        db.session.add(result)
        db.session.commit()
        flash("录入成功，工具人请继续")
        return redirect(url_for('gradein'))
    
    return render_template('gradein.html', title='录入', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/living', methods=['GET', 'POST'])
def living():
    form = LiveOptionForm()
    labels = ['选手序号', '名字', '成绩', '详细成绩', '', '', '', '']
    content = []
    if form.validate_on_submit():
        comp_id = app.config['COMP_ID']

        form_round = form.rround.data
        form_event = form.item.data

        # 验证项目轮次正确
        db_compevent = db.session.query(CompEvents).get((comp_id, form_event))
        if not db_compevent:
            flash("赛事未开设此项目")
            return redirect(url_for('living'))
        db_round = db_compevent.round_num
        if db_round < form_round or form_round < 1:
            flash("此项目妹有这个轮次")
            return redirect(url_for('living'))

        # 从result表查询成绩
        curr_res = db.session \
            .query(Entry.sign_id,
                #    Player.id,
                   Player.player_name, 
                #    Result.item,
                   Result.res1,
                   Result.res2,
                   Result.res3,
                   Result.res4,
                   Result.res5) \
            .join(Player, Result.player_id==Player.id) \
            .join(Entry, Result.player_id==Entry.player_id) \
            .filter(Result.round==form_round, Result.comp_id==comp_id, Result.item==form_event) \
            .all()

        if len(curr_res)==0:
            flash("此轮次尚未有成绩更新")
            return redirect(url_for('living'))
        # 取最好
        if form_round == 1:
            curr_res = sorted(curr_res, key=lambda res: min(res[-5], res[-4], res[-3]))
        # 取去尾平均
        elif form_round == 2:
            curr_res = sorted(curr_res, key=ao5)

        for row in curr_res:
            # new_row = [i for i in row]
            new_row = []
            for i in row:
                if i == -1:
                    new_row.append('DNF')
                elif i == -2:
                    new_row.append('DNS')
                else:
                    new_row.append(i)
            if form_round == 1:
                new_row.insert(-5, min(row[-5], row[-4], row[-3]))
            elif form_round == 2:
                new_row.insert(-5, ao5(row))
            print(row, new_row)
            content.append( new_row )
        return render_template('living.html', form=form, labels=labels, content=content)
    return render_template('living.html', form=form)
