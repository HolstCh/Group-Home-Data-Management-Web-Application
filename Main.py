from collections import OrderedDict
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
from DatabaseConfig import mysql
import requests
import json
from App import app  # Flask app object that runs this application
from API import api  # required to access the API endpoints
import datetime  # automatically input date & time when uploading a document
import easygui  # GUI notification system
from requests import get, post

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
    return redirect(url_for("home", message=" "))


@app.route("/home/<message>", methods=["POST", "GET"])  # login URL page
def home(message):
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
        return render_template('designApp.html', message=message)


@app.route("/accountYouth")  # user Youth Worker's main page
def accountYouth():
    return render_template('designAccYouth.html', usr=userName, profession=userProfession)


@app.route("/accountPed")  # user Pediatrician's main page
def accountPed():
    return render_template('designAccPed.html', usr=userName, profession=userProfession)


@app.route("/accountPsy")  # user Psychologist's main page
def accountPsy():
    return render_template('designAccPsy.html', usr=userName, profession=userProfession)


@app.route("/mainPage")  # deciphers which main page to direct to depending on the profession type (user type)
def mainPage():
    if userProfession == 'Youth Worker':
        return redirect(url_for("accountYouth"))
    elif userProfession == 'Psychologist':
        return redirect(url_for("accountPsy"))
    elif userProfession == 'Pediatrician':
        return redirect(url_for("accountPed"))


@app.route(
    "/loadPhysicalCodes")  # load shared & user physical codes into global list (owned goes in "My Files", shared in "Shared Files")
def loadPhysicalCodes():
    global sharedPhysicalCodes
    allCodes = get(BASE + "AllPhysicalCodes/" + str(userSIN))
    if allCodes.status_code == 200:
        codes = json.loads(allCodes.text)
        for i in codes:
            sharedPhysicalCodes.append(i["physicalCode"])
    elif allCodes.status_code == 404:
        print("Error: codes not found")

    print("Shared Physical Codes: ", sharedPhysicalCodes)

    global ownedPhysicalCodes
    otherCodes = get(BASE + "OwnedPhysicalCodes/" + str(userSIN))
    if otherCodes.status_code == 200:
        ownedCodes = json.loads(otherCodes.text)
        for i in ownedCodes:
            ownedPhysicalCodes.append(i["physicalShareCode"])
    elif otherCodes.status_code == 404:
        print("Error: codes not found")

    for i in ownedPhysicalCodes[:]:
        if i in sharedPhysicalCodes:
            sharedPhysicalCodes.remove(i)

    print("Owned Physical Codes: ", ownedPhysicalCodes)
    print("Shared Physical Codes: ", sharedPhysicalCodes)

    return redirect(url_for("loadLogCodes"))


@app.route("/loadLogCodes")  # load user log codes into global list (owned goes in "My Files", shared in "Shared Files")
def loadLogCodes():
    global sharedLogCodes
    allCodes = get(BASE + "AllLogCodes/" + str(userSIN))
    if allCodes.status_code == 200:
        codes = json.loads(allCodes.text)
        for i in codes:
            sharedLogCodes.append(i["logCode"])
    elif allCodes.status_code == 404:
        print("Error: codes not found")

    print("Shared Log Codes: ", sharedLogCodes)

    global ownedLogCodes
    otherCodes = get(BASE + "OwnedLogCodes/" + str(userSIN))
    if otherCodes.status_code == 200:
        ownedCodes = json.loads(otherCodes.text)
        for i in ownedCodes:
            ownedLogCodes.append(i["logShareCode"])
    elif otherCodes.status_code == 404:
        print("Error: codes not found")

    for i in ownedLogCodes[:]:
        if i in sharedLogCodes:
            sharedLogCodes.remove(i)

    print("Owned Log Codes: ", ownedLogCodes)
    print("Shared Log Codes: ", sharedLogCodes)

    return redirect(url_for("loadMentalCodes"))


@app.route(
    "/loadMentalCodes")  # load user mental codes into global list (owned goes in "My Files", shared in "Shared Files")
