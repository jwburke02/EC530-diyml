from flask_restful import Resource, reqparse
from JovQueue import JovQueue

def doTraining(args):
    '''
    This function performs the training of a model, and upon completion, will update current_url for project
    '''
    api_token = args['api_token']
    project_name = args['project_name']
    train_split = args['train_split']
    epochs = args['epochs']
    # MUST BE REPLACED WITH TRAINING LOGIC
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
            arguments['train_split'] = args['train_split']
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