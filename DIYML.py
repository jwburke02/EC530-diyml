from Auth import AuthenticationAPI
from DataAnalysis import DataAnalysisAPI
from AnalyzeModel import AnalyzeModelAPI
from DataUpload import UploadDataAPI, UploadClassAPI, UploadProjectAPI
from Inference import InferenceAPI
from Publishing import PublishAPI
from Reports import ReportsAPI
from Training import TrainAPI
from flask import Flask
from flask_restful import Api

# app and api are defined by Flask
app = Flask(__name__)
api = Api(app)

# add configured service endpoints  
api.add_resource(AuthenticationAPI, '/auth')  # Auth
api.add_resource(DataAnalysisAPI, '/data_analysis')  # image/label data info
api.add_resource(AnalyzeModelAPI, '/analyze_model')  # model results + scores
api.add_resource(UploadDataAPI, '/upload/data_point')  # datapoint upload (images + labels)
api.add_resource(UploadClassAPI, '/upload/class_info')  # class upload (list of strings)
api.add_resource(UploadProjectAPI, '/upload/project')  # project upload (new project document)
api.add_resource(InferenceAPI, '/inference')  # API for detection or classification using a trained model
api.add_resource(PublishAPI, '/publish')  # API for publishing a project as a model
api.add_resource(ReportsAPI, '/reporting')  # API for reporting model stats
api.add_resource(TrainAPI, '/train')  # API for training

# run on all available hosts locally on 7001
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001)