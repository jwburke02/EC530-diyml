import pymongo
import hashlib
import os
from dotenv import load_dotenv

# Retrieve environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Functions for retrieving collection with custom schema
def userCollection(DB):
    if "user" in DB.list_collection_names():
        print("DATABASE: Returning existing structured database (user).")
        return DB['user']
    else:
        print("DATABASE: Returning new structured database (user).")
        return DB.create_collection('user', validator= {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["username", "hashed_pass", "api_token"],
                        "properties": {
                            "username": {"bsonType": "string"},
                            "hashed_pass": {"bsonType": "string"},
                            "api_token": {"bsonType": "string"}
        }}})
def projectCollection(DB):
    if "project" in DB.list_collection_names():
        print("DATABASE: Returning existing structured database (project).")
        return DB['project']
    else:
        print("DATABASE: Returning new structured database (project).")
        return DB.create_collection('project', validator= {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["uid", "project_name", "project_type", "current_url", "is_published", "classes", "dids"],
                        "properties": {
                            "uid": {"bsonType": "objectId"},
                            "project_name": {"bsonType": "string"},
                            "project_type": {"bsonType": "string"},
                            "current_url": {"bsonType": "string"},
                            "is_published": {"bsonType": "bool"},
                            "classes": {
                                "bsonType": "array",
                                "items": {"bsonType": "string"}
                            },
                            "dids": {
                                "bsonType": "array",
                                "items": {"bsonType": "objectId"}
                            }
        }}})
def dataPointCollection(DB):
    if "data_point" in DB.list_collection_names():
        print("DATABASE: Returning existing structured database (data_point).")
        return DB['data_point']
    else:
        print("DATABASE: Returning new structured database (data_point).")
        return DB.create_collection('data_point', validator= {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["pid", "name", "location", "labels"],
                        "properties": {
                            "pid": {"bsonType": "objectId"},
                            "name": {"bsonType": "string"},
                            "location": {"bsonType": "string"},
                            "labels": {
                                "bsonType": "array",
                                "items": {"bsonType": "string"}
                            }
        }}})

# Establish MongoDB connection
client = pymongo.MongoClient(MONGO_URI)

db = client['diyml']

user_collection = userCollection(db)
project_collection = projectCollection(db)
data_point_collection = dataPointCollection(db)

########
# USER #
######## 
'''
RETURN TRUE IF EXIST
'''
def userExists(username):
    if (user_collection.find_one({"username": username})):
        return True
    else:
        return False

'''
CREATION
'''
def createUser(username, password):
    # hash for password (and api key)
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashed_pass = sha256_hash.hexdigest()
    sha256_hash.update(hashed_pass.encode('utf-8'))
    api_token = sha256_hash.hexdigest()
    # create user object
    user_doc = {
        "username": username,
        "hashed_pass": hashed_pass,
        "api_token": api_token
    }
    # Insert the user document into the collection
    result = user_collection.insert_one(user_doc)
    # Check if insertion was successful
    if result.inserted_id:
        return api_token
    else:
        raise Exception("Unable to create user.")
'''
DELETION
'''
def deleteUser(username, password, api_token):
    # HASH PASSWORD
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashed_pass = sha256_hash.hexdigest()
    # FIND USER TO DELETE
    result = user_collection.delete_one({
        "username": username,
        "hashed_pass": hashed_pass,
        "api_token": api_token
    })
    if result.deleted_count == 1:
        return 
    else:
        raise Exception("Unable to delete user.")
'''
LOGIN
'''
def loginUser(username, password):
    # HASH PASSWORD
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashed_pass = sha256_hash.hexdigest()
    # FIND USER TO LOGIN
    found_user = user_collection.find_one({
        "username": username,
        "hashed_pass": hashed_pass,
    })
    if found_user:
        return found_user['api_token']
    else:
        raise Exception("Unable to find a user.")
###########
# PROJECT #
###########
'''
PROJECT EXISTS
'''
def projectExists(project_name):
    if (project_name.find_one({"project_name": project_name})):
        return True
    else:
        return False
