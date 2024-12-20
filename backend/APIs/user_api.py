#THIS IS A TEMP FILE!
from flask import Blueprint, request, jsonify
from PseudoAgents import User
from utils.exceptions import KeyNotFoundError, UserNotFoundError

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/getChannelID', methods=['POST'])
def getChannelID():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        # user = User(userEmail="temp@gmail.com")

        user = User(userEmail)
        channelID = user.getChannelID()
        return jsonify({"channelID": channelID, "success": True}), 200
    except UserNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500
    
@user_blueprint.route('/setChannelID', methods=['POST'])
def setChannelID():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        channelID = data.get('channelID')
        
        user = User(userEmail)
        message = user.setChannelID(channelID)
        return jsonify({"message": message, "success": True}), 200
    except UserNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500

@user_blueprint.route('/getGroqAPIKey', methods=['POST'])
def getGroqAPIKey():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')

        user = User(userEmail)
        groqAPIKey = user.getGroqAPIKey()
        return jsonify({"groqAPIKey": groqAPIKey, "success": True}), 200
    except UserNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500

@user_blueprint.route('/setGroqAPIKey', methods=['POST'])
def setGroqAPIKey():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        groqAPIKey = data.get('groqAPIKey')
        
        user = User(userEmail)
        message = user.setGroqAPIKey(groqAPIKey)
        return jsonify({"message": message, "success": True}), 200
    except UserNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500