def loadMentalCodes():
    global sharedMentalCodes
    allCodes = get(BASE + "AllMentalCodes/" + str(userSIN))
    if allCodes.status_code == 200:
        codes = json.loads(allCodes.text)
        for i in codes:
            sharedMentalCodes.append(i["mentalCode"])
    elif allCodes.status_code == 404:
        print("Error: codes not found")

    print("Shared Mental Codes: ", sharedMentalCodes)

    global ownedMentalCodes
    otherCodes = get(BASE + "OwnedMentalCodes/" + str(userSIN))
    if otherCodes.status_code == 200:
        ownedCodes = json.loads(otherCodes.text)
        for i in ownedCodes:
            ownedMentalCodes.append(i["mentalShareCode"])
    elif otherCodes.status_code == 404:
        print("Error: codes not found")

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
        print(profession)
        print(userSIN)
        print(userProfession)
        if not sin:
            print('Error: no account')
            return redirect(url_for("home", message="Username or password is incorrect!"))
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
            return redirect(url_for("home", message="Username or password is incorrect!"))
        else:
            return redirect(url_for("verifyAccount", username=username, password=password, profession=profType[0]))
    except Exception as e:
        print(e)
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

        data = {"day": day, "month": month, "year": year, "weight": weight, "height": height,
                "temperature": temperature,
                "heartRate": heartRate, "bloodPressure": bloodPressure, "respiratoryRate": respiratoryRate,
                "pedSIN": pedSIN,
                "youthName": youthName, "name": drugName, "dosage": dosage, "dosesPerDay": dosesPerDay,
                "illness": illness}

        upload = post(BASE + "PHE/" + str(code), data=data)
        if upload.status_code == 200:
            easygui.msgbox(userName + ', your physical health evaluation was uploaded successfully.', 'Success!')
            ownedPhysicalCodes.append(code)
            post(BASE + "SendPedCode/" + str(userName) + "/" + str(code))
            return redirect(url_for("accountPed"))
        elif upload.status_code == 400:
            easygui.msgbox(userName + ', your physical health evaluation upload has failed', 'Error!')
            return render_template('uploadPed.html', date=displayDate, SC=code)
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
        symptom2 = request.form["inputSymptom2"]
        severity2 = request.form["inputSeverity2"]
        symptom3 = request.form["inputSymptom3"]
        severity3 = request.form["inputSeverity3"]
        symptom4 = request.form["inputSymptom4"]
        severity4 = request.form["inputSeverity4"]
        symptom5 = request.form["inputSymptom5"]
        severity5 = request.form["inputSeverity5"]
        symptom6 = request.form["inputSymptom6"]
        severity6 = request.form["inputSeverity6"]
        symptom7 = request.form["inputSymptom7"]
        severity7 = request.form["inputSeverity7"]
        symptom8 = request.form["inputSymptom8"]
        severity8 = request.form["inputSeverity8"]
        symptom9 = request.form["inputSymptom9"]
        severity9 = request.form["inputSeverity9"]
        symptom10 = request.form["inputSymptom10"]
        severity10 = request.form["inputSeverity10"]

        data = {"psySIN": psySIN, "youthName": youthName, "sessionID": sessionID, "illness": illness,
                "sessionLength": sessLength, "day": day,
                "month": month, "year": year, "time": time, "therapeuticMethod": therapyMethod, "symptom": symptom,
                "severity": severity,
                "symptom2": symptom2, "severity2": severity2, "symptom3": symptom3, "severity3": severity3,
                "symptom4": symptom4, "severity4": severity4, "symptom5": symptom5, "severity5": severity5,
                "symptom6": symptom6, "severity6": severity6, "symptom7": symptom7, "severity7": severity7,
                "symptom8": symptom8, "severity8": severity8, "symptom9": symptom9, "severity9": severity9,
                "symptom10": symptom10, "severity10": severity10}

        upload = post(BASE + "MHE/" + str(code), data=data)
        if upload.status_code == 200:
            easygui.msgbox(userName + ', your mental health evaluation was uploaded successfully.', 'Success!')
            ownedMentalCodes.append(code)
            post(BASE + "SendPsyCode/" + str(userName) + "/" + str(code))
            return redirect(url_for("accountPsy"))  # back to Psy's main page
        elif upload.status_code == 400:
            easygui.msgbox(userName + ', your mental health evaluation upload has failed.', 'Error!')
            return render_template('uploadPsy.html', date=displayDate, SC=code)

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

        data = {'logShareCode': code, 'day': day, 'month': month, 'year': year, 'event': event, 'behaviour': behaviour,
                'actionsTaken': actions, 'YSIN': youthSIN, 'youthName': youthName}

        upload = post(BASE + "Log/" + str(code), data=data)
        if upload.status_code == 200:
            easygui.msgbox(userName + ', your log book entry was uploaded successfully.', 'Success!')
            ownedLogCodes.append(code)
            post(BASE + "SendLogCode/" + str(userName) + "/" + str(code))
            return redirect(url_for("accountYouth"))  # back to Youth's main page
        elif upload.status_code == 400:
            easygui.msgbox(userName + ', your log book entry upload has failed.', 'Error!')
            return render_template('uploadYouth.html', date=displayDate, SC=code)
    else:
        return render_template('uploadYouth.html', date=displayDate, SC=code)


