from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database/database.db')
db = SQLAlchemy(app)