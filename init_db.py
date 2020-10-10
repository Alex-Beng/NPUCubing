from app import app, db
from app.models import User, Player, Comp, CompEvents, Events, Result, Entry

import datetime

# 创建表，谢谢
db.create_all()
# 删光数据，谢谢
print("deleting below data...")
yaya = [User, Player, Comp, CompEvents, Events, Result, Entry]
for tb in yaya:
    t = tb.query.all()
    print(tb, t)
    [db.session.delete(tt) for tt in t]
    db.session.commit()

# user添加数据
u = User(user_name='alexbeng')
u.set_password('10920971')
db.session.add(u)
db.session.commit()


# player添加数据
p_names = ['吴语嘉', '李想', '赵狗']
p_gender = ['男', '男', '女']
for i in range(len(p_names)):
    p = Player(id=i+20200, player_name=p_names[i], player_gender=p_gender[i])
    # print(p)
    db.session.add(p)
db.session.commit()

# Comp添加数据
comp_names = ['第四届校内赛', '第五届校内赛']
comp_dates = [datetime.date(2020, 5, 15), datetime.date(2021, 5, 20)]
for i in range(len(comp_names)):
    c = Comp(id=i, comp_name=comp_names[i], comp_date=comp_dates[i])
    # print(c)
    db.session.add(c)
db.session.commit()


# Events添加数据
event_names=['222', '333', '333of', 'czz']
for i in range(len(event_names)):
    e = Events(name=event_names[i])
    # print(e)
    db.session.add(e)
db.session.commit()

# CompEvents添加数据
comp_ids = [0, 0, 0, 0]
event_names = ['222', '333', '333of', 'czz']
round_nums = [2, 2, 1, 1]
for i in range(len(comp_ids)):
    ce = CompEvents(comp_id=comp_ids[i], event_name=event_names[i], round_num=round_nums[i])
    db.session.add(ce)
db.session.commit()

# Entry添加数据
comp_ids = [0, 0, 0]
sign_ids = [0, 2, 1]
player_ids = [20200, 20201, 20202]
for i in range(len(comp_ids)):
    e = Entry(comp_id=comp_ids[i], sign_id=sign_ids[i], player_id=player_ids[i])
    db.session.add(e)
db.session.commit()
