from services.auth import AuthenticationAPI
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

# add configured service endpoints  
api.add_resource(AuthenticationAPI, '/auth')

# run on all available hosts locally on 7001
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7001)