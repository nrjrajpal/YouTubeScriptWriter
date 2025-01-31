from utils.exceptions import KeyNotFoundError, UserNotFoundError, ProjectNotFoundError
from flask import Blueprint, jsonify, request
from PseudoAgents import SyntheticAgent,ResearcherAgent,YouTubeAgent,User, ScriptAgent
import ast
import json
import os

sources_blueprint = Blueprint('sources', __name__)

@sources_blueprint.route('/generateSearchQuery', methods=['POST'])
def generateSearchQuery():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            print("User email not found", userEmail)
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        ra = ResearcherAgent(projectID, userEmail)
        searchQuery = ra.generateSearchQuery()
        return jsonify({"success": True, "message": "Successfully generated search query.", "searchQuery":searchQuery})
        
    except (UserNotFoundError, KeyNotFoundError, ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        print("\n\n\nError: ", e)
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500
    

@sources_blueprint.route('/setSearchQuery', methods=['POST'])
def setSearchQuery():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        searchQuery = data.get('searchQuery')


        if not projectID:
            print("Project ID not found")
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        if not userEmail:
            print("User email not found")
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400
        
        if not searchQuery:
            print("Search Query not found")
            return jsonify({"error": "Query is not selected", "success": False}), 400
        
        ra=ResearcherAgent(projectID, userEmail)
        message = ra.setSearchQuery(searchQuery)
        return jsonify({"success": True, "message":message})
        
    except (UserNotFoundError, KeyNotFoundError, ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        print("\n\n\nError: ", e)
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500