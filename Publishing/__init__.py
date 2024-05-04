from flask_restful import Resource, reqparse
import DatabaseAccess

class PublishAPI(Resource):
    def get(self):
            '''
                This endpoint gets all published projects from username
            '''
            try:
                parser = reqparse.RequestParser().add_argument('username', location='args')
                args = parser.parse_args()
                projects = DatabaseAccess.getAllProjectsPublished(args['username'])
                if (projects):
                    for project in projects:
                        project['dids'] = []
                        project['_id'] = None
                        project['uid'] = None
                    return projects
                else:
                    return "Could not find any projects for this user", 200
            except:
                return "There was some issue with your request", 400

    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('api_token', help="API Token cannot be blank...", required=True).add_argument('project_name', help="Project Name cannot be blank...", required=True).add_argument('is_published', help="is_published Token cannot be blank...", required=True)
            args = parser.parse_args()
            DatabaseAccess.projectPublishing(args['project_name'], args['api_token'], args['is_published'])
            is_pub = args['is_published']
            return {'Status' : f'Operation successful, is_published set to {is_pub}'}, 200
        except Exception as e:
            print(e)
            return "There was some issue with your request", 400