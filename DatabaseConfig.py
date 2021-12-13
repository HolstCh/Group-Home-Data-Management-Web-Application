from flaskext.mysql import MySQL
from App import app

try:
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'chad'
    app.config['MYSQL_DATABASE_PASSWORD'] = '@@Kawa1000'
    app.config['MYSQL_DATABASE_DB'] = 'youth'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)
except Error as e:
    print(e)