'''
PROJECT CREATION
'''
def createProject(project_name, project_type, api_token):
    # check if api_token present in users table
    user = user_collection.find_one({"api_token": api_token})
    # check if project present already
    project = project_collection.find_one({"project_name": project_name})
    if (project):
        raise Exception("You cant create this, name taken.")
    if user:
        project_doc = {
            "uid": user['_id'],
            "project_name": project_name,
            "project_type": project_type,
            "current_url": "NONE",
            "is_published": False,
            "classes": [],
            "dids": []
        }
        result = project_collection.insert_one(project_doc).inserted_id
        if (result):
            return result
        else:
            raise Exception("Unable to create project.")
    else:
        raise Exception("Invalid api_token")
'''
PROJECT DELETION
'''
def deleteProject(project_name, api_token):
    # check if this is project associated with api_token
    project = project_collection.find_one({"project_name": project_name})
    user = user_collection.find_one({"api_token": api_token})
    if user['_id'] == project['uid']:
        dids_to_delete = project['dids']
        project_collection.delete_one({"project_name": project_name})
        for did in dids_to_delete:
            data_point_collection.delete_one({"_id": did})
    else:
        raise Exception("Incorrect api_key given project name.")
'''
PROJECT DETAIL ENDPOINT
'''
def getProjectInfo(project_name, api_token):
    # check if this is project associated with api_token
    project = project_collection.find_one({"project_name": project_name})
    user = user_collection.find_one({"api_token": api_token})
    if user['_id'] == project['uid']:
        # return the project
        return project
    else:
        raise Exception("Incorrect api_key given project name.")
'''
GET ALL PROJECT INFOS
'''
def getAllProjects(username):
    # get uid from user_name
    user = user_collection.find_one({"username": username})
    uid = user['_id']
    # use this uid to get every possible project
    projcursor = project_collection.find({"uid": uid})
    return [item for item in projcursor]

'''
ADD URL TO PROJECT
'''
def addModelURLToProject(project_name, URL):
    project_collection.update_one({"project_name": project_name}, {"$set": {"current_url": URL}})
    return

'''
PUBLISH/UNPUBLISH PROJECT
'''
def projectPublishing(project_name, api_token, is_published):
    # check if this is project associated with api_token
    project = project_collection.find_one({"project_name": project_name})
    user = user_collection.find_one({"api_token": api_token})
    if user['_id'] == project['uid']:
        # add classes to project
        result = project_collection.update_one(
            {"project_name": project_name},
            {"$set": {"is_published": is_published}}
        )
        if result.modified_count > 0:
            return
        else:
            raise Exception("Unable to modify published status of project.")
    else:
        raise Exception("Incorrect api_key given project name.")

###########
# CLASSES #
###########
'''
VIEW CLASSES FOR PROJECT
'''
def getProjectClasses(project_name, api_token):
    # check if this is project associated with api_token
    project = project_collection.find_one({"project_name": project_name})
    user = user_collection.find_one({"api_token": api_token})
    if user['_id'] == project['uid']:
        # return the project classes
        return project['classes']
    else:
        raise Exception("Incorrect api_key given project name.")
'''
ADD/REPLACE CLASSES TO PROJECT
'''
def addProjectClasses(project_name, api_token, class_info):
    # check if this is project associated with api_token
    project = project_collection.find_one({"project_name": project_name})
    user = user_collection.find_one({"api_token": api_token})
    if user['_id'] == project['uid']:
        # add classes to project
        result = project_collection.update_one(
            {"project_name": project_name},
            {"$set": {"classes": class_info.split("|")}}
        )
        if result.modified_count > 0:
            return
        else:
            raise Exception("Unable to add classes to project.")
    else:
        raise Exception("Incorrect api_key given project name.")
