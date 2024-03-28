from flask_restful import Resource, reqparse
import DatabaseAccess

class DataAnalysisAPI(Resource):
    '''
    RETURNS DETAILED INFORMATION ABOUT A PROJECT DATA
    '''
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('api_token', help="API Token cannot be blank...", required=True).add_argument('project_name', help="Project Name cannot be blank...", required=True)
            args = parser.parse_args()
            result = DatabaseAccess.analyzeProject(args['project_name'], args['api_token'])
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such project found'}, 404
        except:
            return "There was some issue with your request", 400