from flask import Blueprint, request, jsonify
from PseudoAgents import CustomDataAgent
from utils.exceptions import KeyNotFoundError, ProjectNotFoundError

custom_blueprint = Blueprint('custom', __name__)

@custom_blueprint.route('/setCustomData', methods=['POST'])
def setCustomData():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        customData=data.get('customData')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        if not customData:
            return jsonify({"error": "Missing required field: customData", "success": False}), 400
        
        customagent = CustomDataAgent(projectID, userEmail)
        message = customagent.setCustomData(customData)

        return jsonify({"message":message, "success": True}), 200
    
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500
    

@custom_blueprint.route('/getCustomData', methods=['POST'])
def getCustomData():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
                    
        customagent = CustomDataAgent(projectID, userEmail)
        customData = customagent.getCustomData()

        return jsonify({"message":"Successfully retrieved custom Data", "customData": customData, "success": True}), 200
    
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500
