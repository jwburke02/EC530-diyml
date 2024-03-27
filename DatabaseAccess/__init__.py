import pymongo
import config
import hashlib
import re

# Connect to MongoDB Atlas
client = pymongo.MongoClient(config.atlas_uri)
# Access the database 
db = client['diyml']

def createNewUserInDatabase(username, password):
    # specify user collection
    collection = db['user']
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
    result = collection.insert_one(user_doc)
    
    # Check if insertion was successful
    if result.inserted_id:
        print("User added successfully.")
    else:
        print("Failed to add user.")
    return

def createNewProjectInDatabase(project_name, project_type, api_token):
    # we need two collections here
    user_collection = db['user']
    project_collection = db['project']
    # get uid from the user with api_token
    user = user_collection.find_one({"api_token": api_token})
    uid = user["_id"]
    # create project object
    project_doc = {
        "project_name": project_name,
        "project_type": project_type,
        "current_url": "None",
        "is_published": False,
        "classes": [],
        "dids": [],
        "uid": uid
    }
    # place project in storage
    project_collection.insert_one(project_doc)
    return

def createNewDataPointInDatabase(project_name, data_point_name, label_data, location):
    # we need access to both the project collection and data_point collection
    data_point_collection = db['data_point']
    project_collection = db['project']
    # we create the object
    data_point_doc = {
        "name": data_point_name,
        "location": location,
        "labels": re.split('|', label_data)
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