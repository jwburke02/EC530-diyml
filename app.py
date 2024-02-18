from flask import Flask, request

import services.auth
import services.data_analysis
import services.data_upload
import services.inference
import services.publishing
import services.reports
import services.test_model
import services.training

app = Flask(__name__)

####################################
# AUTHENTICATION AND AUTHORIZATION #
####################################
"""
    Function: To create a user

    Required Params: username (string), password (string)

    This route allows a user of the API to create a user by inputting a 
    username and password string, each 10 or more characters.
"""
@app.route("/auth/user/create", methods = ['PUT'])
def create_user_route():
    if request.method == 'PUT':
        username = request.args.get('username')
        password = request.args.get('password')
        return services.auth.create_user(username, password)
    else:
        return "[Error] Invalid request type: " + request.method, 422

"""
    Function: To delete a user

    Required Params: username (string), password (string)

    This route allows a user of the API to delete a user by inputting a 
    username and password string that matches an already existing user 
    available for deletion.
"""
@app.route("/auth/user/delete", methods=['DELETE'])
def delete_user_route():
    if request.method == 'DELETE':
        username = request.args.get('username')
        password = request.args.get('password')
        return services.auth.delete_user(username, password)
    else:
        return "[Error] Invalid request type: " + request.method, 422

"""
    Function: To login a user

    Required Params: username (string), password (string)

    This route allows a user of the API to login a user by inputting a 
    username and password string that matches a pre-existing user combination.
    This is what gives the user their authorization token for the API.
"""
@app.route("/auth/user/login", methods=['POST'])
def login_user_route():
    if request.method == 'POST':
        username = request.args.get('username')
        password = request.args.get('password')
        return services.auth.login_user(username, password)
    else:
        return "[Error] Invalid request type: " + request.method, 422

"""
    Function: To logout a user

    Required Params: username (string)

    This route allows a user of the API to logout a user by inputting a 
    username.
"""
@app.route("/auth/user/logout", methods=['POST'])
def logout_user_route():
    if request.method == 'POST':
        username = request.args.get('username')
        return services.auth.logout_user(username)
    else:
        return "[Error] Invalid request type: " + request.method, 422

#####################################
# DATA UPLOADING + PROJECT CREATION #
#####################################
"""
    Function: To create a project folder

    Required Params: project_name (string), 
    project_type ("classification"|"detection"),
    auth_token (string)

    This route allows a user of the API to create a new project folder.
    They must specify the type of learning: detection or classification.
"""
@app.route("/data_upload/project/create", methods=['PUT'])
def create_project_route():
    if request.method == 'PUT':
        auth_token = request.args.get('auth_token')
        project_name = request.args.get('project_name')
        project_type = request.args.get('project_type')
        return services.data_upload.create_project(auth_token, project_name, project_type)
    else:
        return "[Error] Invalid request type: " + request.method, 422

"""
    Function: To delete a project folder

    Required Params: project_name (string), 
    auth_token (string)

    This route allows a user of the API to delete a project folder.
"""
@app.route("/data_upload/project/delete", methods=['DELETE'])
def delete_project_route():
    if request.method == 'DELETE':
        auth_token = request.args.get('auth_token')
        project_name = request.args.get('project_name')
        return services.data_upload.delete_project(auth_token, project_name)
    else:
        return "[Error] Invalid request type: " + request.method, 422

"""
    Function: To add/update images for a project

    Required Params: auth_token (string)

    JSON Required: 
        A list of (filename, image_data)

    This route allows a user of the API to add image data to a project.
"""
@app.route("/data_upload/upload/images/<project_name>", methods=['PUT', 'POST'])
def upload_images_route(project_name):
    if request.method == 'PUT' or request.method == 'POST':
        auth_token = request.args.get('auth_token')
        image_data = request.json.get('image_data')
        return services.data_upload.upload_images(auth_token, image_data)
    else:
        return "[Error] Invalid request type: " + request.method, 422

"""
    Function: To add/update labels for a project

    Required Params: auth_token (string)

    JSON Required: 
        A list of (filename, label_data)

    This route allows a user of the API to add label data to a project.
"""
@app.route("/data_upload/upload/labels/<project_name>", methods=['PUT', 'POST'])
def upload_labels_route(project_name):
    if request.method == 'PUT' or request.method == 'POST':
        auth_token = request.args.get('auth_token')
        label_data = request.json.get('label_data')
        return services.data_upload.upload_labels(auth_token, label_data)
    else:
        return "[Error] Invalid request type: " + request.method, 422

"""
    Function: To add/update class information for a project

    Required Params: auth_token (string)

    JSON Required: 
        A list of classes (strings)

    This route allows a user of the API to add class data to a project.
"""
@app.route("/data_upload/upload/classes/<project_name>", methods=['PUT', 'POST'])
def upload_classes_route(project_name):
    if request.method == 'PUT' or request.method == 'POST':
        auth_token = request.args.get('auth_token')
        class_data = request.json.get('class_data')
        return services.data_upload.upload_classes(auth_token, class_data)
    else:
        return "[Error] Invalid request type: " + request.method, 422

