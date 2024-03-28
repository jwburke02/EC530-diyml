import pymongo
import hashlib
import os
from dotenv import load_dotenv

# Retrieve environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Establish MongoDB connection
client = pymongo.MongoClient(MONGO_URI)

db = client['diyml']

user_collection = db['user']
project_collection = db['project']
data_point_collection = db['data_point']

########
# USER #
######## 
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
#############
# DATAPOINT #
#############

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

#############
# DATAPOINT #
#############
def createNewDataPointInDatabase(project_name, data_point_name, label_data, location):
    # we need access to both the project collection and data_point collection
    data_point_collection = db['data_point']
    project_collection = db['project']
    # we create the object
    data_point_doc = {
        "name": data_point_name,
        "location": location,
        "labels": label_data.split("|")
    }
    # place in the data_point and grab the id
    did = data_point_collection.insert_one(data_point_doc).inserted_id
    # we should now push the did to the appropriate project
    result = project_collection.update_one(
        {"project_name": project_name},
        {"$push": {"dids": did}}
    )
    # Check if the update was successful
    if result.modified_count > 0:
        print("Value appended successfully.")
    else:
        print("Failed to append value.")
    return