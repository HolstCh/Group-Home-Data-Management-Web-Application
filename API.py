from flask_restful import Resource, Api, reqparse
from App import app
from DatabaseConfig import mysql
from flask import jsonify
import pymysql
from flask import request
import requests
import json

api = Api(app)


class MHE(Resource):
    def get(self,
            mentalShareCode):  # retrieve MHE data in JSON format to then be deserialized and displayed in HTML table
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT youthName, day, month, year, time, sessionID, illness, sessionLength, therapeuticMethod, symptom," \
                    " severity, symptom2, severity2, symptom3, severity3, symptom4, severity4, symptom5, severity5, symptom6," \
                    " severity6, symptom7, severity7, symptom8, severity8, symptom9, severity9, symptom10, severity10, psySIN" \
                    " FROM MENTAL_CODES as P1, MENTAL_HEALTH_EVALUATION as P2, THERAPY as P3, SYMPTOMS as P4" \
                    " WHERE P1.mentalCode = P2.mentalShareCode and P2.mentalShareCode = P3.mentalShareCode " \
                    " and P2.mentalShareCode = P4.mentalShareCode and P1.mentalCode = %s"
            info = mentalShareCode
            cursor.execute(query, info)
            canView = cursor.fetchone()
            result = jsonify(canView)
            if canView:
                result.status_code = 200
                return result
            else:
                result.status_code = 404
                return result
        except Exception as e:
            print(e)
            print('Error: no log book found')
        finally:
            cursor.close()
            connection.close()

    def post(self,
             mentalShareCode):  # insert into three tables to upload MHE and returns JSON format for confirmation of insert queries
        try:
            code = mentalShareCode
            data = request.values
            psySIN = data['psySIN']
            youthName = data['youthName']
            sessionID = data['sessionID']
            sessLength = data['sessionLength']
            illness = data['illness']
            day = data['day']
            month = data['month']
            year = data['year']
            time = data['time']
            therapyMethod = data['therapeuticMethod']
            symptom = data['symptom']
            severity = data['severity']
            symptom2 = data['symptom2']
            severity2 = data['severity2']
            symptom3 = data['symptom3']
            severity3 = data['severity3']
            symptom4 = data['symptom4']
            severity4 = data['severity4']
            symptom5 = data['symptom5']
            severity5 = data['severity5']
            symptom6 = data['symptom6']
            severity6 = data['severity6']
            symptom7 = data['symptom7']
            severity7 = data['severity7']
            symptom8 = data['symptom8']
            severity8 = data['severity8']
            symptom9 = data['symptom9']
            severity9 = data['severity9']
            symptom10 = data['symptom10']
            severity10 = data['severity10']

            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT mentalShareCode FROM MENTAL_HEALTH_EVALUATION WHERE mentalShareCode = %s"
            cursor.execute(query, code)
            doesExist = cursor.fetchone()
            if doesExist:
                result = jsonify({'status code': 400, 'message': 'Failure: the MHE file already exists'})
                result.status_code = 400
                return result
            else:
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
                        "(mentalShareCode, symptom, severity, symptom2, severity2, symptom3, severity3, symptom4, severity4, " \
                        "symptom5, severity5, symptom6, severity6, symptom7, severity7, symptom8, severity8, " \
                        "symptom9, severity9, symptom10, severity10)" \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (
                    code, symptom, severity, symptom2, severity2, symptom3, severity3, symptom4, severity4, symptom5,
                    severity5,
                    symptom6, severity6, symptom7, severity7, symptom8, severity8, symptom9, severity9, symptom10,
                    severity10)
                cursor.execute(query, values)
                connection.commit()
                result = jsonify(
                    {'status code': 200, 'message': 'Success: MHE was added to MHE, Therapy, and Symptoms tables',
                     "mentalShareCode": code,
                     "psySIN": psySIN, "youthName": youthName, "sessionID": sessionID, "illness": illness,
                     "sessionLength": sessLength, "day": day, "month": month, "year": year, "time": time,
                     "therapeuticMethod": therapyMethod, "symptom": symptom, "severity": severity,
                     "symptom2": symptom2, "severity2": severity2, "symptom3": symptom3, "severity3": severity3,
                     "symptom4": symptom4, "severity4": severity4, "symptom5": symptom5, "severity5": severity5,
                     "symptom6": symptom6, "severity6": severity6, "symptom7": symptom7, "severity7": severity7,
                     "symptom8": symptom8, "severity8": severity8, "symptom9": symptom9, "severity9": severity9,
                     "symptom10": symptom10, "severity10": severity10})
                result.status_code = 200
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(MHE, "/MHE/<mentalShareCode>")


