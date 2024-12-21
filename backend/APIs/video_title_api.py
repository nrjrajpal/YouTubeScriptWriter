from flask import Blueprint, request, jsonify
from utils.exceptions import KeyNotFoundError, UserNotFoundError, ProjectNotFoundError
from PseudoAgents import User
from PseudoAgents import SyntheticAgent

video_title_blueprint = Blueprint('video_title', __name__)

# @video_title_blueprint.route('/setAPIKeysAndChannelID', methods=['POST'])
# def setAPIKeysAndChannelID():
@video_title_blueprint.route('/generateVideoTitles', methods=['POST'])
def generateVideoTitles():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        syntheticAgent = SyntheticAgent(projectID, userEmail)
        titles = syntheticAgent.generateVideoTitles()        
        
        return jsonify({"success": True, "titles": titles}), 200
    except (UserNotFoundError, KeyNotFoundError, ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        print("\n\n\nError: ", e)
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500
    

@video_title_blueprint.route('/setVideoTitle', methods=['POST'])
def setVideoTitle():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        videoTitle = data.get('videoTitle')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400

        if not videoTitle:
            return jsonify({"error": "Missing required field: videoTitle", "success": False}), 400

        syntheticAgent = SyntheticAgent(projectID, userEmail)
        message = syntheticAgent.setVideoTitle(videoTitle)    
        syntheticAgent.updateProjectState('selectQuestions')    
        
        return jsonify({"success": True, "message": message}), 200
    except (UserNotFoundError, KeyNotFoundError, ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        print("\n\n\nError: ", e)
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500
