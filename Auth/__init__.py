from flask_restful import Resource, reqparse
import DatabaseAccess

class AuthenticationAPI(Resource):
    def get(self): #check if user exist
        try:
            parser = reqparse.RequestParser().add_argument('username', help="Username cannot be blank...", required=True, location='args')
            args = parser.parse_args()
            if DatabaseAccess.userExists(args['username']):
                return True, 200
            else:
                return False, 200
        except:
            return "There was some error with your request", 400
    def post(self): # LOGIN
        try:
            parser = reqparse.RequestParser().add_argument('username', help="Username cannot be blank...", required=True).add_argument('password', help="Password cannot be blank...", required=True)
            args = parser.parse_args()
            api_token = DatabaseAccess.loginUser(args['username'], args['password'])
            result = {
                "username": args['username'],
                "api_token": api_token,
                "status": "USER LOGGED IN"
            }
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except:
            return "There was some issue with your request", 400
    def put(self): # USER CREATION
        try:
            parser = reqparse.RequestParser().add_argument('username', help="Username cannot be blank...", required=True).add_argument('password', help="Password cannot be blank...", required=True)
            args = parser.parse_args()
            if DatabaseAccess.userExists(args['username']):
                return "User already exists.", 400
            api_token = DatabaseAccess.createUser(args['username'], args['password'])
            result = {
                "username": args['username'],
                "api_token": api_token,
                "status": "USER CREATED"
            }
            return result, 200
        except Exception as e:
            return "There was some issue with your request", 400
    def patch(self): # USER DELETION
        try:
            parser = reqparse.RequestParser().add_argument('username', help="Username cannot be blank...", required=True).add_argument('password', help="Password cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            DatabaseAccess.deleteUser(args['username'], args['password'], args['api_token'])
            return {"Status": "Successful deletion"}, 200
        except:
            return "There was some issue with your request", 400