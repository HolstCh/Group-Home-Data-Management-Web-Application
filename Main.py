from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from DatabaseConfig import mysql
from App import app


# redirect directs to different page based on url_for

@app.route("/")
def main():
    return redirect(url_for("home"))


@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        user = request.form["inputUsername"]
        password = request.form["inputPassword"]
        return redirect(url_for("verifyAccount", username=user, password=password))
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


@app.route("/verifyAccount/<username>/<password>", methods=['POST'])
def verifyAccount(username, password):
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "SELECT * FROM ACCOUNT WHERE username = %s AND password = %s"
    info = (username, password)
    cursor.execute(query, info)
    canLogin = cursor.fetchone()
    if not canLogin:
        print('Error: no account')
        return redirect(url_for("home"))
    else:
        return redirect(url_for("account", usr=username))


#  if request.method == 'GET':
#       hasAccount = redirect(url_for("verifyAccount", username=user, password=password))
#  if hasAccount is True:
#     return redirect(url_for("account", usr=user))
# redirect(url_for("verifyAccount", username=user, password=password))

if __name__ == "__main__":
    app.run()
