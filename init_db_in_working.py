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

u = User(user_name='npuca')
u.set_password('npuca')
db.session.add(u)
db.session.commit()