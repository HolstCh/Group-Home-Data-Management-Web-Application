from flaskext.mysql import MySQL
from App import app

try:
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'Your Username Here'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'Your Password Here'
    app.config['MYSQL_DATABASE_DB'] = 'youth'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
except Exception as e:
    print(e)