@app.route("/displayPHE/<physicalShareCode>", methods=['GET'])  # display PHE in HTML table
def displayPHE(physicalShareCode):
    jsonObject = get(BASE + "PHE/" + physicalShareCode)
    data = []
    if jsonObject.status_code == 200:
        rowData = json.loads(jsonObject.text)
        rowData = rowData.values()
        data = list(rowData)
        print(rowData)
        print(type(rowData))
    elif jsonObject.status_code == 404:
        print("PHE was not found")
        easygui.msgbox(userName + ', your log book with a share code of ' + physicalShareCode + ' has not been found.',
                       'Error!')
    return render_template('displayPHE.html', rowData=data)


@app.route("/displayLog/<logShareCode>", methods=['GET'])  # display Log Book in HTML table
def displayLog(logShareCode):
    jsonObject = get(BASE + "Log/" + logShareCode)
    data = []
    if jsonObject.status_code == 200:
        rowData = json.loads(jsonObject.text)
        rowData = rowData.values()
        data = list(rowData)
        print(rowData)
        print(type(rowData))
    elif jsonObject.status_code == 404:
        easygui.msgbox(userName + ', your log book with a share code of ' + logShareCode + ' has not been found.',
                       'Error!')
        print("PHE was not found")
    return render_template('displayLog.html', rowData=data)


@app.route("/displayMHE/<mentalShareCode>", methods=['GET'])  # display MHE in HTML table
def displayMHE(mentalShareCode):
    jsonObject = get(BASE + "MHE/" + mentalShareCode)
    data = []
    if jsonObject.status_code == 200:
        rowData = json.loads(jsonObject.text)
        rowData = rowData.values()
        data = list(rowData)
        print(rowData)
        print(type(rowData))
    if jsonObject.status_code == 404:
        easygui.msgbox(
            userName + ', your Mental Health Evaluation with a share code of ' + mentalShareCode + ' has not been found.',
            'Error!')
        print("MHE was not found")
    return render_template('displayMHE.html', rowData=data)


@app.route("/displayClient/<name>", methods=["GET"])  # first sign up page for new account
def displayClient(name):
    jsonObject = get(BASE + "Client/" + name)
    data = []
    if jsonObject.status_code == 200:
        rowData = json.loads(jsonObject.text)
        rowData = rowData.values()
        data = list(rowData)
        print(rowData)
        print(type(rowData))
    if jsonObject.status_code == 404:
        easygui.msgbox(
            userName + ', the client named ' + name + ' has not been found.', 'Error!')
        print("MHE was not found")
    return render_template('displayClient.html', rowData=data)


@app.route("/displayFamily/<clientID>", methods=["GET"])  # first sign up page for new account
def displayFamily(clientID):
    jsonObject = get(BASE + "Family/" + clientID)
    dataOne = []
    dataTwo = []
    if jsonObject.status_code == 200:
        rowData = json.loads(jsonObject.text)
        rowOne = rowData[0]
        rowTwo = rowData[1]
        rowOne = rowOne.values()
        rowTwo = rowTwo.values()
        dataOne = list(rowOne)
        dataTwo = list(rowTwo)
        print(rowData)
        print(type(rowData))
    if jsonObject.status_code == 404:
        easygui.msgbox(
            userName + ', the family members of have not been found.', 'Error!')
        print("MHE was not found")
    return render_template('displayFamily.html', rowDataOne=dataOne, rowDataTwo=dataTwo)


@app.route("/sharedFiles", methods=['GET'])  # universal shared files page where user's shared files are displayed
def sharedFiles():
    physical = [i for i in sharedPhysicalCodes]
    log = [i for i in sharedLogCodes]
    mental = [i for i in sharedMentalCodes]
    return render_template('sharedFiles.html', sharedPHEs=physical, sharedLogs=log, sharedMHEs=mental)


