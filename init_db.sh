rm -r app.db migrations/
flask db init
flask db migrate -m "init db"
flask db upgrade