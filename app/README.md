# TTM4115 Semester Project
### NB: This folder contains the application aside from what is hosted at Heroku. 
### The code for the video and chat service hosted on Heroku is provided in the folder named CallService
### NB: The database on Azure has been turned off now since the project is completed.

## Dependencies
### Motion detection
- tensorflow
- opencv-python
- mediapipe

### Game
- pygame
- numpy

### Database service
- mysql-connector-python

### Controllers and other components
- appJar
- stmpy
- paho.mqtt.client
- threading

## To run the project
- All the dependencies must be installed.
- Some places in the code a machine specific path is used. These must be updated to what is accurate on the given machine.
- Choose whether to use the application as a Home office device or as an Office device. 
  - If you choose as a home office device run the HomeOfficeApp.py file. 
  - If you wish to run the project as an office device run the OfficeApp.py file.
