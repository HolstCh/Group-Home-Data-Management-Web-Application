from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Resource is a class, Hello inherits from Resource, GET is HTTP method, parameter "name" is on add_resource():
api = Api(app)


class Hello(Resource):
    def get(self, name):
        return {"Hello": name}


api.add_resource(Hello, '/hello/<name>')