class PHE(Resource):
    def get(self,
            physicalShareCode):  # retrieve PHE data in JSON format to then be deserialized in main.py and displayed in HTML table
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = " SELECT youthName, day, month, year, weight, height, temperature, heartRate, bloodPressure, respiratoryRate, name, dosage, dosesPerDay, illness, pedSIN" \
                    " FROM PHYSICAL_CODES as P1, PHYSICAL_HEALTH_EVALUATION as P2, PRESCRIPTION as P3" \
                    " WHERE P1.physicalCode = P2.physicalShareCode and P2.physicalShareCode = P3.physicalShareCode and P1.physicalCode = %s"
            info = physicalShareCode
            cursor.execute(query, info)
            canView = cursor.fetchone()
            result = jsonify(canView)
            if canView:
                result.status_code = 200
                return result
            else:
                result.status_code = 404
                return result
        except Exception as e:
            print(e)
            print('Error: no PHE found')
        finally:
            cursor.close()
            connection.close()

    def post(self,
             physicalShareCode):  # insert into two tables to upload PHE (no duplicates possible since unique share code)
        try:  # returns JSON format for confirmation of insert queries
            data = request.values
            code = physicalShareCode
            day = data['day']
            month = data['month']
            year = data['year']
            weight = data['weight']
            height = data['height']
            temperature = data['temperature']
            heartRate = data['heartRate']
            bloodPressure = data['bloodPressure']
            respiratoryRate = data['respiratoryRate']
            pedSIN = data['pedSIN']
            youthName = data['youthName']
            drugName = data['name']
            dosage = data['dosage']
            dosesPerDay = data['dosesPerDay']
            illness = data['illness']

            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT physicalShareCode FROM PHYSICAL_HEALTH_EVALUATION WHERE physicalShareCode = %s"
            cursor.execute(query, code)
            doesExist = cursor.fetchone()
            if doesExist:
                result = jsonify({'status code': 400, 'message': 'Failure: the PHE file already exists'})
                result.status_code = 400
                return result
            else:
                query = "INSERT INTO PHYSICAL_HEALTH_EVALUATION" \
                        " (physicalShareCode, day, month, year, weight, height, temperature, heartRate, bloodPressure, respiratoryRate, pedSIN, youthName)" \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (
                    code, day, month, year, weight, height, temperature, heartRate, bloodPressure, respiratoryRate,
                    pedSIN,
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
                result = jsonify(
                    {"status code": 200, "message": "Success: PHE was added to PHE and Prescription tables",
                     "physicalShareCode": code, "day": day, "month": month, "year": year, "weight": weight,
                     "height": height,
                     "temperature": temperature,
                     "heartRate": heartRate, "bloodPressure": bloodPressure,
                     "respiratoryRate": respiratoryRate, "pedSIN": pedSIN,
                     "youthName": youthName, "name": drugName, "dosage": dosage,
                     "dosesPerDay": dosesPerDay, "illness": illness})
                result.status_code = 200
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(PHE, "/PHE/<physicalShareCode>")


class Log(Resource):
    def get(self,
            logShareCode):  # retrieve Log data in JSON format to then be deserialized in main.py and displayed in HTML table
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = " SELECT youthName, day, month, year, event, behaviour, actionsTaken, YSIN FROM LOG_CODES as L1, LOG_BOOK as L2" \
                    " WHERE L2.logShareCode = %s and L1.logCode = L2.logShareCode"
            info = logShareCode
            cursor.execute(query, info)
            canView = cursor.fetchone()
            result = jsonify(canView)
            if canView:
                result.status_code = 200
                return result
            else:
                result.status_code = 404
                return result
        except Exception as e:
            print(e)
            print('Error: no log book found')
        finally:
            cursor.close()
            connection.close()

    def post(self,
             logShareCode):  # insert into one tables to upload Log (no duplicates possible since unique share code)
        try:  # returns JSON format for confirmation of insert queries
            data = request.values
            youthName = data['youthName']
            day = data['day']
            month = data['month']
            year = data['year']
            behaviour = data['behaviour']
            event = data['event']
            actions = data['actionsTaken']
            youthSIN = data['YSIN']
            code = logShareCode

            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT logShareCode FROM LOG_BOOK WHERE logShareCode = %s"
            cursor.execute(query, code)
            doesExist = cursor.fetchone()
            if doesExist:
                result = jsonify({'status code': 400, 'message': 'Failure: the Log Book file already exists'})
                result.status_code = 400
                return result
            else:
                query = "INSERT INTO LOG_BOOK" \
                        " (logShareCode, day, month, year, event, behaviour, actionsTaken, YSIN, youthName)" \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (code, day, month, year, event, behaviour, actions, youthSIN, youthName)
                cursor.execute(query, values)
                connection.commit()
                print(cursor.rowcount, "record inserted.")
                result = jsonify(
                    {'status code': 200, 'message': 'Success: Log Book was added to Log Book table',
                     'logShareCode': code, 'day': day, 'month': month, 'year': year, 'event': event,
                     'behaviour': behaviour,
                     'actionsTaken': actions, 'YSIN': youthSIN, 'youthName': youthName})
                result.status_code = 200
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(Log, "/Log/<logShareCode>")


class AllPhysicalCodes(Resource):
    def get(self,
            SIN):  # retrieve all PHE share codes in JSON format to be deserialized in main.py and stored in global list
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT physicalCode FROM PHYSICAL_CODES WHERE SIN = %s"
            sin = SIN
            cursor.execute(query, sin)
            allCodes = cursor.fetchall()
            result = jsonify(allCodes)
            if allCodes:
                result.status_code = 200
                return result
            else:
                result.status_code = 404
                return result
        except Exception as e:
            print(e)
            print('Error: no PHE found')
        finally:
            cursor.close()
            connection.close()


api.add_resource(AllPhysicalCodes, "/AllPhysicalCodes/<SIN>")


class AllLogCodes(Resource):
    def get(self,
            SIN):  # retrieve all Log share codes in JSON format to be deserialized in main.py and stored in global list
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT logCode FROM LOG_CODES WHERE SIN = %s"
            sin = SIN
            cursor.execute(query, sin)
            allCodes = cursor.fetchall()
            result = jsonify(allCodes)
            if allCodes:
                result.status_code = 200
                return result
            else:
                result.status_code = 404
                return result
        except Exception as e:
            print(e)
            print('Error: no log book found')
        finally:
            cursor.close()
            connection.close()


api.add_resource(AllLogCodes, "/AllLogCodes/<SIN>")


class AllMentalCodes(Resource):
    def get(self,
            SIN):  # retrieve all MHE share codes in JSON format to be deserialized in main.py and stored in global list
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT mentalCode FROM MENTAL_CODES WHERE SIN = %s"
            sin = SIN
            cursor.execute(query, sin)
            allCodes = cursor.fetchall()
            result = jsonify(allCodes)
            if allCodes:
                result.status_code = 200
                return result
            else:
                result.status_code = 404
                return result
        except Exception as e:
            print(e)
            print('Error: no log book found')
        finally:
            cursor.close()
            connection.close()


api.add_resource(AllMentalCodes, "/AllMentalCodes/<SIN>")


class OwnedPhysicalCodes(Resource):
    def get(self,
            SIN):  # retrieve owned PHE share codes in JSON format to be deserialized in main.py and stored in global list
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT physicalShareCode FROM PHYSICAL_HEALTH_EVALUATION WHERE pedSIN = %s"
            sin = SIN
            cursor.execute(query, sin)
            canView = cursor.fetchall()
            result = jsonify(canView)
            if canView:
                result.status_code = 200
                return result
            else:
                result.status_code = 404
                return result
        except Exception as e:
            print(e)
            print('Error: no PHE found')
        finally:
            cursor.close()
            connection.close()


api.add_resource(OwnedPhysicalCodes, "/OwnedPhysicalCodes/<SIN>")


class OwnedLogCodes(Resource):
    def get(self,
            SIN):  # retrieve owned Log share codes in JSON format to be deserialized in main.py and stored in global lists
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT logShareCode FROM LOG_BOOK WHERE YSIN = %s"
            sin = SIN
            cursor.execute(query, sin)
            canView = cursor.fetchall()
            result = jsonify(canView)
            if canView:
                result.status_code = 200
                return result
            else:
                result.status_code = 404
                return result
        except Exception as e:
            print(e)
            print('Error: No Log Codes found')
        finally:
            cursor.close()
            connection.close()


api.add_resource(OwnedLogCodes, "/OwnedLogCodes/<SIN>")


class OwnedMentalCodes(Resource):
    def get(self,
            SIN):  # retrieve all MHE share codes in JSON format to be deserialized in main.py and stored in global lists
        try:
            connection = mysql.connect()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT mentalShareCode FROM MENTAL_HEALTH_EVALUATION WHERE psySIN = %s"
            sin = SIN
            cursor.execute(query, sin)
            canView = cursor.fetchall()
            result = jsonify(canView)
            if canView:
                result.status_code = 200
                return result
            else:
                result.status_code = 404
                return result
        except Exception as e:
            print(e)
            print('Error: No Mental Codes found')
        finally:
            cursor.close()
            connection.close()


api.add_resource(OwnedMentalCodes, "/OwnedMentalCodes/<SIN>")


class SendLogCode(Resource):
    def post(self, toUser, shareCode):  # inserts Log share code to another user's account
        try:  # returns JSON format for confirmation of insert queries
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT SIN FROM HAS WHERE username = %s"
            cursor.execute(query, (toUser,))
            sin = cursor.fetchone()

            query = "SELECT logCode FROM LOG_CODES WHERE SIN = %s and logCode = %s"
            cursor.execute(query, (sin, shareCode))
            doesExist = cursor.fetchone()
            if doesExist:
                result = jsonify(
                    {'status code': 400, 'message': 'Error: your log code was already shared to the other user'})
                result.status_code = 400
                return result
            else:
                query = "INSERT INTO LOG_CODES (SIN, logCode) VALUES(%s, %s)"
                values = (sin, shareCode)
                cursor.execute(query, values)
                connection.commit()
                print(cursor.rowcount, "record inserted.")
                result = jsonify(
                    {'status code': 200, 'message': 'Success: your log code was shared to other user', "SIN": sin,
                     "logCode": shareCode})
                result.status_code = 200
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(SendLogCode, "/SendLogCode/<toUser>/<shareCode>")


class SendPedCode(Resource):
    def post(self, toUser, shareCode):  # inserts PHE share code to another user's account
        try:  # returns JSON format for confirmation of insert queries
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT SIN FROM HAS WHERE username = %s"
            cursor.execute(query, (toUser,))
            sin = cursor.fetchone()

            query = "SELECT physicalCode FROM PHYSICAL_CODES WHERE SIN = %s and physicalCode = %s"
            cursor.execute(query, (sin, shareCode))
            doesExist = cursor.fetchone()
            if doesExist:
                result = jsonify(
                    {'status code': 400, 'message': 'Error: your physical code was already shared to the other user'})
                result.status_code = 400
                return result
            else:
                query = "INSERT INTO PHYSICAL_CODES (SIN, physicalCode) VALUES(%s, %s)"
                values = (sin, shareCode)
                cursor.execute(query, values)
                connection.commit()
                print(cursor.rowcount, "record inserted.")
                result = jsonify({'status code': 200, 'message': 'Success: your physical code was shared', "SIN": sin,
                                  "physicalCode": shareCode})
                result.status_code = 200
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(SendPedCode, "/SendPedCode/<toUser>/<shareCode>")


class SendPsyCode(Resource):
    def post(self, toUser, shareCode):  # inserts MHE share code to another user's account
        try:  # returns JSON format for confirmation of insert queries
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT SIN FROM HAS WHERE username = %s"
            cursor.execute(query, toUser)
            sin = cursor.fetchone()

            query = "SELECT mentalCode FROM MENTAL_CODES WHERE SIN = %s and mentalCode = %s"
            cursor.execute(query, (sin, shareCode))
            doesExist = cursor.fetchone()
            if doesExist:
                result = jsonify(
                    {'status code': 400, 'message': 'Error: your mental code was already shared to the other user'})
                result.status_code = 400
                return result
            else:
                query = "INSERT INTO MENTAL_CODES (SIN, mentalCode) VALUES(%s, %s)"
                values = (sin, shareCode)
                cursor.execute(query, values)
                connection.commit()
                result = jsonify({'status code': 200, 'message': 'Success: your mental code was shared', "SIN": sin,
                                  "mentalCode": shareCode})
                result.status_code = 200
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(SendPsyCode, "/SendPsyCode/<toUser>/<shareCode>")


class Professional(Resource): # checks if account exists. If not, then insert into Professional, Has, and Account tables
    def post(self):
        try:
            data = request.values
            sin = data['SIN']
            city = data['city']
            fName = data['firstName']
            midInitial = data['middleInitial']
            lastName = data['lastName']
            phoneNum = data['phoneNumber']

            connection = mysql.connect()
            cursor = connection.cursor()
            query = "SELECT SIN FROM PROFESSIONAL WHERE SIN = %s"
            cursor.execute(query, (sin,))
            doesExist = cursor.fetchone()
            if doesExist:
                result = jsonify(
                    {'status code': 400, 'message': 'Error: An account already exists with that SIN'})
                result.status_code = 400
                return result
            else:
                query = "INSERT INTO PROFESSIONAL" \
                        " (SIN, city, firstName, middleInitial, lastName, phoneNumber)" \
                        "VALUES(%s, %s, %s, %s, %s, %s)"
                values = (sin, city, fName, midInitial, lastName, phoneNum)
                cursor.execute(query, values)
                connection.commit()
                result = jsonify(
                    {'status code': 200, 'message': 'Success: Professional was added to the Professional table',
                     'SIN': sin, 'city': city, 'firstName': fName, 'middleInitial': midInitial, 'lastName': lastName,
                     'phoneNumber': phoneNum})
                result.status_code = 200
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(Professional, "/Professional")


class Youth(Resource):
    def post(self, sin):  # inserts into Youth Worker table when creating a new account
        try:  # returns JSON format for confirmation of insert query
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "INSERT INTO YOUTH_WORKER" \
                    " (SIN, certificate)" \
                    "VALUES(%s, %s)"
            certificate = "Youth Care Worker Certificate"
            values = (sin, certificate)
            cursor.execute(query, values)
            connection.commit()
            if cursor.rowcount == 1:
                result = jsonify(
                    {'status code': 200, 'message': 'Success: Youth Worker was added to the Youth Worker table',
                     "SIN": sin, "certificate": certificate})
                result.status_code = 200
                return result
            elif cursor.rowcount == 0:
                result = jsonify(
                    {'status code': 400, 'message': 'Failure: Youth Worker was not added to the Youth Worker table'})
                result.status_code = 400
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(Youth, "/Youth/<sin>")


class Ped(Resource):
    def post(self, sin):  # inserts into Pediatrician table when creating a new account
        try:  # returns JSON format for confirmation of insert query
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "INSERT INTO PEDIATRICIAN" \
                    " (SIN, degree)" \
                    "VALUES(%s, %s)"
            degree = "Doctor of Medicine"
            values = (sin, degree)
            cursor.execute(query, values)
            connection.commit()
            print(cursor.rowcount, "Pediatrician Record Inserted.")
            if cursor.rowcount == 1:
                result = jsonify(
                    {'status code': 200, 'message': 'Success: Pediatrician was added to the Pediatrician table',
                     "SIN": sin, "degree": degree})
                result.status_code = 200
                return result
            elif cursor.rowcount == 0:
                result = jsonify(
                    {'status code': 400, 'message': 'Failure: Pediatrician was not added to the Pediatrician table'})
                result.status_code = 400
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(Ped, "/Ped/<sin>")


class Psy(Resource):
    def post(self, sin):  # inserts into Psychologist table when creating a new account
        try:  # returns JSON format for confirmation of insert query
            connection = mysql.connect()
            cursor = connection.cursor()
            query = "INSERT INTO PSYCHOLOGIST" \
                    " (SIN, degree)" \
                    "VALUES(%s, %s)"
            degree = "Ph.D in Psychology"
            values = (sin, degree)
            cursor.execute(query, values)
            connection.commit()
            print(cursor.rowcount, "Psychologist Record Inserted.")
            if cursor.rowcount == 1:
                result = jsonify(
                    {'status code': 200, 'message': 'Success: Psychologist was added to the Psychologist table',
                     "SIN": sin, "degree": degree})
                result.status_code = 200
                return result
            elif cursor.rowcount == 0:
                result = jsonify(
                    {'status code': 400, 'message': 'Failure: Psychologist was not added to the Psychologist table'})
                result.status_code = 400
                return result
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()


api.add_resource(Psy, "/Psy/<sin>")
