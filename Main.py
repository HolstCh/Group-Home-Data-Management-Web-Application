from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from DatabaseConfig import mysql
import requests
import json
from App import app
import datetime

BASE = "http://127.0.0.1:5000/"  # base URL for directing to different pages within our app

allPhysicalCodes = {}  # user's share codes is saved globally and are available to them when logging in
allLogCodes = {}
allMentalCodes = {}

userSIN = 0  # user's sin is saved globally when logging in
userName = ""
userProfession = ""


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
        password = request.form["inputPassword"]
        profession = request.form["inputProfession"]
        return redirect(url_for("moreNewAccount", user=user, password=password, profession=profession))  # go to user's account page
    else:
        return render_template('designNew.html')


@app.route("/moreNewAccount/<user>/<password>/<profession>", methods=["POST", "GET"])
def moreNewAccount(user, password, profession):
    if request.method == 'POST':
        # values to insert into Professional (sin as well):
        city = request.form["city"]
        fName = request.form["fName"]
        midInitial = request.form["mid"]
        lastName = request.form["lName"]
        phoneNum = request.form["phone"]

        # values to insert into Account (user & password as well):
        professionType = profession

        # values to insert into Has (user as well):
        sin = request.form["sin"]

        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "INSERT INTO PROFESSIONAL" \
                    " (SIN, city, firstName, middleInitial, lastName, phoneNumber)" \
                    "VALUES(%s, %s, %s, %s, %s, %s)"
            values = (sin, city, fName, midInitial, lastName, phoneNum)
            cursor.execute(query, values)
            connection.commit()

            query = "INSERT INTO ACCOUNT" \
                    " (username, password, professionName)" \
                    "VALUES(%s, %s, %s)"
            values = (user, password, professionType)
            cursor.execute(query, values)
            connection.commit()

            query = "INSERT INTO HAS" \
                    " (SIN, username)" \
                    "VALUES(%s, %s)"
            values = (sin, user)
            cursor.execute(query, values)
            connection.commit()

            print(cursor.rowcount, "record inserted.")
            result = jsonify("New Account Created")
            result.status_code = 200
            return redirect(url_for("home"))  # go back to login page
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    else:
        return render_template('moreDesignNew.html', user=user)


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
    global allPhysicalCodes
    allPhysicalCodes = json.loads(codes.text)
    print(allPhysicalCodes)
    print(type(allPhysicalCodes))
    return redirect(url_for("loadLogCodes", SIN=SIN, username=username, profession=profession))


@app.route("/loadLogCodes/<SIN>/<username>/<profession>")  # load user log codes into local array
def loadLogCodes(SIN, username, profession):
    codes = requests.get("http://127.0.0.1:5000/logCodes/" + SIN)
    global allLogCodes
    allLogCodes = json.loads(codes.text)
    print(allLogCodes)
    return redirect(url_for("loadMentalCodes", SIN=SIN, username=username, profession=profession))


@app.route(
    "/loadMentalCodes/<SIN>/<username>/<profession>")  # load user mental codes into local array and then directs to professional specific page
def loadMentalCodes(SIN, username, profession):
    codes = requests.get("http://127.0.0.1:5000/mentalCodes/" + SIN)
    global allMentalCodes
    allMentalCodes = json.loads(codes.text)
    print(allMentalCodes)
    if profession == 'Youth Worker':
        return redirect(url_for("accountYouth", usr=username, profession=profession))
    elif profession == 'Psychologist':
        return redirect(url_for("accountPsy", usr=username, profession=profession))
    elif profession == 'Pediatrician':
        return redirect(url_for("accountPed", usr=username, profession=profession))


@app.route("/verifyAccount/<username>/<password>/<profession>", methods=['GET'])  # verifies user and then loads their share codes into a local array
def verifyAccount(username, password, profession):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT SIN FROM ACCOUNT as A, HAS as H WHERE A.username = %s AND A.password = %s" \
                " AND A.professionName = %s AND A.username = H.username"
        info = (username, password, profession)
        cursor.execute(query, info)
        sin = cursor.fetchone()
        global userSIN
        userSIN = sin[0]  # save user's SIN
        global userName
        userName = username
        global userProfession
        userProfession = profession
        print(userSIN)
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


@app.route("/getLog/<logShareCode>", methods=['GET'])  # get JSON object of a log book document using share code
def getLog(logShareCode):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = " SELECT day, month, year, event, behaviour, actionsTaken, YSIN, youthName FROM LOG_CODES as L1, LOG_BOOK as L2" \
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
        query = " SELECT day, month, year, weight, height, temperature, heartRate, bloodPressure, respiratoryRate, pedSIN, youthName, name, dosage, dosesPerDay, illness" \
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


def generateShareCode():  # counts all rows for all three documents and adds one so the next "upload" has a unique share code
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT (SELECT COUNT(*) FROM PHYSICAL_HEALTH_EVALUATION) +" \
                "(SELECT COUNT(*) FROM MENTAL_HEALTH_EVALUATION) +" \
                "(SELECT COUNT(*) FROM LOG_BOOK) as totalCount"
        cursor.execute(query)
        nextShareCode = cursor.fetchone()[0]
        nextShareCode = nextShareCode + 1
        print(nextShareCode)
        return nextShareCode
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


@app.route("/uploadPsy", methods=['POST', 'GET'])
def uploadPsy():
    date = datetime.datetime.now()
    displayDate = date.date()
    code = generateShareCode()
    if request.method == 'POST':
        # values to insert into MHE table(code included):
        psySIN = userSIN
        youthName = request.form["inputName"]

        # values to insert into Therapy table:
        sessionID = code
        illness = request.form["inputIllness"]
        sessLength = request.form["inputLength"]
        day = date.day
        month = date.month
        year = date.year
        time = request.form["inputTime"]
        therapyMethod = request.form["inputMethod"]

        # values to insert into Symptoms table:
        symptom = request.form["inputSymptom"]
        severity = request.form["inputSeverity"]

        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "INSERT INTO MENTAL_HEALTH_EVALUATION" \
                    " (mentalShareCode, psySIN, youthName)" \
                    "VALUES(%s, %s, %s)"
            values = (code, psySIN, youthName)
            cursor.execute(query, values)
            connection.commit()

            query = "INSERT INTO THERAPY" \
                    " (sessionID, illness, sessionLength, day, month, year, time, therapeuticMethod, mentalShareCode)" \
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (sessionID, illness, sessLength, day, month, year, time, therapyMethod, code)
            cursor.execute(query, values)
            connection.commit()

            query = "INSERT INTO SYMPTOMS" \
                    " (mentalShareCode, symptom, severity)" \
                    "VALUES(%s, %s, %s)"
            values = (code, symptom, severity)
            cursor.execute(query, values)
            connection.commit()

            print(cursor.rowcount, "record inserted.")
            result = jsonify("MHE Created")
            result.status_code = 200
            return redirect(url_for("accountPsy", usr=userName, profession=userProfession))  # back to Psy's main page
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    else:
        return render_template('uploadPsy.html', date=displayDate, SC=code)


@app.route("/uploadYouth")
def uploadYouth():
    return render_template('uploadYouth.html')


if __name__ == "__main__":
    app.run(debug=True)