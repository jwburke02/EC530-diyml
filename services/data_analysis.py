from flask_restful import Resource, reqparse

class DataAnalysisAPI(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('api_token', help="API Token cannot be blank...", required=True).add_argument('project_name', help="Project Name cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "DataAnalysisResults": "Example results",
                "project_name": args['project_name']
            }
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such project found'}, 404
        except:
            return "There was some issue with your request", 400