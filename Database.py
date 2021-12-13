from flaskext.mysql import MySQL
from flask import Flask

app = Flask(__name__)
mysql = MySQL()

class Database:
    try:
        app.config['MYSQL_DATABASE_USER'] = 'chad'
        app.config['MYSQL_DATABASE_PASSWORD'] = '@@Kawa1000'
        app.config['MYSQL_DATABASE_DB'] = 'youth'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)
    except Error as e:
        print(e)

    def selectAllAccounts(self):
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ACCOUNT")
        records = cursor.fetchall()
        for i in records:
            print(i)

    def verifyAccount(self, username, password):
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT * FROM ACCOUNT WHERE username = %s AND password = %s"
        info = (username, password)
        cursor.execute(query, info)
        record = cursor.fetchone()
        if not record:
            print('Error: No account')
        else:
            return True