@app.route("/myFilesPed", methods=['POST', 'GET'])  # Ped's own files where they can view or share to other users
def myFilesPed():
    physical = [i for i in ownedPhysicalCodes]
    render_template('myFilesPed.html', ownedPHEs=physical)
    if request.method == 'POST':
        # values to input into another user's physical codes for them to access if they have an account
        shareCode = request.form["shareYourCode"]
        toUser = request.form["inputUsername"]

        share = post(BASE + "SendPedCode/" + str(toUser) + "/" + str(shareCode))
        if share.status_code == 200:
            easygui.msgbox(
                userName + ', your share code of ' + shareCode + ' was shared to ' + toUser + ' successfully.',
                'Success!')
            return redirect(url_for("accountPed"))  # back to Ped's main page
        elif share.status_code == 400:
            easygui.msgbox(
                userName + ', your share code of ' + shareCode + ' has already been shared to ' + toUser + ' so the share has failed.',
                'Error!')
            physical = [i for i in ownedPhysicalCodes]
            return render_template('myFilesPed.html', ownedPHEs=physical)
    else:
        physical = [i for i in ownedPhysicalCodes]
        return render_template('myFilesPed.html', ownedPHEs=physical)


@app.route("/myFilesYouth", methods=['POST', 'GET'])  # Youth's own files where they can view or share to other users
def myFilesYouth():
    log = [i for i in ownedLogCodes]
    render_template('myFilesYouth.html', ownedLogs=log)
    if request.method == 'POST':
        # values to input into another user's log codes for them to access if they have an account
        shareCode = request.form["shareYourCode"]
        toUser = request.form["inputUsername"]

        share = post(BASE + "SendLogCode/" + str(toUser) + "/" + str(shareCode))
        if share.status_code == 200:
            easygui.msgbox(
                userName + ', your share code of ' + shareCode + ' was shared to ' + toUser + ' successfully.',
                'Success!')
            return redirect(url_for("accountYouth"))  # back to Youth's main page
        elif share.status_code == 400:
            easygui.msgbox(
                userName + ', your share code of ' + shareCode + ' has already been shared to ' + toUser + ' so the share has failed.',
                'Error!')
            log = [i for i in ownedLogCodes]
            return render_template('myFilesYouth.html', ownedLogs=log)
    else:
        log = [i for i in ownedLogCodes]
        return render_template('myFilesYouth.html', ownedLogs=log)


@app.route("/myFilesPsy", methods=['POST', 'GET'])  # Psy's own files where they can view or share to other users
def myFilesPsy():
    mental = [i for i in ownedMentalCodes]
    render_template('myFilesPsy.html', ownedMHEs=mental)
    if request.method == 'POST':
        # values to input into another user's mental codes for them to access if they have an account
        shareCode = request.form["shareYourCode"]
        toUser = request.form["inputUsername"]

        share = post(BASE + "SendPsyCode/" + str(toUser) + "/" + str(shareCode))
        if share.status_code == 200:
            easygui.msgbox(
                userName + ', your share code of ' + shareCode + ' was shared to ' + toUser + ' successfully.',
                'Success!')
            return redirect(url_for("accountPsy"))  # back to Youth's main page
        elif share.status_code == 400:
            easygui.msgbox(
                userName + ', your share code of ' + shareCode + ' was already shared to ' + toUser + ' so the share has failed.',
                'Error!')
            mental = [i for i in ownedMentalCodes]
            return render_template('myFilesPsy.html', ownedMHEs=mental)
    else:
        mental = [i for i in ownedMentalCodes]
        return render_template('myFilesPsy.html', ownedMHEs=mental)


@app.route("/newAccount", methods=["POST", "GET"])  # first sign up page for new account
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
def moreNewAccount(user, password,
                   profession):  # second sign up page for new account: inserts into Professional, Has, and Account tables
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

        data = {"SIN": sin, "city": city, "firstName": fName, "middleInitial": midInitial, "lastName": lastName,
                "phoneNumber": phoneNum}
        newUser = post(BASE + "Professional", data=data)
        if newUser.status_code == 400:
            easygui.msgbox(user + ', the ' + professionType + ' account with the SIN of ' + sin + ' already exists',
                           'Error!')
            return render_template('moreDesignNew.html', user=user)
        elif newUser.status_code == 200:
            try:
                connection = mysql.connect()
                cursor = connection.cursor()
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

                if professionType == "Youth Worker":
                    post(BASE + "Youth/" + sin)
                elif professionType == "Pediatrician":
                    post(BASE + "Ped/" + sin)
                elif professionType == "Psychologist":
                    post(BASE + "Psy/" + sin)

                print(cursor.rowcount, "record inserted.")
                easygui.msgbox(user + ', your new ' + professionType + ' account was created successfully.', 'Success!')
                result = jsonify("New Account Created")
                result.status_code = 200
                return redirect(url_for("home", message=" "))  # go back to login page
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                connection.close()
    else:
        return render_template('moreDesignNew.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
