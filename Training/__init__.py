from flask_restful import Resource, reqparse
from JovQueue import JovQueue
from ultralytics import YOLO
import os
import shutil
import utils
import DatabaseAccess
import random

ROOT_DIR = utils.ROOT_DIR

def setUpFileSystem(project_name, train_split, api_token):
    train_folder = f"{ROOT_DIR}/LOCALSTORAGE/TRAIN/"
    # generate location in file system
    train_project_location = f"{train_folder}/{project_name}"
    # place at location in file system
    if not os.path.exists(train_project_location):
        os.makedirs(train_project_location)
        os.makedirs(train_project_location + '/train')
        os.makedirs(train_project_location + '/train/images')
        os.makedirs(train_project_location + '/train/labels')
        os.makedirs(train_project_location + '/valid')
        os.makedirs(train_project_location + '/valid/images')
        os.makedirs(train_project_location + '/valid/labels')
        os.makedirs(train_project_location + '/output')
    project_into = DatabaseAccess.getProjectInfo(project_name, api_token)
    dids = project_into['dids']
    if train_split < .5 or train_split > 1:
        train_split = .8
    for iter, did in enumerate(dids):
        result = DatabaseAccess.getDatapointTraining(did)
        # we should create an image and label either in valid or train
        location = result['location']
        labels = result['labels']
        name = result['name']
        # copy from location to train_project_location
        param = random.random()
        if iter == 0:
            # place in train/images
            shutil.copy(location, train_project_location + f'/train/images/{name}.jpg')
            # use labels to create a new file
            with open(train_project_location + f'/train/labels/{name}.txt', 'x') as file:
                for label in labels:
                    file.write(label + "\n")
            # place in valid/images
            shutil.copy(location, train_project_location + f'/valid/images/{name}.jpg')
            # use labels to create a new file
            with open(train_project_location + f'/valid/labels/{name}.txt', 'x') as file:
                for label in labels:
                    file.write(label + "\n")
            continue # this places something in val and test no matter what for first iteration, this allows YOLO to work correctly
        if param < train_split:
            # place in train/images
            shutil.copy(location, train_project_location + f'/train/images/{name}.jpg')
            # use labels to create a new file
            with open(train_project_location + f'/train/labels/{name}.txt', 'x') as file:
                for label in labels:
                    file.write(label + "\n")
        else:
            # place in valid/images
            shutil.copy(location, train_project_location + f'/valid/images/{name}.jpg')
            # use labels to create a new file
            with open(train_project_location + f'/valid/labels/{name}.txt', 'x') as file:
                for label in labels:
                    file.write(label + "\n")
    # NOW we have TRAIN/project_name as a directory we can train from.. must add yaml config
    yaml_array = []
    yaml_array.append(f"path: {ROOT_DIR}/LOCALSTORAGE/TRAIN/{project_name}") # path spec
    yaml_array.append("train: train/images") # train path
    yaml_array.append("val: valid/images") # valid path
    classes = DatabaseAccess.getProjectClasses(project_name, api_token)
    yaml_array.append(f"nc: {len(classes)}")
    names_string = "names: ["
    for iter, classifier in enumerate(classes):
        if iter != len(classes) - 1:
            names_string += f'"{classifier}",'
        else:
            names_string += f'"{classifier}"]'
    yaml_array.append(names_string)
    # write out yaml_array to yaml configuration file
    with open(train_project_location + f'/data.yaml', 'x') as file:
        for configuration in yaml_array:
            file.write(configuration + "\n")
    return train_project_location

def trainModel(train_location, epochs, project_name):
    model = YOLO("yolov8m.pt")
    model.train(data=train_location + f'/data.yaml', epochs=epochs, project=train_location + '/output')
    # now we have to place the best one inside LOCALSTORAGE/MODELS/{project_name}
    output_root = train_location + '/output'
    if not os.path.exists(f'{ROOT_DIR}/LOCALSTORAGE/MODELS/{project_name}'):
        os.makedirs(f'{ROOT_DIR}/LOCALSTORAGE/MODELS/{project_name}') # make directory to store model if not exist
    shutil.copy(output_root + '/train/weights/best.pt', f'{ROOT_DIR}/LOCALSTORAGE/MODELS/{project_name}/model.pt')
    DatabaseAccess.addModelURLToProject(project_name, f'{ROOT_DIR}/LOCALSTORAGE/MODELS/{project_name}/model.pt')
    return

def cleanupFileSystem(train_location):
    utils.remove_folder_contents_and_folder(train_location)
    return

def doTraining(args):
    '''
    This function performs the training of a model, and upon completion, will update current_url for project
    '''
    api_token = args['api_token']
    project_name = args['project_name']
    train_split = args['train_split']
    epochs = int(args['epochs'])
    # MUST BE REPLACED WITH TRAINING LOGIC
    train_location = setUpFileSystem(project_name, train_split, api_token)
    trainModel(train_location, epochs, project_name)
    cleanupFileSystem(train_location)
    return

training_queue = JovQueue(3, doTraining)

class TrainAPI(Resource):
    def put(self):
        try:
            parser = reqparse.RequestParser().add_argument('api_token', help="API Token cannot be blank...", required=True).add_argument('project_name', help="Project Name cannot be blank...", required=True).add_argument('train_split', required=True).add_argument('epochs', required=True)
            args = parser.parse_args()
            arguments = {}
            arguments['api_token'] = args['api_token']
            arguments['project_name'] = args['project_name']
            arguments['train_split'] = float(args['train_split'])
            arguments['epochs'] = args['epochs']
            training_queue.run(arguments)
            result = {
                "RequestResult": "Training has began for this project."
            }
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such project found'}, 404
        except:
            return "There was some issue with your request", 400