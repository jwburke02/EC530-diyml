from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
from random import randint

# define application + api
app = Flask(__name__)
api = Api(app)

# configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database/database.db')
db = SQLAlchemy(app)

# define database schema in SQLAlchemy to reflect schema in database.db
# CREATE TABLE user(
# id int primary key,
# username text not null,
# hashed_pass text not null,
# api_token text not null);

class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    hashed_pass = db.Column(db.String(200), nullable = False)
    api_token = db.Column(db.String(200), nullable = False)

    def __init__(self, id, username, hashed_pass, api_token):
        self.id = id
        self.username = username
        self.hashed_pass = hashed_pass
        self.api_token = api_token

    def __repr__(self):
        return self.username

# Define data schema for user output
user_definition = {
    'uid' : fields.Integer,
    'username' : fields.String,
    'api_token' : fields.String
}

class FormatUser(object):
    def __init__(self, uid, username, api_token):
        self.uid = uid
        self.username = username
        self.api_token = api_token

userpassParse = reqparse.RequestParser()
userpassParse.add_argument('username', help="Username cannot be blank...")
userpassParse.add_argument('password', help="Password cannot be blank...")
userpasstokenParse = reqparse.RequestParser()
userpasstokenParse.add_argument('username', help="Username cannot be blank...")
userpasstokenParse.add_argument('password', help="Password cannot be blank...")
userpasstokenParse.add_argument('uid', help="Must provide a valid uid...")
userpasstokenParse.add_argument('api_token', help="Must provide a valid api_token...")

def generateUID():
    min = 1
    max = 100000
    rand = randint(min, max)
    while user.query.filter_by(id=rand).limit(1).first() is not None:
        rand = randint(min, max)
    return rand

class AuthenticationAPI(Resource):
    @marshal_with(user_definition)
    def get(self):
        try:
            args = userpassParse.parse_args()
            print(args)
            hashed_pass = hashlib.md5(args['password'].encode('UTF-8')).hexdigest()
            result = user.query.filter_by(username=args['username'], hashed_pass=hashed_pass).first()
            print(result)
            if (result):
                return FormatUser(result.id, result.username, result.api_token)
            else:
                return {'error' : 'no such user found'}, 404
        except Exception as e:
            print(e)
    @marshal_with(user_definition)
    def post(self):
        try:
            args = userpasstokenParse.parse_args()
            hashed_pass = hashlib.md5(args['password'].encode('UTF-8')).hexdigest()
            new_user = user(args['uid'], args['username'], hashed_pass, args['api_token'])
            db.session.add(new_user)
            db.session.commit()
            return FormatUser(args['uid'], args['username'], args['api_token'])
        except Exception as e:
            print(e)
            return e
    @marshal_with(user_definition)
    def put(self):
        try:
            args = userpassParse.parse_args()
            hashed_pass = hashlib.md5(args['password'].encode('UTF-8')).hexdigest()
            api_token = hashlib.md5(hashed_pass.encode('UTF-8')).hexdigest()
            print(hashlib.md5(args['password'].encode('UTF-8')).hexdigest())
            new_id = generateUID()
            new_user = user(new_id, args['username'], hashed_pass, api_token)
            db.session.add(new_user)
            db.session.commit()
            return FormatUser(new_id, args['username'], api_token)
        except Exception as e:
            print(e)
            return e
    def delete(self):
        try:
            args = userpasstokenParse.parse_args()
            result = user.query.filter_by(id=args['uid'], username=args['username'], hashed_pass=hashlib.md5(args['password'].encode('UTF-8')).hexdigest(), api_token=args['api_token'])
            if (result):
                db.session.delete(result)
                db.session.commit()
            else:
                return {'error' : 'no such user found'}, 404
        except Exception as e:
            return e
    
api.add_resource(AuthenticationAPI, '/auth')

if __name__ == '__main__':
    app.run()