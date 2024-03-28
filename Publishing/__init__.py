from flask_restful import Resource, reqparse
import DatabaseAccess

class PublishAPI(Resource):
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('api_token', help="API Token cannot be blank...", required=True).add_argument('project_name', help="Project Name cannot be blank...", required=True).add_argument('is_published', help="is_published Token cannot be blank...", required=True)
            args = parser.parse_args()
            DatabaseAccess.projectPublishing(args['project_name'], args['api_token'], args['is_published'])
            return {'Status' : f'Operation successful, is_published set to {args['is_published']}'}, 200
        except Exception as e:
            print(e)
            return "There was some issue with your request", 400