"""
    Function: To delete image information for a project

    Required Params: auth_token (string)
"""
@app.route("/data_upload/delete/images/<project_name>", methods=['DELETE'])
def delete_images_route(project_name):
    if request.method == 'DELETE':
        auth_token = request.args.get('auth_token')
        return services.data_upload.delete_images(auth_token, project_name)
    else:
        return "[Error] Invalid request type: " + request.method, 422
"""
    Function: To delete label information for a project

    Required Params: auth_token (string)
"""
@app.route("/data_upload/delete/labels/<project_name>", methods=['DELETE'])
def delete_labels_route(project_name):
    if request.method == 'DELETE':
        auth_token = request.args.get('auth_token')
        return services.data_upload.delete_labels(auth_token, project_name)
    else:
        return "[Error] Invalid request type: " + request.method, 422
"""
    Function: To delete class information for a project

    Required Params: auth_token (string)
"""
@app.route("/data_upload/delete/classes/<project_name>", methods=['DELETE'])
def delete_classes_route(project_name):
    if request.method == 'DELETE':
        auth_token = request.args.get('auth_token')
        return services.data_upload.delete_classes(auth_token, project_name)
    else:
        return "[Error] Invalid request type: " + request.method, 422

#################
# DATA ANALYSIS #
#################
"""
    Function: To perform data analysis for a given project based on the 
    supplied images and labels:

    Required Params: auth_token (string)

    This endpoint will analyze the infromation present in the labels and images folders for
    the project the user is concerned with and will display statistics about it.
"""
@app.route("/data_analysis/statistics/<project_name>", methods=['POST'])
def statistics_route(project_name):
    if request.method == 'POST':
        auth_token = request.args.get('auth_token')
        return services.data_analysis.statistics(auth_token, project_name)
    else:
        return "[Error] Invalid request type: " + request.method, 422

############
# TRAINING #
############
"""
    Function: to train a specified model

    Required Params: auth_token (string),
    epochs (integer), train_split (float)
"""
@app.route("/training/train_model/<project_name>", methods=['POST'])
def train_model_route(project_name):
    if request.method == 'POST':
        auth_token = request.args.get('auth_token')
        epochs = int(request.args.get('epochs'))
        train_split = float(request.args.get('train_split'))
        return services.training.train_model(auth_token, project_name, epochs, train_split)
    else:
        return "[Error] Invalid request type: " + request.method, 422
    
##############
# PUBLISHING #
##############
"""
    Function: to publish a specified model

    Required Params: auth_token (string),
    model_name (string)
"""
@app.route("/publishing/publish/<project_name>", methods=['POST'])
def publish_model_route(project_name):
    if request.method == 'POST':
        auth_token = request.args.get('auth_token')
        model_name = request.args.get('model_name')
        return services.publishing.publish_model(auth_token, project_name, model_name)
    else:
        return "[Error] Invalid request type: " + request.method, 422

#############
# INFERRING #
#############
"""
    Function: to infer using a specified published model

    Required Params: auth_token (string)

    JSON:
        List of image bytes
"""
@app.route("/inference/predict/<model_name>", methods=['GET'])
def infer_route(model_name):
    if request.method == 'GET':
        auth_token = request.args.get('auth_token')
        image_data = request.json.get('image_data')
        return services.inference.infer(auth_token, model_name, image_data)
    else:
        return "[Error] Invalid request type: " + request.method, 422
    
#################
# TESTING MODEL #
#################
"""
    Function: to test a specified project model

    Required Params: auth_token (string),
    
    JSON:
        List of image bytes
"""
@app.route("/test_model/predict/<project_name>", methods=['GET'])
def test_model_route(project_name):
    if request.method == 'GET':
        auth_token = request.args.get('auth_token')
        image_data = request.json.get('image_data')
        return services.test_model.test_model(auth_token, project_name, image_data)
    else:
        return "[Error] Invalid request type: " + request.method, 422

#############
# REPORTING #
#############
"""
    Function: to report stats about a model already published

    Required Params: auth_token (string),
    
    JSON:
        List of image bytes (testing)
"""
@app.route("/reports/analyze_model/<model_name>", methods=['GET'])
def report_published_route(model_name):
    if request.method == 'GET':
        auth_token = request.args.get('auth_token')
        image_data = request.json.get('image_data')
        return services.reports.report_published(auth_token, model_name, image_data)
    else:
        return "[Error] Invalid request type: " + request.method, 422

"""
    Function: to report stats about a model in development

    Required Params: auth_token (string),
    
    JSON:
        List of image bytes (testing)
"""
@app.route("/reports/analyze_project/<project_name>", methods=['GET'])
def report_unpublished_route(project_name):
    if request.method == 'GET':
        auth_token = request.args.get('auth_token')
        image_data = request.json.get('image_data')
        return services.reports.report_unpublished(auth_token, project_name, image_data)
    else:
        return "[Error] Invalid request type: " + request.method, 422


if __name__ == '__main__':
    app.run(debug=True)