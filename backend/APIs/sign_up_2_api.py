from flask import Blueprint, jsonify

sign_up_2_blueprint = Blueprint('sign_up_2', __name__)

@sign_up_2_blueprint.route('/setAPIKeysAndChannelID', methods=['POST'])
def setAPIKeysAndChannelID():
    try:
        return jsonify({"pass":"pass", "success": True})
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False})
