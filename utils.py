import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def remove_folder_contents_and_folder(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            remove_folder_contents_and_folder(item_path)

    os.rmdir(folder_path)