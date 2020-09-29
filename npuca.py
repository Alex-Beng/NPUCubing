from app import app, db
from app.models import User, Post


# 设置 flask shell 上下文\
# 让 flask shell 里面db有东西
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
