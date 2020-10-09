from app import app, db
from app.models import User, Player, Comp, Result, Entry

import datetime

# 创建表，谢谢
db.create_all()
# 删光数据，谢谢
print("deleting below data...")
yaya = [User, Player, Comp, Result, Entry]
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
    p = Player(id=i, player_name=p_names[i], player_gender=p_gender[i])
    # print(p)
    db.session.add(p)
db.session.commit()

# Comp添加数据
comp_names = ['某届魔方赛', '某届魔方赛2']
comp_dates = [datetime.date(2020, 5, 15), datetime.date(2020, 5, 20)]
for i in range(len(comp_names)):
    c = Comp(id=i, comp_name=comp_names[i], comp_date=comp_dates[i])
    # print(c)
    db.session.add(c)
db.session.commit()



