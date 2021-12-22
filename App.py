from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# -----------------------------------------------------------------------------------------------------------------------
# This is experimenting trying to make the api
# Resource is a class, Hello inherits from Resource, GET is HTTP method, parameter "name" is on add_resource():
api = Api(app)

args = reqparse.RequestParser()
args.add_argument("username", type=str, help="name of user")
args.add_argument("password", type=str, help="pass of user")
args.add_argument("professionName", type=str, help="prof of user")
args.add_argument("SIN", type=int, help="sin of user")
args.add_argument("city", type=str, help="city of user")
args.add_argument("firstName", type=str, help="fname of user")
args.add_argument("middleInitial", type=str, help="middle initial of user")
args.add_argument("lastName", type=str, help="last name of user")
args.add_argument("phoneNumber", type=str, help="phone # of user")


class CreateAccount(Resource):
    def post(self):
        post = args.parse_args()
        return post, 201


api.add_resource(CreateAccount, '/CreateAccount')
