#Framework for python web
import requests
import json
import flask
from flask import request
from flask_api import status

#The Flask app
app = flask.Flask(__name__)

#Define the routes
@app.route('/', methods=['GET'])
def home():
    return "<h1>Students</h1>"

def createstudentlist():
    student = dict()
    student["jc1001"] = {
        "no" : "jc1001",
        "name" : "John Doe",
        "grade" : 10,
        "subjects" : {
            "Math" : 93,
            "English" : 82,
            "French" : 78,
            "History" : 91
        }
    }
    student["jc1002"] = {
        "no" : "jc1002",
        "name" : "Bob James",
        "grade" : 12,
        "subjects" : {
            "Geography" : 91,
            "English" : 88,
            "Science" : 86,
            "History" : 81
        }
    }
    student["jc1003"] = {
        "no" : "jc1003",
        "name" : "Rick Paul",
        "grade" : 11,
        "subjects" : {
            "Physics" : 99,
            "Chemistry" : 89,
            "Math" : 88,
            "English" : 81
        }
    }

    return student
    
#Searching student by their id
@app.route('/student/<id>', methods=['GET'])
def student_by_id(id):
    response = {}
    if id in studentlist:
        response['error'] = False
        response['id'] = id
        response['student'] = studentlist[id]
        return response, status.HTTP_200_OK
    else:
        response['error'] = True
        response['message'] = 'id is not within the range'
        return response, status.HTTP_404_NOT_FOUND

#adding a student to dictionary
@app.route('/student/add/', methods=["POST"])
def add_student():
    response = {}
    payload = request.get_json()
    id = payload["no"]
    if id in studentlist:
        response['error'] = True
        response['message'] = 'id is in the database.'
        return response, status.HTTP_412_PRECONDITION_FAILED
    else:
        studentlist[id] = payload
        response['error'] = False
        response['id'] = id
        response['student'] = studentlist[id]
        return response, status.HTTP_200_OK

#updating a student
@app.route('/student/update/<id>', methods=["POST"])
def update_student(id):
    response = {}
    if id in studentlist:
        payload = request.get_json()
        studentlist[id] = payload
        response['error'] = False
        response['id'] = id
        response['student'] = studentlist[id]
    else:
        response['error'] = True
        response['message'] = 'id is not in the database'
    return response

#updating a students score
@app.route('/student/update/subject/<id>', methods=["POST"])
def update_studentgrade(id):
    response = {}
    if id in studentlist:
        payload = request.get_json()
        studentlist[id]["subjects"] = payload
        response['error'] = False
        response['id'] = id
        response['student'] = studentlist[id]
    else:
        response['error'] = True
        response['message'] = 'id is not in the database'
    return response

@app.route('/students', methods=['GET'])
def students():
    response = ""
    for s in studentlist:
        id = studentlist[s]["no"]
        name = studentlist[s]["name"]
        response = response + "<b>" + id + "</b> &emsp;&emsp;&emsp;" + name + "<br>"
    
    return response
        
    

studentlist = createstudentlist()

app.run()