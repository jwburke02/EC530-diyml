# EC530 - DIY Maching Learning
## API Descriptions
### Auth
This is a module that deals with creating accounts for users of this service. Additionally, it is responsible for lending out the authorization tokens needed by the other APIs.
### Data Upload
This is a module that deals with uploading of data to the model. It deals with the creation of user projects, which can be used for a detection or a classification model. It also is responsible for the uploading of image and label data to the system, as well as updating the class list for the project, i.e. what objects it can detect.
### Data Analysis
This module reports statistical information about the data points that are present within a project.
### Training
This module is used in order to train a model. If a project folder is complete enough, and the correct parameters are specified, this endpoint will train a machine learning model for the given images and class data.
### Model Publishing
This module is used to publish a previously trained model within a project.
### Inference
This module is used to utilized a previously trained and published model.
