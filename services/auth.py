from flask_restful import Resource, fields, marshal_with, reqparse
import hashlib
from random import randint

from core import db

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
auth_return = {
    'uid' : fields.Integer,
    'username' : fields.String,
    'api_token' : fields.String,
    'error_string' : fields.String
}

class FormatAuthReturn(object):
    def __init__(self, uid, username, api_token, error_string):
        self.uid = uid
        self.username = username
        self.api_token = api_token
        self.error_string = error_string

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
    @marshal_with(auth_return)
    def get(self):
        try:
            args = userpassParse.parse_args()
            hashed_pass = hashlib.md5(args['password'].encode('UTF-8')).hexdigest()
            result = user.query.filter_by(username=args['username'], hashed_pass=hashed_pass).first()
            if (result):
                return FormatAuthReturn(result.id, result.username, result.api_token, "Successful")
            else:
                return FormatAuthReturn(-1, "Error", "Error", "No user found...")
        except Exception as e:
            return FormatAuthReturn(-1, "Error", "Error", e)
    @marshal_with(auth_return)
    def put(self):
        try:
            args = userpassParse.parse_args()
            if user.query.filter_by(username=args['username']).limit(1).first() is not None:
                return FormatAuthReturn(-1, "Error", "Error", "Username taken.")
            hashed_pass = hashlib.md5(args['password'].encode('UTF-8')).hexdigest()
            api_token = hashlib.md5(hashed_pass.encode('UTF-8')).hexdigest()
            print(hashlib.md5(args['password'].encode('UTF-8')).hexdigest())
            new_id = generateUID()
            new_user = user(new_id, args['username'], hashed_pass, api_token)
            db.session.add(new_user)
            db.session.commit()
            return FormatAuthReturn(new_id, args['username'], api_token, "Successful")
        except Exception as e:
            return FormatAuthReturn(-1, "Error", "Error", e)
    def delete(self):
        try:
            args = userpasstokenParse.parse_args()
            result = user.query.filter_by(id=args['uid'], username=args['username'], hashed_pass=hashlib.md5(args['password'].encode('UTF-8')).hexdigest(), api_token=args['api_token']).first()
            if (result):
                db.session.delete(result)
                db.session.commit()
                return {"Status": "Successful deletion"}, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except Exception as e:
            return e