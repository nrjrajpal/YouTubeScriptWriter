from flask import Blueprint, request, jsonify
from utils.exceptions import KeyNotFoundError, UserNotFoundError
from PseudoAgents import User

sign_up_2_blueprint = Blueprint('sign_up_2', __name__)

# @sign_up_2_blueprint.route('/setAPIKeysAndChannelID', methods=['POST'])
# def setAPIKeysAndChannelID():
@sign_up_2_blueprint.route('/setAPIKeys', methods=['POST'])
def setAPIKeys():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        userID = data.get('userID')
        groqAPIKey = data.get('groqAPIKey')
        serperAPIKey = data.get('serperAPIKey')
        tavilyAPIKey = data.get('tavilyAPIKey')
        # channelID = data.get('channelID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400
        
        if not userID:
            return jsonify({"error": "Missing required field: userID", "success": False}), 400
        
        if not groqAPIKey:
            return jsonify({"error": "Missing required field: groqAPIKey", "success": False}), 400
        
        if not serperAPIKey:
            return jsonify({"error": "Missing required field: serperAPIKey", "success": False}), 400
        
        if not tavilyAPIKey:
            return jsonify({"error": "Missing required field: tavilyAPIKey", "success": False}), 400

        user = User(userEmail)
        user.createUser(userID)
        user.setGroqAPIKey(groqAPIKey)
        user.setSerperAPIKey(serperAPIKey)
        user.setTavilyAPIKey(tavilyAPIKey)

        # if channelID:
        #     user.setChannelID(channelID)

        return jsonify({"message": "Data set successfully", "success": True}), 200
    except UserNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        print("\n\n\nError: ", e)
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500