'''
REMOVE CLASSES FROM PROJECT
'''
def deleteProjectClasses(project_name, api_token):
    # check if this is project associated with api_token
    project = project_collection.find_one({"project_name": project_name})
    user = user_collection.find_one({"api_token": api_token})
    if user['_id'] == project['uid']:
        # remove classes from project
        result = project_collection.update_one(
            {"project_name": project_name},
            {"$set": {"classes": []}}
        )
        if result.modified_count > 0:
            return
        else:
            raise Exception("Unable to remove classes from project.")
    else:
        raise Exception("Incorrect api_key given project name.")
    
'''
DATA ANALYSIS DATABASE FUNCTION
'''
def analyzeProject(project_name, api_token):
    # the return from this is forwarded as analysis to endpoint
    # locate project 
    project = project_collection.find_one({"project_name": project_name})
    user = user_collection.find_one({"api_token": api_token})
    response = {} # to be sent as response
    if user['_id'] == project['uid']:
        response['project_name'] = project_name
        response['project_type'] = project['project_type']
        response['is_published'] = project['is_published']
        response['classes'] = project['classes']
        response['data_points'] = []
        for did in project['dids']:
            # get the data from table
            d_dict = {}
            data_point = data_point_collection.find_one({"_id": did})
            d_dict['name'] = data_point['name']
            d_dict['labels'] = data_point['labels']
            response['data_points'].append(d_dict)
        if(response):
            return response
        else: 
            raise Exception("Error analyzing project.")
    else:
        raise Exception("Error finding project.")
        
#############
# DATAPOINT #
#############
'''
ADD NEW DATAPOINT TO PROJECT
'''
def addDatapoint(data_point_name, project_name, api_token, location, label_data):
    # get project id
    project = project_collection.find_one({"project_name": project_name})
    # make sure api_token is valid
    user = user_collection.find_one({"api_token": api_token})
    if project['uid'] != user['_id']:
        raise Exception("Incorrect api_token for associated project.")
    # now we can write data_point with info we have
    data_point_doc = {
        "name": data_point_name,
        "location": location,
        "labels": label_data.split("|"),
        "pid": project['_id'],
    }
    result = data_point_collection.insert_one(data_point_doc).inserted_id
    if (result):
        # append the did to project
        project_collection.update_one(
            {"project_name": project_name},
            {"$push": {"dids": result}}
        )
        return
    else:
        raise Exception("Unable to create data_point.")
'''
DELETE DATAPOINT FROM PROJECT
'''
def deleteDatapoint(data_point_name, project_name, api_token):
    # get project id
    project = project_collection.find_one({"project_name": project_name})
    # make sure api_token is valid
    user = user_collection.find_one({"api_token": api_token})
    if project['uid'] != user['_id']:
        raise Exception("Incorrect api_token for associated project.")
    # grab data_point
    result = data_point_collection.find_one_and_delete({"name": data_point_name, "pid": project['_id']})
    if (result):
        # remove the id from project
        project_collection.update_one({"project_name": project_name},{"$pull": {"dids": result['_id']}})
        return 
    else:
        raise Exception("Unable to delete data_point.")

'''
VIEW DETAIL ABOUT DATAPOINT
'''
def getDatapoint(data_point_name, project_name, api_token):
    print(f"{data_point_name}{project_name}{api_token}")
    # get project id
    project = project_collection.find_one({"project_name": project_name})
    # make sure api_token is valid
    user = user_collection.find_one({"api_token": api_token})
    if project['uid'] != user['_id']:
        raise Exception("Incorrect api_token for associated project.")
    # grab data_point
    result = data_point_collection.find_one({"name": data_point_name, "pid": project['_id']})
    if (result):
        print(result)
        return result
    else:
        raise Exception("Unable to find datapoint.")
    
'''
USE DID TO GET LOCATION AND LABEL LIST
'''
def getDatapointTraining(did):
    data_point = data_point_collection.find_one({"_id": did})
    result = {

    }
    result['location'] = data_point['location']
    result['labels'] = data_point['labels']
    result['name'] = data_point['name']
    return result