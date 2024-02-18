def train_model(auth_token, project_name, epochs, train_split):
    if auth_token is None or not isinstance(auth_token, str):
        return "[Error] Invalid token", 422
    if project_name is None or not isinstance(project_name, str):
        return "[Error] Invalid parameter - project_name", 422
    if epochs is None or epochs < 1 or epochs > 250:
        return "[Error] Invalid parameter - epochs", 422
    if train_split is None or train_split < 0.1 or train_split > 1.0:
        return "[Error] Invalid parameter - train_split (between 0 and 1)", 422
    return "Success", 200