from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from DatabaseConfig import mysql
import requests
import json
from App import app
import datetime

BASE = "http://127.0.0.1:5000/"  # base URL for directing to different pages within our app

sharedPhysicalCodes = []  # user's codes that are used to view available documents and are saved globally when logging in
sharedLogCodes = []
sharedMentalCodes = []

ownedPhysicalCodes = []  # one of three will be user's own share codes that load when they login
ownedLogCodes = []
ownedMentalCodes = []

userSIN = 0  # user's sin is saved globally when logging in
userName = ""  # user's username is saved globally when logging in
userProfession = ""  # user's profession is saved globally when logging in


@app.route("/")
def main():
    return redirect(url_for("home"))


@app.route("/home", methods=["POST", "GET"])
def home():
    sharedPhysicalCodes.clear()
    sharedLogCodes.clear()
    sharedMentalCodes.clear()
    ownedPhysicalCodes.clear()
    ownedLogCodes.clear()
    ownedMentalCodes.clear()
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
        return redirect(
            url_for("moreNewAccount", user=user, password=password, profession=profession))  # go to user's account page
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


@app.route("/accountYouth")
def accountYouth():
    return render_template('designAccYouth.html', usr=userName, profession=userProfession)


@app.route("/accountPed")
def accountPed():
    return render_template('designAccPed.html', usr=userName, profession=userProfession)


@app.route("/accountPsy")
def accountPsy():
    return render_template('designAccPsy.html', usr=userName, profession=userProfession)


@app.route("/mainPage")
def mainPage():
    if userProfession == 'Youth Worker':
        return redirect(url_for("accountYouth"))
    elif userProfession == 'Psychologist':
        return redirect(url_for("accountPsy"))
    elif userProfession == 'Pediatrician':
        return redirect(url_for("accountPed"))


@app.route("/loadPhysicalCodes")  # load shared & user physical codes into local array
def loadPhysicalCodes():
    allCodes = requests.get(BASE + "getAllPhysicalCodes/" + str(userSIN))
    global sharedPhysicalCodes
    sharedPhysicalCodes = json.loads(allCodes.text)
    print("Shared Physical Codes: ", sharedPhysicalCodes)
    ownedCodes = requests.get(BASE + "getOwnedPhysicalCodes/" + str(userSIN))
    global ownedPhysicalCodes
    ownedPhysicalCodes = json.loads(ownedCodes.text)
    for i in ownedPhysicalCodes[:]:
        if i in sharedPhysicalCodes:
            sharedPhysicalCodes.remove(i)

    print("Owned Physical Codes: ", ownedPhysicalCodes)
    print("Shared Physical Codes: ", sharedPhysicalCodes)

    return redirect(url_for("loadLogCodes"))


@app.route("/loadLogCodes")  # load user log codes into local array
def loadLogCodes():
    allCodes = requests.get(BASE + "getAllLogCodes/" + str(userSIN))
    global sharedLogCodes
    sharedLogCodes = json.loads(allCodes.text)
    print("Shared Log Codes: ", sharedLogCodes)
    ownedCodes = requests.get(BASE + "getOwnedLogCodes/" + str(userSIN))
    global ownedLogCodes
    ownedLogCodes = json.loads(ownedCodes.text)
    for i in ownedLogCodes[:]:
        if i in sharedLogCodes:
            sharedLogCodes.remove(i)

    print("Owned Log Codes: ", ownedLogCodes)
    print("Shared Log Codes: ", sharedLogCodes)

    return redirect(url_for("loadMentalCodes"))


@app.route(
    "/loadMentalCodes")  # load user mental codes into local array and then directs to professional specific main page
def loadMentalCodes():
    allCodes = requests.get(BASE + "getAllMentalCodes/" + str(userSIN))
    global sharedMentalCodes
    sharedMentalCodes = json.loads(allCodes.text)
    print("Shared Mental Codes: ", sharedMentalCodes)
    ownedCodes = requests.get(BASE + "getOwnedMentalCodes/" + str(userSIN))
    global ownedMentalCodes
    ownedMentalCodes = json.loads(ownedCodes.text)
    for i in ownedMentalCodes[:]:
        if i in sharedMentalCodes:
            sharedMentalCodes.remove(i)

    print("Owned Mental Codes: ", ownedMentalCodes)
    print("Shared Mental Codes: ", sharedMentalCodes)

    return redirect(url_for("mainPage"))  # function to direct professional user to their own main page


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

        global userSIN
        userSIN = sin[0]  # save user's SIN
        global userName
        userName = username  # save user's username
        global userProfession
        userProfession = profession  # save user's Profession Type
        print(userSIN)
        if not sin:
            print('Error: no account')
            return redirect(url_for("home"))
        else:
            return redirect(url_for("loadPhysicalCodes"))
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


@app.route("/getAllLogCodes/<SIN>", methods=['GET'])
def getAllLogCodes(SIN):
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


@app.route("/getAllMentalCodes/<SIN>", methods=['GET'])
def getAllMentalCodes(SIN):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT mentalCode FROM MENTAL_CODES WHERE SIN = %s"
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


