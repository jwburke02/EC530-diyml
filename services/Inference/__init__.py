from flask_restful import Resource, reqparse
from JovQueue import JovQueue

stored_inferences = {}

def makeInference(args):
    '''
    This function makes an inference using a model and then sends the result to a variable located inside the Inference module to be later accessed
    '''
    project_name = args['project_name']
    inference_mapping = args['inference_mapping']

    # MUST BE REPLACED WITH INFERENCE LOGIC
    result = {
        "InferenceResults": f"Example inference results for {project_name}"
    }

    stored_inferences[inference_mapping] = result
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