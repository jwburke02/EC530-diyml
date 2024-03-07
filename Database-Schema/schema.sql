/* Running this would create database for the project */
/* Create USER table to store users */
CREATE TABLE user (
    uid INT PRIMARY KEY,
    username TEXT NOT NULL,
    hashed_pass TEXT NOT NULL,
    api_token TEXT NOT NULL
);
/* Create PROJECT table to store projects */
CREATE TABLE project (
    pid INT PRIMARY KEY,
    uid INT NOT NULL,
    project_name TEXT NOT NULL,
    type TEXT NOT NULL,
    current_api TEXT NOT NULL,
    is_published BOOLEAN NOT NULL
);
/* Create CLASS table to store classes the API knows */
CREATE TABLE class (
    cid INT PRIMARY KEY,
    class_name TEXT NOT NULL
);
/* Create DATAPOINT table to store data points for projects */
CREATE TABLE datapoint (
    did INT PRIMARY KEY,
    pid INT NOT NULL,
    name TEXT NOT NULL,
    img_data TEXT NOT NULL,
    label_data TEXT NOT NULL
);
/* Create PROJECTCLASS table to store relations between projects + classes */
CREATE TABLE projectclass (
    pcid INT PRIMARY KEY,
    pid INT NOT NULL,
    cid INT NOT NULL
)