@app.route("/getAllPhysicalCodes/<SIN>", methods=['GET'])
def getAllPhysicalCodes(SIN):
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
        query = " SELECT youthName, day, month, year, event, behaviour, actionsTaken, YSIN FROM LOG_CODES as L1, LOG_BOOK as L2" \
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
        query = "SELECT youthName, day, month, year, time, sessionID, illness, sessionLength, therapeuticMethod, symptom, severity, psySIN" \
                " FROM MENTAL_CODES as P1, MENTAL_HEALTH_EVALUATION as P2, THERAPY as P3, SYMPTOMS as P4" \
                " WHERE P1.mentalCode = P2.mentalShareCode and P2.mentalShareCode = P3.mentalShareCode " \
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
        query = " SELECT youthName, day, month, year, weight, height, temperature, heartRate, bloodPressure, respiratoryRate, name, dosage, dosesPerDay, illness, pedSIN" \
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
        print('Error: no PHE found')
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


@app.route("/uploadPed", methods=['POST', 'GET'])  # upload button for Ped which allows uploading PHEs
def uploadPed():
    date = datetime.datetime.now()
    displayDate = date.date()
    code = generateShareCode()
    if request.method == 'POST':
        # values to insert into PHE table:
        pedSIN = userSIN
        day = date.day
        month = date.month
        year = date.year
        weight = request.form["inputWeight"]
        height = request.form["inputHeight"]
        temperature = request.form["inputTemp"]
        heartRate = request.form["inputHR"]
        bloodPressure = request.form["inputBP"]
        respiratoryRate = request.form["inputRR"]
        youthName = request.form["inputName"]

        # values to insert into Prescription table:
        drugName = request.form["inputPres"]
        dosage = request.form["inputDosage"]
        dosesPerDay = request.form["inputDPD"]
        illness = request.form["inputIllness"]
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "INSERT INTO PHYSICAL_HEALTH_EVALUATION" \
                    " (physicalShareCode, day, month, year, weight, height, temperature, heartRate, bloodPressure, respiratoryRate, pedSIN, youthName)" \
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (
                code, day, month, year, weight, height, temperature, heartRate, bloodPressure, respiratoryRate, pedSIN,
                youthName)
            cursor.execute(query, values)
            connection.commit()

            query = "INSERT INTO PRESCRIPTION" \
                    " (name, dosage, dosesPerDay, illness, physicalShareCode)" \
                    "VALUES(%s, %s, %s, %s, %s)"
            values = (drugName, dosage, dosesPerDay, illness, code)
            cursor.execute(query, values)
            connection.commit()

            print(cursor.rowcount, "record inserted.")
            result = jsonify("PHE Created")
            result.status_code = 200
            return redirect(url_for("accountPed"))
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    else:
        return render_template('uploadPed.html', date=displayDate, SC=code)


@app.route("/uploadPsy", methods=['POST', 'GET'])  # upload button for Psy which allows uploading MHEs
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
            return redirect(url_for("accountPsy"))  # back to Psy's main page
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    else:
        return render_template('uploadPsy.html', date=displayDate, SC=code)


@app.route("/uploadYouth", methods=['POST', 'GET'])  # upload button for Youth Worker which allows uploading Log Books
def uploadYouth():
    date = datetime.datetime.now()
    displayDate = date.date()
    code = generateShareCode()
    if request.method == 'POST':
        # values to insert into Log Book
        youthName = request.form["inputName"]
        day = date.day
        month = date.month
        year = date.year
        behaviour = request.form["inputBehaviour"]
        event = request.form["inputEvent"]
        actions = request.form["inputActions"]
        youthSIN = userSIN

        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "INSERT INTO LOG_BOOK" \
                    " (logShareCode, day, month, year, event, behaviour, actionsTaken, YSIN, youthName)" \
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (code, day, month, year, event, behaviour, actions, youthSIN, youthName)
            cursor.execute(query, values)
            connection.commit()

            print(cursor.rowcount, "record inserted.")
            result = jsonify("Log Book Created")
            result.status_code = 200
            return redirect(url_for("accountYouth"))  # back to Youth's main page
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    else:
        return render_template('uploadYouth.html', date=displayDate, SC=code)


@app.route("/displayLog/<logShareCode>", methods=['GET'])  # display Log Book in HTML table
def displayLog(logShareCode):
    jsonObject = requests.get(BASE + "getLog/" + logShareCode)
    rowData = json.loads(jsonObject.text)
    print(rowData)
    print(type(rowData))
    return render_template('displayLog.html', rowData=rowData)


@app.route("/displayMHE/<mentalShareCode>", methods=['GET'])  # display MHE in HTML table
def displayMHE(mentalShareCode):
    jsonObject = requests.get(BASE + "getMHE/" + mentalShareCode)
    rowData = json.loads(jsonObject.text)
    print(rowData)
    print(type(rowData))
    return render_template('displayMHE.html', rowData=rowData)


@app.route("/displayPHE/<physicalShareCode>", methods=['GET'])  # display PHE in HTML table
def displayPHE(physicalShareCode):
    jsonObject = requests.get(BASE + "getPHE/" + physicalShareCode)
    rowData = json.loads(jsonObject.text)
    print(rowData)
    print(type(rowData))
    return render_template('displayPHE.html', rowData=rowData)


