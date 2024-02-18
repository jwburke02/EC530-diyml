def create_project(auth_token, project_name, project_type):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project_name", 422
    if project_type is None or not isinstance(project_type, str):
        return "[Error] Invalid parameter - project_type", 422
    return "Success", 200

def delete_project(auth_token, project_name):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project_name", 422
    return "Success", 200

def upload_images(auth_token, image_data, project_name):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project name", 422
    if image_data is None or not isinstance(image_data, list):
        return "[Error] Invalid parameter - image_data", 422
    return "Success", 200

def upload_labels(auth_token, label_data, project_name):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project name", 422
    if label_data is None or not isinstance(label_data, list):
        return "[Error] Invalid parameter - label_data", 422
    return "Success", 200

def upload_classes(auth_token, class_data, project_name):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project name", 422
    if class_data is None or not isinstance(class_data, list):
        return "[Error] Invalid parameter - class_data", 422
    return "Success", 200

def delete_images(auth_token, project_name):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project name", 422
    return "Success", 200

def delete_labels(auth_token, project_name):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project name", 422
    return "Success", 200

def delete_classes(auth_token, project_name):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project name", 422
    return "Success", 200