import requests
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
        return redirect(url_for("verifyProfession", username=user, password=password))
    else:
        return render_template('designApp.html')


@app.route("/create-account", methods=["POST", "GET"])
def newaccount():
    if request.method == 'POST':
        user = request.form["inputUsername"]
        return redirect(url_for("account", usr=user))  # go to user's account page
    else:
        return render_template('designNew.html')


@app.route("/accountYouth/<usr>/<profession>")
def accountYouth(usr, profession):
    return render_template('designAccYouth.html', usr=usr, profession=profession)


@app.route("/accountPed/<usr>/<profession>")
def accountPed(usr, profession):
    return render_template('designAccPed.html', usr=usr, profession=profession)


@app.route("/accountPsy/<usr>/<profession>")
def accountPsy(usr, profession):
    return render_template('designAccPsy.html', usr=usr, profession=profession)


@app.route("/verifyAccount/<username>/<password>/<profession>", methods=['GET']) # verifies user and directs them to their professional page
def verifyAccount(username, password, profession):
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "SELECT * FROM ACCOUNT WHERE username = %s AND password = %s AND professionName = %s"
    info = (username, password, profession)
    cursor.execute(query, info)
    canLogin = cursor.fetchone()
    if not canLogin:
        print('Error: no account')
        return redirect(url_for("home"))
    elif profession == 'Youth Worker':
        return redirect(url_for("accountYouth", usr=username, profession=profession))
    elif profession == 'Psychologist':
        return redirect(url_for("accountPsy", usr=username, profession=profession))
    elif profession == 'Pediatrician':
        return redirect(url_for("accountPed", usr=username, profession=profession))


@app.route("/verifyProfession/<username>/<password>", methods=['GET'])  # calls verifyAccount() to direct to the professional's page
def verifyProfession(username, password):
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "SELECT professionName FROM ACCOUNT WHERE username = %s AND password = %s"
    info = (username, password)
    cursor.execute(query, info)
    profType = cursor.fetchone()
    if not profType:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("verifyAccount", username=username, password=password, profession=profType))


@app.route("/getLog", methods=['GET'])
def log(logShareCode):
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "SELECT * FROM LOG_BOOK WHERE logShareCode = %i"
    info = logShareCode
    canView = cursor.fetchone()
    if not canView:
        print('Error: no log book found')
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
