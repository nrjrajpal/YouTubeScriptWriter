from flask import Blueprint, request, jsonify
from PseudoAgents import Project
from utils.exceptions import KeyNotFoundError, ProjectNotFoundError, UserNotFoundError, EmailMismatchError

project_blueprint = Blueprint('project', __name__)

@project_blueprint.route('/createProject', methods=['POST'])
def createProject():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        ideaTitle = data.get('ideaTitle')
        ideaDescription = data.get('ideaDescription')
        # user = User(userEmail="temp@gmail.com")
        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400
        
        if not ideaTitle:
            return jsonify({"error": "Missing required field: ideaTitle", "success": False}), 400
        
        if not ideaDescription:
            return jsonify({"error": "Missing required field: ideaDescription", "success": False}), 400
        prj = Project(None)
        projectDetails=prj.createProject(ideaTitle,ideaDescription,userEmail)
        # "message":temp, 
        return jsonify({"project":projectDetails,"success": True, "message": "Project created successfully"}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500

@project_blueprint.route('/api/checkProject/<project_id>', methods=['POST'])
def check_project(project_id):
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        project = Project(projectID=project_id)
        project.getProjectDetails(userEmail)
        return jsonify({"exists": True, "project_id": project_id}), 200
    except ProjectNotFoundError as e:
        return jsonify({"exists": False, "error": "Project not found"}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500

@project_blueprint.route('/api/getNextStage/<project_id>', methods=['GET'])
def get_next_stage(project_id):
    try:
        project = Project(projectID=project_id)
        next_stage = project.getProjectNextState()
        return jsonify({"next_stage": next_stage}), 200
    except KeyNotFoundError as e:
        return jsonify({"exists": False, "error": e}), 404
    except ProjectNotFoundError as e:
        return jsonify({"exists": False, "error": e}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500

@project_blueprint.route('/deleteProject', methods=['DELETE'])
def deleteProject():
    try:
        data = request.get_json()
        print("Deletion: ", data)
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        # user = User(userEmail="temp@gmail.com")

        project = Project(projectID)
        response = project.deleteProject(projectID, userEmail)
        # prj.deleteProject()
        # "message":temp, 
        return jsonify({"success": True, "message": response["message"]}), 200
    except (KeyNotFoundError, UserNotFoundError, ProjectNotFoundError) as e:   
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500

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
        return jsonify({"error": e, "success": False}), 500
    
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
        return jsonify({"error": e, "success": False}), 500
    
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
        return jsonify({"error": e, "success": False}), 500

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
        return jsonify({"error": e, "success": False}), 500

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
        return jsonify({"error": e, "success": False}), 500