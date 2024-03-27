import pymongo
import config
import hashlib

# Connect to MongoDB Atlas
client = pymongo.MongoClient(config.atlas_uri)

# Access the database collections
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

#############
# DATAPOINT #
#############

###########
# CLASSES #
###########

########
# USER #
######## 
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

###########
# PROJECT #
###########
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

def addClassesToProjectInDatabase(project_name, class_info):
    # we need the project_collection
    project_collection = db['project']
    # we should overwrite the classes of the current project
    class_list = class_info.split("|")
    result = project_collection.update_one(
        {"project_name": project_name},
        {"$set": {"classes": class_list}}
    )
    # Check if the update was successful
    if result.modified_count > 0:
        print("Value appended successfully.")
    else:
        print("Failed to append value.")
    return

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