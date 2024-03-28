from flask_restful import Resource, reqparse
import DatabaseAccess

class UploadProjectAPI(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            result = DatabaseAccess.getProjectInfo(args['project_name'], args['api_token'])
            if (result):
                result['_id'] = str(result['_id'])
                result['uid'] = str(result['uid'])
                return result, 200
            else:
                return {'Error' : 'no such project found'}, 404
        except:
            return "There was some issue with your request", 400
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('project_type', help="Project type cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            project_id = DatabaseAccess.createProject(args['project_name'], args['project_type'], args['api_token'])
            result = {
                "project_name": args['project_name'],
                "project_type": args['project_type'],
                "project_id": str(project_id)
            }
            return result, 200
        except Exception as e:
            return "There was some issue with your request", 400
    def patch(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            DatabaseAccess.deleteProject(args['project_name'], args['api_token'])
            return {"Status": "Successful deletion"}, 200
        except:
            return "There was some issue with your request", 400
        
class UploadDataAPI(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('data_point_name',help="Data point name cannot be blank",required=True).add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "data_point_name": args['data_point_name'],
                "image_data": "oi76yiuytfi87astbiua7stik7abteiob7atkauy",
                "label_data": ["label1", "label2"]
            }
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such data_point found'}, 404
        except:
            return "There was some issue with your request", 400
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('image_data', required=True).add_argument('label_data', required=True).add_argument('data_point_name',help="Data point name cannot be blank",required=True).add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "data_point_name": args['data_point_name']
            }
            return result, 200
        except:
            return "There was some issue with your request", 400
    def patch(self):
        try:
            parser = reqparse.RequestParser().add_argument('data_point_name',help="Data point name cannot be blank",required=True).add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "data_point_name": args['data_point_name'],
                "api_token": "token"
            }
            if (result):
                return {"Status": "Successful deletion"}, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except:
            return "There was some issue with your request", 400
        
class UploadClassAPI(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            class_list = DatabaseAccess.getProjectClasses(args['project_name'], args['api_token'])
            if (class_list):
                return class_list, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except:
            return "There was some issue with your request", 400
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('class_info', help="Class types cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            DatabaseAccess.addProjectClasses(args['project_name'], args['api_token'], args['class_info'])
            return {"Status": "Classes Added."}, 200
        except:
            return "There was some issue with your request", 400
    def patch(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            DatabaseAccess.deleteProjectClasses(args['project_name'], args['api_token'])
            return {"Status": "Successful deletion"}, 200
        except:
            return "There was some issue with your request", 400