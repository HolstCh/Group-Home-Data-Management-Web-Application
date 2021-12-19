import requests
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from DatabaseConfig import mysql
import requests
import json

from App import app

allPhysicalCodes = {}
allLogCodes = {}
allMentalCodes = {}


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


@app.route("/loadPhysicalCodes/<SIN>/<username>/<profession>")  # load user physical codes into local array
def loadPhysicalCodes(SIN, username, profession):
    x = requests.get("http://127.0.0.1:5000/physicalCodes/" + SIN)
    allPhysicalCodes = json.loads(x.text)
    print(allPhysicalCodes)
    return redirect(url_for("loadLogCodes", SIN=SIN, username=username, profession=profession))


@app.route("/loadLogCodes/<SIN>/<username>/<profession>")  # load user log codes into local array
def loadLogCodes(SIN, username, profession):
    x = requests.get("http://127.0.0.1:5000/logCodes/" + SIN)
    allLogCodes = json.loads(x.text)
    print(allLogCodes)
    return redirect(url_for("loadMentalCodes", SIN=SIN, username=username, profession=profession))


@app.route(
    "/loadMentalCodes/<SIN>/<username>/<profession>")  # load user mental codes into local array and then directs to professional specific page
def loadMentalCodes(SIN, username, profession):
    x = requests.get("http://127.0.0.1:5000/mentalCodes/" + SIN)
    allMentalCodes = json.loads(x.text)
    print(allMentalCodes)
    if profession == 'Youth Worker':
        return redirect(url_for("accountYouth", usr=username, profession=profession))
    elif profession == 'Psychologist':
        return redirect(url_for("accountPsy", usr=username, profession=profession))
    elif profession == 'Pediatrician':
        return redirect(url_for("accountPed", usr=username, profession=profession))


@app.route("/verifyAccount/<username>/<password>/<profession>",
           methods=['GET'])  # verifies user and then loads their share codes into a local array
def verifyAccount(username, password, profession):
    connection = mysql.connect()
    cursor = connection.cursor()
    query = "SELECT SIN FROM ACCOUNT as A, HAS as H WHERE A.username = %s AND A.password = %s" \
            " AND A.professionName = %s AND A.username = H.username"
    info = (username, password, profession)
    cursor.execute(query, info)
    sin = cursor.fetchone()
    if not sin:
        print('Error: no account')
        return redirect(url_for("home"))
    else:
        return redirect(url_for("loadPhysicalCodes", SIN=sin, username=username, profession=profession))


@app.route("/verifyProfession/<username>/<password>",
           methods=['GET'])  # calls verifyAccount() to direct to the professional's page
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


@app.route("/logCodes/<SIN>", methods=['GET'])
def logCodes(SIN):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT logCode FROM LOG_CODES WHERE SIN = %s"
        sin = SIN
        cursor.execute(query, sin)
        allCodes = cursor.fetchall()
        result = jsonify(allCodes)
        result.status_code = 200
        return result
    except Exception as e:
        print(e)
        print('Error: no log book found')
    finally:
        cursor.close()
        connection.close()


@app.route("/mentalCodes/<SIN>", methods=['GET'])
def mentalCodes(SIN):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT mentalCode FROM MENTAL_CODES WHERE SIN = %s"
        sin = SIN
        cursor.execute(query, sin)
        allCodes = cursor.fetchone()
        result = jsonify(allCodes)
        result.status_code = 200
        return result
    except Exception as e:
        print(e)
        print('Error: no log book found')
    finally:
        cursor.close()
        connection.close()


@app.route("/physicalCodes/<SIN>", methods=['GET'])
def physicalCodes(SIN):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT physicalCode FROM PHYSICAL_CODES WHERE SIN = %s"
        sin = SIN
        cursor.execute(query, sin)
        allCodes = cursor.fetchall()
        result = jsonify(allCodes)
        result.status_code = 200
        return result
    except Exception as e:
        print(e)
        print('Error: no PHE found')
    finally:
        cursor.close()
        connection.close()


@app.route("/createAccount", methods=['POST', 'GET'])  # not sure
def createAccount():
    try:
        _json = requests.json
        _username = _json['username']
        _password = _json['password']
        _professionName = _json['professionName']

        query = "INSERT INTO ACCOUNT(username,password,professionName)"
        data = (_username, _password, _professionName)
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute(query, data)
        cursor.commit()
        result = jsonify("ProfessionalCreated")
        result.status_code = 200
        return result
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


@app.route("/getLog/<logShareCode>", methods=['GET'])  # get JSON object of a log book document using share code
def getLog(logShareCode):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT * FROM LOG_BOOK WHERE logShareCode = %s"
        info = logShareCode
        cursor.execute(query, info)
        canView = cursor.fetchone()
        result = jsonify(canView)
        result.status_code = 200
        return result
    except Exception as e:
        print(e)
        print('Error: no log book found')
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)
