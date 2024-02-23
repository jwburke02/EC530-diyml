from services.auth import AuthenticationAPI
from core import app, api

# add configured service endpoints  
api.add_resource(AuthenticationAPI, '/auth')

# run on all available hosts locally on 7001
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7001)