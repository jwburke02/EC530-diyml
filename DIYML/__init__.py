from Auth import AuthenticationAPI
from DataAnalysis import DataAnalysisAPI
from DataUpload import UploadDataAPI, UploadClassAPI, UploadProjectAPI
from Inference import InferenceAPI
from Publishing import PublishAPI
from Training import TrainAPI
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# app and api are defined by Flask
app = Flask(__name__)
CORS(app)
api = Api(app)

# add configured service endpoints  
api.add_resource(AuthenticationAPI, '/auth')  # Auth
api.add_resource(DataAnalysisAPI, '/data_analysis')  # image/label data info
api.add_resource(UploadDataAPI, '/upload/data_point')  # datapoint upload (images + labels)
api.add_resource(UploadClassAPI, '/upload/class_info')  # class upload (list of strings)
api.add_resource(UploadProjectAPI, '/upload/project')  # project upload (new project document)
api.add_resource(InferenceAPI, '/inference')  # API for detection or classification using a trained model
api.add_resource(PublishAPI, '/publish')  # API for publishing a project as a model
api.add_resource(TrainAPI, '/train')  # API for training