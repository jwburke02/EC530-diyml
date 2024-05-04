# EC530 - DIY Maching Learning Backend
## Note on Frontend
The frontend for this can be found here: https://github.com/jwburke02/EC530-diyml-react-ui
## Running the Project
The backend for this project can be ran through the following means:
1. Clone this repository.
2. Create a virtual python environment.
3. Download all dependencies using `pip install -r requirements.txt`.
4. Run the application using `python3 DIYML.py`.  
The backend can also be installed as a python package. https://test.pypi.org/project/DIYML/0.0.1/ is where this is hosted (on test pypi).  
In order to run the application using the package:
1. Ensure all requirements in requirements.txt are installed in your environment.
2. Ensure DIYML is downloaded: pip install -i https://test.pypi.org/simple/ DIYML==0.0.1
3. Run `DIYML` by importing `app` from `DIYML` and doing `app.run(host='0.0.0.0', port=7001)`
4. Ensure the `utils.py` folder is present when running this module. It is found in the backend repo here.
## API Descriptions and Uses
### Auth
This is a module that deals with creating accounts for users of this service. Additionally, it is responsible for lending out the authorization tokens needed by the other APIs.
- The GET function is responsible for returning if a user exists to the caller
- The POST function is responsible for logging in a user
- The PUT function is responsible for creating a user account and subsequently logging in
- The PATCH function is reponsible for user account deletion
### Data Upload
This is a module that deals with uploading of data to the model. It deals with the creation of user projects, which can be used for a detection or a classification model. It also is responsible for the uploading of image and label data to the system, as well as updating the class list for the project, i.e. what objects it can detect.
#### UploadProjectAPI
This specific API handles the uploading, updating, and deletion of projects.
- GET retrieves all of the projects a user has
- POST retrieves specific information for a single project
- PUT places a new project into the database
- PATCH deletes a project if api_token is valid
#### UploadDataAPI
This specific API handles the uploading, updating, and deletion of data.
- POST and PUT both place a data point into the system
- PATCH deletes a data point if api_token and project_name are valid
#### UploadClassAPI
This specific API handles the uploading, updating, and deletion of classes.
- POST and PUT both place a class list into the system for the current project specified
- PATCH deletes a class list if api_token and project_name are valid
### Training
This module is used in order to train a model. If a project folder is complete enough, and the correct parameters are specified, this endpoint will train a machine learning model for the given images and class data.
- PUT begins the training of the model, and this information updates the project data in the database for the next time any project data is read
### Model Publishing
This module is used to publish a previously trained model within a project.
If a model is published, other users are able to find the model and make an inference using it. A user may only infer on their own models if they are published as well.
### Inference
This module is used to utilized a previously trained and currently published model. Users can infer on either their own or someone elses published machine learning models
