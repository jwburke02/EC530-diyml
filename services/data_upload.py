from flask_restful import Resource, reqparse

class UploadProjectAPI(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "project_type": 'classification',
                "project_id": 1
            }
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except:
            return "There was some issue with your request", 400
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('project_type', help="Project type cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "project_type": args['project_type'],
                "project_id": 1
            }
            return result, 200
        except Exception as e:
            return "There was some issue with your request", 400
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('project_type', help="Project type cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "project_type": args['project_type'],
                "project_id": 1
            }
            return result, 200
        except Exception as e:
            return "There was some issue with your request", 400
    def delete(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "api_token": "token"
            }
            if (result):
                return {"Status": "Successful deletion"}, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except:
            return "There was some issue with your request", 400
        
class UploadDataAPI(Resource):
    def get(self):
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
    def post(self):
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
    def delete(self):
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
    def get(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "class_info": 'class information about project'
            }
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except:
            return "There was some issue with your request", 400
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('class_info', help="Class types cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "class_info": args['class_info']
            }
            return result, 200
        except:
            return "There was some issue with your request", 400
    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('class_info', help="Class types cannot be blank...", required=True).add_argument('api_token', help="API token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "class_info": args['class_info']
            }
            return result, 200
        except:
            return "There was some issue with your request", 400
    def delete(self):
        try:
            parser = reqparse.RequestParser().add_argument('project_name', help="Project name cannot be blank...", required=True).add_argument('api_token', help="API Token cannot be blank...", required=True)
            args = parser.parse_args()
            result = {
                "project_name": args['project_name'],
                "class_info": "Class info",
                "api_token": "token"
            }
            if (result):
                return {"Status": "Successful deletion"}, 200
            else:
                return {'Error' : 'no such user found'}, 404
        except:
            return "There was some issue with your request", 400