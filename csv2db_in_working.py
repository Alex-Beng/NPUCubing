from app import app, db
from app.models import User, Player, Comp, CompEvents, Events, Result, Entry

import datetime

# 一些基础信息
file_path = "./data/working.csv"
# 以下是某一场比赛(通过app设定的comp_id确定，例如今年(2020)用的是0)
# 开设项目的id，名字，和轮次
event = [
    '333', 
    '222', 
    '333of', 
    '444', 
    '333oh', 
    'py', 
    'sk'
]
col = [
    '三阶速拧', 
    '二阶速拧', 
    '三阶单面', 
    '四阶速拧', 
    '三阶单手',
    '金字塔',
    '斜转'
]
rnd = [
    2,
    2,
    1,
    1,
    1,
    1,
    1
]
compute_way = [
    ['bo3', 'ao5'],
    ['bo3', 'ao5'],
    ['bo3'],
    ['ao5'],
    ['ao5'],
    ['ao5'],
    ['ao5']
]
event2col = dict(zip(event, col))
col2event = dict(zip(col, event))

comp_id = app.config['COMP_ID']
# 插Comp表
comp_name = '第四届校内赛'
comp_date = datetime.date(2020, 10, 31)
db.session.add(
    Comp(
        id = comp_id,
        comp_name = comp_name,
        comp_date = comp_date
    )
)
try:
    db.session.commit()
except Exception as e:
    print("赛事 {}-{} 已经存在，跳过".format(comp_name, comp_id))

# 插event和comp_event表
for i, evt in enumerate(event):
    db.session.add(
        Events(
            name = evt
        )
    )
    try:
        db.session.commit()
    except Exception as e:
        print("项目 {} 已经存在，跳过".format(evt))
    for j in range(rnd[i]):
        db.session.add(
            CompEvents(
                comp_id = comp_id,
                event_name = evt,
                round_cnt = j+1,
                compute_way = compute_way[i][j]
            )
        )
        try:
            db.session.commit()
        except Exception as e:
            print("比赛轮次 {}-{}-{} 已经存在，跳过".format(comp_id, evt, j))
file = open(file_path, encoding='utf-8')


# drop the last \n
idx2col = file.readline().split(',')[:-1]
col2idx = {}
for idx, col in enumerate(idx2col):
    col2idx[col] = idx

# 插与人相关的信息
for row in file.readlines():
    row_info_list = row.split(',')[:-1]
    row_info = dict(zip(idx2col, row_info_list))

    # print(row_info)

    # 获得info后，做插入
    # Player表插入
    # 直接插，except异常做处理
    db.session.add(
    # print(
        Player(
            id = row_info['学号'],
            player_name = row_info['姓名'],
            player_gender = row_info['性别']
        )
    )
    try:
        db.session.commit()
    except Exception as e:
        print("选手 {}-{} 已经存在, 跳过".format(row_info['姓名'], row_info['学号']))
    
    # 插Entry表
    db.session.add(
        Entry(
            comp_id = comp_id,
            sign_id = row_info['序号'],
            player_id = row_info['学号']
        )
    )
    try:
        db.session.commit()
    except Exception as e:
        print("参赛 {}-{} 已经存在, 跳过".format(comp_id, row_info['学号']))
    

        
