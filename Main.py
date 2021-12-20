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


@app.route("/newAccount", methods=["POST", "GET"])
def newAccount():
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
    codes = requests.get("http://127.0.0.1:5000/physicalCodes/" + SIN)
    allPhysicalCodes = json.loads(codes.text)
    print(allPhysicalCodes)
    print(type(allPhysicalCodes))
    return redirect(url_for("loadLogCodes", SIN=SIN, username=username, profession=profession))


@app.route("/loadLogCodes/<SIN>/<username>/<profession>")  # load user log codes into local array
def loadLogCodes(SIN, username, profession):
    codes = requests.get("http://127.0.0.1:5000/logCodes/" + SIN)
    allLogCodes = json.loads(codes.text)
    print(allLogCodes)
    return redirect(url_for("loadMentalCodes", SIN=SIN, username=username, profession=profession))


@app.route(
    "/loadMentalCodes/<SIN>/<username>/<profession>")  # load user mental codes into local array and then directs to professional specific page
def loadMentalCodes(SIN, username, profession):
    codes = requests.get("http://127.0.0.1:5000/mentalCodes/" + SIN)
    allMentalCodes = json.loads(codes.text)
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
    try:
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
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


@app.route("/verifyProfession/<username>/<password>",
           methods=['GET'])  # calls verifyAccount() to direct to the professional's page
def verifyProfession(username, password):
    try:
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
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


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


@app.route("/createAccount", methods=['POST', 'GET'])  # work in progress
def createAccount():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        _professionName = _json['professionName']
        if _username and _password and _professionName and request.method == 'POST':
            query = "INSERT INTO ACCOUNT(username, password, professionName)"
            data = (_username, _password, _professionName)
            cursor.execute(query, data)
            cursor.commit()
            result = jsonify("Professional Created")
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
        query = " SELECT day, month, year, event, behaviour, actionsTaken, YSIN FROM LOG_CODES as L1, LOG_BOOK as L2" \
                " WHERE L2.logShareCode = %s and L1.logCode = L2.logShareCode"
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


@app.route("/getMHE/<mentalShareCode>", methods=['GET'])  # get JSON object of a log book document using share code
def getMHE(mentalShareCode):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT * FROM MENTAL_CODES as P1, MENTAL_HEALTH_EVALUATION as P2, THERAPY as P3, SYMPTOMS as P4" \
                "WHERE P1.mentalCode = P2.mentalShareCode and P2.mentalShareCode = P3.mentalShareCode " \
                "and P2.mentalShareCode = P4.mentalShareCode and P1.mentalCode = %s"
        info = mentalShareCode
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


@app.route("/getPHE/<physicalShareCode>", methods=['GET'])  # get JSON object of a log book document using share code
def getPHE(physicalShareCode):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = " SELECT day, month, year, weight, height, temperature, heartRate, bloodPressure, respiratoryRate, pedSIN, name, dosage, dosesPerDay, illness" \
                " FROM PHYSICAL_CODES as P1, PHYSICAL_HEALTH_EVALUATION as P2, PRESCRIPTION as P3" \
                " WHERE P1.physicalCode = P2.physicalShareCode and P2.physicalShareCode = P3.physicalShareCode and P1.physicalCode = %s"
        info = physicalShareCode
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


@app.route("/upload/Youth", methods=["POST", "GET"])
def uploadYouth():
    if request.method == 'POST':
        return redirect(url_for('accountYouth'))
    else:
        return render_template('uploadYouth.html')

@app.route("/upload/Pediatrician", methods=["POST", "GET"])
def uploadPediatrician():
    if request.method == 'POST':
        pedSin = request.form["inputPed"]
        youthName = request.form["inputName"]
        weight = request.form["inputWeight"]
        height = request.form["inputHeight"]
        temperature = request.form["inputTemp"]
        heartrate = request.form["inputHR"]
        bloodpr = request.form["inputBP"]
        respiratory = request.form["inputRR"]
        presname = request.form["inputPres"]
        dosage = request.form["inputDosage"]
        dpd = request.form["inputDPD"]
        illness = request.form["inputIllness"]
        return redirect(url_for('accountPed'))
    else:
        return render_template('uploadPed.html', SC = "share code", date = "date")


if __name__ == "__main__":
    app.run(debug=True)
