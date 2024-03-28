from flask_restful import Resource, reqparse
from JovQueue import JovQueue
from ultralytics import YOLO
from utils import remove_folder_contents_and_folder, ROOT_DIR
import DatabaseAccess
import os
import base64

stored_inferences = {}

def makeInference(args):
    '''
    This function makes an inference using a model and then sends the result to a variable located inside the Inference module to be later accessed
    '''
    project_name = args['project_name']
    inference_mapping = args['inference_mapping']
    api_token = args['api_token']
    image_data = args['image_data']
    project = DatabaseAccess.getProjectInfo(project_name, api_token)
    if project['current_url'] == 'NONE':
        return # we have nothing to infer with
    # MUST BE REPLACED WITH INFERENCE LOGIC
    model = YOLO(project['current_url'])
    # place image_data into local path and figure out the path
    decoded_binary = base64.b64decode(image_data)
    with open(f"{ROOT_DIR}/{project_name}.jpg", "wb") as image_file: # temp file
        image_file.write(decoded_binary)
    results = model.predict(f"{ROOT_DIR}/{project_name}.jpg")
    # cleanup image path and place results
    os.remove(f"{ROOT_DIR}/{project_name}.jpg")
    result = results[0]
    length = len(result.boxes)
    response = []
    for box in result.boxes:
      cords = box.xyxy[0].tolist()
      class_id = box.cls[0].item()
      conf = box.conf[0].item()
      type = result.names[class_id]
      response.append({
          "coords": cords,
          "classification": type,
          "confidence": conf
      })
    if length == 0:
        response = ["Nothing Detected in Image"]
    stored_inferences[inference_mapping] = response
    return

inference_queue = JovQueue(3, makeInference)

class InferenceAPI(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser().add_argument('inference_mapping', help="inference mapping cannot be left blank...", location="args")
            args = parser.parse_args()
            inference_mapping = int(args['inference_mapping'])
            result = stored_inferences[inference_mapping]
            del stored_inferences[inference_mapping]
            return result, 200
        except:
            return "There was some issue with your request", 400

    def post(self):
        try:
            parser = reqparse.RequestParser().add_argument('api_token', help="API Token cannot be blank...", required=True).add_argument('project_name', help="Project Name cannot be blank...", required=True).add_argument('image_data', required=True)
            args = parser.parse_args()
            # place into queue
            arguments = {}
            arguments['project_name'] = args['project_name']
            arguments['image_data'] = args['image_data']
            arguments['api_token'] = args['api_token']
            for i in range(100):
                if i in stored_inferences:
                    continue
                else:
                    arguments['inference_mapping'] = i
                    break
            inference_queue.run(arguments)
            result = {
                "RequestResult": "Inference placed in queue for processing.",
                "inference_mapping": arguments['inference_mapping']
            }
            if (result):
                return result, 200
            else:
                return {'Error' : 'no such project found'}, 404
        except:
            return "There was some issue with your request", 400