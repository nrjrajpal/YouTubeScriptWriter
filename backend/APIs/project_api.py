from flask import Blueprint, request, jsonify
from PseudoAgents import Project
from utils.exceptions import KeyNotFoundError,ProjectNotFoundError,UserNotFoundError,EmailMismatchError

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route('/createProject', methods=['POST'])
def createProject():
    try:
        # data = request.get_json()
        # userEmail = data.get('userEmail')
        # user = User(userEmail="temp@gmail.com")

        prj = Project(None)
        projectDetails=prj.createProject("ideatitle","ideadesc","temp5000@gmail.com")
        # "message":temp, 
        return jsonify({"projectDetails":projectDetails,"success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500

@project_blueprint.route('/deleteProject', methods=['POST'])
def deleteProject():
    try:
        # data = request.get_json()
        # userEmail = data.get('userEmail')
        # user = User(userEmail="temp@gmail.com")

        prj = Project(projectID="7000")
        prj.deleteProject()
        # "message":temp, 
        return jsonify({"success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500

@project_blueprint.route('/getIdeaTitle', methods=['POST'])
def getIdeaTitle():
    try:
        # data = request.get_json()
        # userEmail = data.get('userEmail')
        # user = User(userEmail="temp@gmail.com")

        prj = Project(projectID="11223")
        projectideatitle=prj.getProjectIdeaTitle()
        # "message":temp, 
        return jsonify({"projectideatitle":projectideatitle,"success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500
    
@project_blueprint.route('/getIdeaDescription', methods=['POST'])
def getIdeaDescription():
    try:
        # data = request.get_json()
        # userEmail = data.get('userEmail')
        # user = User(userEmail="temp@gmail.com")

        prj = Project(projectID="11223")
        projectIdeaDescription=prj.getProjectIdeaDescription()
        return jsonify({"ProjectIdeaDescription":projectIdeaDescription,"success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500
    
@project_blueprint.route('/getDateCreated', methods=['POST'])
def getDateCreated():
    try:
        # data = request.get_json()
        # userEmail = data.get('userEmail')
        # user = User(userEmail="temp@gmail.com")

        prj = Project(projectID="HNMKPIA")
        projectDateCreated=prj.getProjectDateCreated()
        return jsonify({"ProjectDateCreated":projectDateCreated,"success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500

@project_blueprint.route('/getOwnerEmail', methods=['POST'])
def getOwnerEmail():
    try:
        # data = request.get_json()
        # userEmail = data.get('userEmail')
        # user = User(userEmail="temp@gmail.com")

        prj = Project(projectID="HNMKPIA")
        projectOwnerEmail=prj.getProjectOwnerEmail()
        return jsonify({"Project Owner Email":projectOwnerEmail,"success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500

@project_blueprint.route('/getProjectDetails', methods=['POST'])
def getProjectDetails():
    try:
        # data = request.get_json()
        # userEmail = data.get('userEmail')
        # user = User(userEmail="temp@gmail.com")

        prj = Project(projectID="tGeCwKb")
        projectDetails=prj.getProjectDetails(projectID="HNMKPIA",userEmail="temp@gmail.com")
        return jsonify({"Project Details":projectDetails,"success": True}), 200
    except (KeyNotFoundError, ProjectNotFoundError, EmailMismatchError, UserNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500