@app.route("/sharedFiles", methods=['GET'])  # universal shared files page where user's shared files are displayed
def sharedFiles():
    physical = [i[0] for i in sharedPhysicalCodes]
    log = [i[0] for i in sharedLogCodes]
    mental = [i[0] for i in sharedMentalCodes]
    return render_template('sharedFiles.html', sharedPHEs=physical, sharedLogs=log, sharedMHEs=mental)


@app.route("/myFilesPed", methods=['POST', 'GET'])  # Ped's own files where they can view or share to other users
def myFilesPed():
    if request.method == 'POST':
        # values to input into another user's physical codes for them to access if they have an account
        shareCode = request.form["shareYourCode"]
        toUser = request.form["inputUsername"]
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT SIN FROM HAS WHERE username = %s"
            cursor.execute(query, toUser)
            sin = cursor.fetchone()

            query = "INSERT INTO PHYSICAL_CODES (SIN, physicalCode) VALUES(%s, %s)"
            values = (sin, shareCode)
            cursor.execute(query, values)
            connection.commit()
            print(cursor.rowcount, "record inserted.")
            result = jsonify("Physical Code Shared")
            result.status_code = 200
            return redirect(url_for("accountPed"))  # back to Ped's main page
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    else:
        physical = [i[0] for i in ownedPhysicalCodes]
        return render_template('myFilesPed.html', ownedPHEs=physical)


@app.route("/myFilesYouth", methods=['POST', 'GET'])  # Youth's own files where they can view or share to other users
def myFilesYouth():
    if request.method == 'POST':
        # values to input into another user's log codes for them to access if they have an account
        shareCode = request.form["shareYourCode"]
        toUser = request.form["inputUsername"]
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT SIN FROM HAS WHERE username = %s"
            cursor.execute(query, toUser)
            sin = cursor.fetchone()

            query = "INSERT INTO LOG_CODES (SIN, logCode) VALUES(%s, %s)"
            values = (sin, shareCode)
            cursor.execute(query, values)
            connection.commit()
            print(cursor.rowcount, "record inserted.")
            result = jsonify("Log Code Shared")
            result.status_code = 200
            return redirect(url_for("accountYouth"))  # back to Youth's main page
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    else:
        log = [i[0] for i in ownedLogCodes]
        return render_template('myFilesYouth.html', ownedLogs=log)


@app.route("/myFilesPsy", methods=['POST', 'GET'])  # Psy's own files where they can view or share to other users
def myFilesPsy():
    if request.method == 'POST':
        # values to input into another user's mental codes for them to access if they have an account
        shareCode = request.form["shareYourCode"]
        toUser = request.form["inputUsername"]
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT SIN FROM HAS WHERE username = %s"
            cursor.execute(query, toUser)
            sin = cursor.fetchone()

            query = "INSERT INTO MENTAL_CODES (SIN, mentalCode) VALUES(%s, %s)"
            values = (sin, shareCode)
            cursor.execute(query, values)
            connection.commit()
            print(cursor.rowcount, "record inserted.")
            result = jsonify("Mental Code Shared")
            result.status_code = 200
            return redirect(url_for("accountPsy"))  # back to Youth's main page
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    else:
        mental = [i[0] for i in ownedMentalCodes]
        return render_template('myFilesPsy.html', ownedMHEs=mental)


@app.route("/getOwnedPhysicalCodes/<SIN>", methods=['GET'])  # loads Ped's owned codes into global list
def getOwnedPhysicalCodes(SIN):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT physicalShareCode FROM PHYSICAL_HEALTH_EVALUATION WHERE pedSIN = %s"
        sin = SIN
        cursor.execute(query, sin)
        canView = cursor.fetchall()
        result = jsonify(canView)
        result.status_code = 200
        return result
    except Exception as e:
        print(e)
        print('Error: no PHE found')
    finally:
        cursor.close()
        connection.close()


@app.route("/getOwnedLogCodes/<SIN>", methods=['GET'])  # loads Youth Worker's owned codes into global list
def getOwnedLogCodes(SIN):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT logShareCode FROM LOG_BOOK WHERE YSIN = %s"
        sin = SIN
        cursor.execute(query, sin)
        canView = cursor.fetchall()
        result = jsonify(canView)
        result.status_code = 200
        return result
    except Exception as e:
        print(e)
        print('Error: No Log Codes found')
    finally:
        cursor.close()
        connection.close()


@app.route("/getOwnedMentalCodes/<SIN>", methods=['GET'])  # loads Psy's owned codes into global list
def getOwnedMentalCodes(SIN):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = "SELECT mentalShareCode FROM MENTAL_HEALTH_EVALUATION WHERE psySIN = %s"
        sin = SIN
        cursor.execute(query, sin)
        canView = cursor.fetchall()
        result = jsonify(canView)
        result.status_code = 200
        return result
    except Exception as e:
        print(e)
        print('Error: No Mental Codes found')
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)
