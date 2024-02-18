def create_user(username, password):
    if username is None or username == "":
        return "[Error] Missing parameter: username", 422
    if password is None or password == "":
        return "[Error] Missing parameter: password", 422
    if len(username) < 10:
        return "[Error] Username must be at least 10 characters long", 422
    if len(password) < 10:
        return "[Error] Username must be at least 10 characters long", 422
    return "Success", 200

def delete_user(username, password):
    if username is None or username == "":
        return "[Error] Missing parameter: username", 422
    if password is None or password == "":
        return "[Error] Missing parameter: password", 422
    return "Success", 200

def login_user(username, password):
    if username is None or username == "":
        return "[Error] Missing parameter: username", 422
    if password is None or password == "":
        return "[Error] Missing parameter: password", 422
    return "Success", 200

def logout_user(username):
    if username is None:
        return "[Error] Missing parameter: username", 422
    return "Success", 200