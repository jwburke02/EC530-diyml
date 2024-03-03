from flask_restful import Resource, reqparse

class TrainAPI(Resource):
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('api_token', help="API Token cannot be blank...", required=True).add_argument('project_name', help="Project Name cannot be blank...", required=True).add_argument('train_split', required=True).add_argument('epochs', required=True)
            args = parser.parse_args()
            result = {
                "Status": "Model is trained...",
                "TrainResults": "Example results"
            }
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such project found'}, 404
        except:
            return "There was some issue with your request", 400