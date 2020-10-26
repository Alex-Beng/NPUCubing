from app import app, db
from app.forms import LoginForm, GradeinForm, LiveOptionForm, GradedelForm
from app.models import User, Player, Comp, CompEvents, Events, Result, Entry
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, send_file, send_from_directory
from werkzeug.urls import url_parse

# 取最好
def bo3(res):
    performs = list(res[-5:][:3])
    for idx,perf in enumerate(performs):
        if perf < 0:
            performs[idx] = float("inf")
    # print(performs)
    return min(performs)

# 去尾平均
def ao5(res):
    performs = list(res[-5:])
    for idx,perf in enumerate(performs):
        if perf < 0:
            performs[idx] = float("inf")
    del performs[performs.index(max(performs))]
    del performs[performs.index(min(performs))]
    # print(performs)
    return sum(performs)/3

@app.route('/favicon.ico')
def get_fav():
    return send_from_directory('../', 'npuca.ico')


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

        db_compevent = db.session.query(CompEvents).get((comp_id, form_event, form_round))
        if not db_compevent:
            flash("赛事未开设此项目或轮次不正确")
            return redirect(url_for('gradein'))
        # print(db_compevent.compute_way)
        # 验证成绩有效
        form_res = []
        form_res.append(form.res1.data)
        form_res.append(form.res2.data)
        form_res.append(form.res3.data)
        form_res.append(form.res4.data)
        form_res.append(form.res5.data)

        if db_compevent.compute_way == 'bo3':
            form_res = form_res[:3]

        form_parsed_res = []
        try:
            for res in form_res:
                if res != '':
                    value = int(res)
                    form_parsed_res.append(value)
        except Exception:
            flash("成绩不符合规范")
            return redirect(url_for('gradein'))
        if db_compevent.compute_way == 'ao5' and len(form_parsed_res)!=5 \
        or db_compevent.compute_way == 'bo3' and len(form_parsed_res)!=3:
            flash("成绩数量不对鸭")
            return redirect(url_for('gradein'))
                    
        # 插入数据库库
        result = Result(
            player_id=db_players.player_id, 
            comp_id=comp_id,
            round=form_round,
            item=form_event
            )
        res_num = len(form_parsed_res)
        if res_num >= 1:
            result.res1=form_parsed_res[0]
        if res_num >= 3:
            result.res2=form_parsed_res[1]
            result.res3=form_parsed_res[2]
        if res_num == 5:
            result.res4=form_parsed_res[3]
            result.res5=form_parsed_res[4]
        db.session.add(result)
        try:
            db.session.commit()
        except Exception:
            flash("此人此项目轮次已录入")
            return redirect(url_for('gradein'))
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
    labels = ['排名', '选手序号', '名字', '成绩', '详细成绩', '', '', '', '']
    content = []
    if form.validate_on_submit():
        comp_id = app.config['COMP_ID']

        form_round = form.rround.data
        form_event = form.item.data
        form_gender = form.gender.data

        # parser gender
        if form_gender in ['男', '女', '其他']:
            form_gender = list(form_gender)
        else:
            form_gender = ['男', '女', '其他']
        
        # 验证项目轮次正确
        db_compevent = db.session.query(CompEvents).get((comp_id, form_event, form_round))
        if not db_compevent:
            flash("赛事未开设此项目或轮次不正确")
            return redirect(url_for('living'))

        # 从result表查询成绩
        curr_res = db.session \
            .query(Entry.sign_id,
                   Player.player_name, 
                   Result.res1,
                   Result.res2,
                   Result.res3,
                   Result.res4,
                   Result.res5) \
            .join(Player, Result.player_id==Player.id) \
            .join(Entry, Entry.player_id==Result.player_id) \
            .filter(Result.round==form_round, Result.comp_id==comp_id, Result.item==form_event, Player.player_gender.in_(form_gender)) \
            .all()
            # wdnmd这个查询的第二个join似乎跟版本相关，之后要改成直接用sql

        if len(curr_res)==0:
            flash("此轮次尚未有成绩更新")
            return redirect(url_for('living'))
        # 取最好
        if db_compevent.compute_way == 'bo3':
            curr_res = sorted(curr_res, key=bo3)
        # 取去尾平均
        elif db_compevent.compute_way == 'ao5':
            curr_res = sorted(curr_res, key=ao5)

        
        for idx, row in enumerate(curr_res):
            # print(row)
            new_row = [idx+1]
            for i in range(2):
                new_row.append(row[i])
            # print(new_row)
            for i in range(2, 7):
                try:
                    time_in_ms = int(row[i])
                    if time_in_ms < 0:
                        int('')
                    time_in_s = "%.2f"%(time_in_ms/1000.0)
                    new_row.append(time_in_s)
                except Exception:
                    new_row.append('DNF')
            # print(new_row)
                
            if db_compevent.compute_way == 'bo3':
                best = bo3(row)/1000.0
                if best == float("inf"):
                    new_row.insert(-5, 'DNF')
                else:
                    new_row.insert(-5, "%.2f"%best)
            elif db_compevent.compute_way == 'ao5':
                best = ao5(row)/1000.0
                if best == float("inf"):
                    new_row.insert(-5, 'DNF')
                else:
                    new_row.insert(-5, "%.2f"%best)
            # print(row, new_row)
            content.append( new_row )
        return render_template('living.html', form=form, labels=labels, content=content, title='直播')
    return render_template('living.html', form=form, title='直播')

@app.route('/gradedel', methods=['GET', 'POST'])
@login_required
def gradedel():
    form = GradedelForm()
    # 确认删除
    if form.validate_on_submit():
        # 获得当前comp_id
        comp_id = app.config['COMP_ID']
        
        # 验证选手报名了比赛
        form_sign_id = form.sign_id.data
        db_players = db.session.query(Entry).get((comp_id, form_sign_id))
        if not db_players:
            flash("选手不存在或未参加")
            return redirect(url_for('gradedel'))

        # 验证项目及轮次是否正确
        form_round = form.rround.data
        form_event = form.item.data

        db_compevent = db.session.query(CompEvents).get((comp_id, form_event, form_round))
        if not db_compevent:
            flash("赛事未开设此项目或轮次不正确")
            return redirect(url_for('gradedel'))
        
        # 验证该选手有无录入的成绩
        db_res = db.session.query(Result).get((db_players.player_id, comp_id, form_round, form_event))
        if not db_res:
            flash("该选手此轮次未录入")
            return redirect(url_for('gradedel'))
        
        # 进行删除
        db.session.delete(db_res)
        db.session.commit()
        flash("成功删除{}的{}第{}轮成绩".format(db_players.player_id, form_event, form_round))
        return redirect(url_for('gradedel'))

    return render_template('gradedel.html', title='删除', form=form)
