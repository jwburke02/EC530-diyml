def report_published(auth_token, model_name, image_data):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if model_name is None or not isinstance(model_name, str):
        return "[Error] Invalid parameter - model_name", 422
    if image_data is None or not isinstance(image_data, list):
        return "[Error] Invalid parameter - image_data", 422
    return "Success", 200
def report_unpublished(auth_token, project_name, image_data):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project name", 422
    if image_data is None or not isinstance(image_data, list):
        return "[Error] Invalid parameter - image_data", 422
    return "Success", 200