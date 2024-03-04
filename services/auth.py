from flask_restful import Resource, reqparse

class AuthenticationAPI(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('username', help="Username cannot be blank...", required=True).add_argument('password', help="Password cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "username": args['username'],
                "api_token": 'fake_token'
            }
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except:
            return "There was some issue with your request", 400
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('username', help="Username cannot be blank...", required=True).add_argument('password', help="Password cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "username": args['username'],
                "api_token": 'new_api_token'
            }
            return result, 200
        except Exception as e:
            return "There was some issue with your request", 400
    def patch(self):
        try:
            parser = reqparse.RequestParser().add_argument('username', help="Username cannot be blank...", required=True).add_argument('password', help="Password cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "username": args['username'],
                "password": args['password'],
                "api_token": args['api_token']
            }
            if (result):
                return {"Status": "Successful deletion"}, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except:
            return "There was some issue with your request", 400