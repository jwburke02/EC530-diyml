from flask_restful import Resource, reqparse
import base64
import os
import DatabaseAccess
from utils import ROOT_DIR, remove_folder_contents_and_folder

class UploadProjectAPI(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser().add_argument('username', help="username cannot be blank...", required=True, location='args')
            username = parser.parse_args()['username']
            projects = DatabaseAccess.getAllProjects(username)
            # remove pid and dids fields, as well as id field
            for project in projects:
                project['dids'] = []
                project['_id'] = None
                project['uid'] = None
            return projects, 200
        except:
            return "There was an issue with your request", 400
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            result = DatabaseAccess.getProjectInfo(args['project_name'], args['api_token'])
            if (result):
                result['_id'] = str(result['_id'])
                result['uid'] = str(result['uid'])
                list_of_dids = result['dids']
                new_list_of_dids = []
                for did in list_of_dids:
                    new_list_of_dids.append(str(did))
                result['dids'] = new_list_of_dids
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
        except:
            return "There was some issue with your request", 400
    def patch(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            DatabaseAccess.deleteProject(args['project_name'], args['api_token'])
            # PERFORM DELETION OF LOCALSTORAGE
            remove_folder_contents_and_folder(f"{ROOT_DIR}/LOCALSTORAGE/{args['project_name']}")
            return {"Status": "Successful deletion"}, 200
        except:
            return "There was some issue with your request", 400
        
class UploadDataAPI(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('data_point_name',help="Data point name cannot be blank",required=True).add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            result = DatabaseAccess.getDatapoint(args['data_point_name'], args['project_name'], args['api_token'])
            if (result):
                result['_id'] = str(result['_id'])
                result['pid'] = str(result['pid'])
                return result, 200
            else:
                return {'Error' : 'no such data_point found'}, 404
        except:
            return "There was some issue with your request", 400
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('image_data', required=True).add_argument('label_data', required=True).add_argument('data_point_name',help="Data point name cannot be blank",required=True).add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            # generate location in file system
            location = f"{ROOT_DIR}/LOCALSTORAGE/{args['project_name']}/{args['data_point_name']}.jpg"
            # place at location in file system
            if not os.path.exists(f"{ROOT_DIR}/LOCALSTORAGE/{args['project_name']}"):
                os.makedirs(f"{ROOT_DIR}/LOCALSTORAGE/{args['project_name']}")
            base64_string = args['image_data']
            image_bytes = base64.b64decode(base64_string)
            # Write the bytes to the file
            with open(location, "wb") as file:
                file.write(image_bytes)
            # modify in mongo
            DatabaseAccess.addDatapoint(args['data_point_name'], args['project_name'], args['api_token'], location, args['label_data'])
            return {"Status": "Successful data point upload."}, 200
        except Exception as e:
            print(e)
            return "There was some issue with your request", 400
    def patch(self):
        try:
            parser = reqparse.RequestParser().add_argument('data_point_name',help="Data point name cannot be blank",required=True).add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            # local deletion of file
            if os.path.exists(f"{ROOT_DIR}/LOCALSTORAGE/{args['project_name']}/{args['data_point_name']}.jpg"):
                os.remove(f"{ROOT_DIR}/LOCALSTORAGE/{args['project_name']}/{args['data_point_name']}.jpg")
            DatabaseAccess.deleteDatapoint(args['data_point_name'], args['project_name'], args['api_token'])
            return {"Status": "Successful deletion"}, 200
        except:
            return "There was some issue with your request", 400
        
class UploadClassAPI(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            class_list = DatabaseAccess.getProjectClasses(args['project_name'], args['api_token'])
            if (class_list):
                return {"class_list": class_list}, 200
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