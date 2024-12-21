from utils.exceptions import KeyNotFoundError, UserNotFoundError, ProjectNotFoundError
from flask import Blueprint, jsonify, request
from PseudoAgents import SyntheticAgent,ResearcherAgent,YouTubeAgent,User, ScriptAgent
import ast
import json
import os

select_questions_blueprint = Blueprint('select_questions', __name__)

@select_questions_blueprint.route('/generateQuestionsBasedOnTitle', methods=['POST'])
def generateQuestionsBasedOnTitle():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        sa = ScriptAgent(projectID, userEmail)
        questions = sa.generateQuestionsBasedOnTitle()
        return jsonify({"message": "Successfully generated questions.", "generated_questions":questions})
        
    except (UserNotFoundError, KeyNotFoundError, ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        print("\n\n\nError: ", e)
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500
    

@select_questions_blueprint.route('/setSelectedQuestions', methods=['POST'])
def setSelectedQuestions():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        selectedQuestions = data.get('selectedQuestions')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        if not selectedQuestions:
            return jsonify({"error": "Questions are not selected", "success": False}), 400
        
        sa=ScriptAgent(projectID, userEmail)
        message = sa.setSelectedQuestions(selectedQuestions)
        sa.updateProjectState('selectSources')
        return jsonify({"Message":message})
        
    except (UserNotFoundError, KeyNotFoundError, ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        print("\n\n\nError: ", e)
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500