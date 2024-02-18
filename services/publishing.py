def publish_model(auth_token, project_name, model_name):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project_name", 422
    if model_name is None or not isinstance(model_name, str):
        return "[Error] Invalid parameter - model_name", 422
    return "Success", 200