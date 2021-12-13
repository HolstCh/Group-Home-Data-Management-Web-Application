from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from DatabaseConfig import mysql
from App import app


@app.route("/")
def main():
    return redirect(url_for("home"))

@app.route("/home", methods=["POST", "GET"])
def home():
    if  request.method == 'POST':
        user = request.form["inputUsername"]
        password = request.form["inputPassword"]
        return redirect(url_for("account", usr=user))
    else:
        return render_template('designApp.html')


@app.route("/create-account", methods=["POST", "GET"])
def newaccount():
    if request.method == 'POST':
        user = request.form["inputUsername"]
        return redirect(url_for("account", usr=user))  # go to user's account page
    else:
        return render_template('designNew.html')


@app.route("/account/<usr>")
def account(usr):
    return render_template('designAcc.html', usr=usr)


@app.route("/verifyAccount/<username>/<password>")
def verifyAccount(username, password):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT * FROM ACCOUNT WHERE username = %s AND password = %s", username, password
        cursor.execute(query)
        canLogin = cursor.fetchone()
        checkRow = canLogin.rowCount
        if checkRow is None:
            return redirect(url_for("home"))
        else:
            return redirect(url_for("account", usr=username))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

#  if request.method == 'GET':
#       hasAccount = redirect(url_for("verifyAccount", username=user, password=password))
#  if hasAccount is True:
#     return redirect(url_for("account", usr=user))
# redirect(url_for("verifyAccount", username=user, password=password))

if __name__ == "__main__":
    app.run()
