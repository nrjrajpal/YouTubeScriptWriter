from flask import Blueprint, request, jsonify
from PseudoAgents import WebpageAgent
from utils.exceptions import KeyNotFoundError,ProjectNotFoundError

webpage_blueprint = Blueprint('webpage', __name__)

@webpage_blueprint.route('/fetchWebPagesFromWeb', methods=['POST'])
def fetchWebPagesFromWeb():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        webagent = WebpageAgent(projectID, userEmail)
        webpage_content = webagent.fetchWebPagesFromWeb()

        return jsonify({"message":"Successfully retrieved webpages", "webpage content":webpage_content, "success": True}), 200
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        print("Error in fetchWebPagesFromWeb",e)
        return jsonify({"error": f"An error occurred: {e}", "success": False}), 500
    
@webpage_blueprint.route('/setWebPageData', methods=['POST'])
def setWebpageData():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        webPageData = data.get('webPageData')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        if not webPageData:
            return jsonify({"error": "Missing required field: webPageData", "success": False}), 400
        
        webagent = WebpageAgent(projectID, userEmail)
        message = webagent.setWebpageData(webPageData)

        return jsonify({"message":message, "success": True}), 200
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}", "success": False}), 500


@webpage_blueprint.route('/getWebPageData', methods=['POST'])
def getWebPageData():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        webagent = WebpageAgent(projectID, userEmail)
        webPageData = webagent.getWebPageData()

        return jsonify({"message":"Successfully retrieved webpages", "webPageData": webPageData, "success": True}), 200
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}", "success": False}), 500


@webpage_blueprint.route('/fetchWebPageRawContent', methods=['POST'])
def fetchWebPageRawContent():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        webPageURL = data.get('webPageURL')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        if not webPageURL:
            return jsonify({"error": "Missing required field: webpageURL", "success": False}), 400
        
        webagent = WebpageAgent(projectID, userEmail)
        webPageData = webagent.fetchWebPageRawContent(webPageURL)

        return jsonify({"message":"Successfully retrieved webpage's raw content", "webpageRawContent": webPageData, "success": True}), 200
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}", "success": False}), 500
    
