from flask import Blueprint, request, jsonify
from PseudoAgents import ResearchPaperAgent
from utils.exceptions import KeyNotFoundError,ProjectNotFoundError

researchpaper_blueprint = Blueprint('researchpaper', __name__)

@researchpaper_blueprint.route('/fetchfromweb', methods=['POST'])
def fetchfromweb():
    try:
        # data = request.get_json()
        # userEmail = data.get('userEmail')
        # userEmail="temp1000@gmail.com"
        rspragent = ResearchPaperAgent(projectID="12345")
        result=rspragent.fetchResearchPaperFromWeb()
        # rspragent.setResearchPaperUrlsAndMetadata(result)
        return jsonify({"Response":result,"success": True}), 200
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500
    
@researchpaper_blueprint.route('/fetchcontent', methods=['POST'])
def fetchcontent():
    try:
        data = request.get_json()
        researchPaperURL = data.get('researchPaperURL')
        print(researchPaperURL)
        rspragent = ResearchPaperAgent(projectID="12345")
        result=rspragent.fetchResearchPaperContent(researchPaperURL)
        # rspragent.setResearchPaperUrlsAndMetadata(result)
        return jsonify({"Response":result,"success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500
    
@researchpaper_blueprint.route('/setResearchPaperData', methods=['POST'])
def setResearchPaperData():
    try:
        data = request.get_json()
        researchPaperData = data.get('researchPaperData')
        print(researchPaperData)
        rspragent = ResearchPaperAgent(projectID="12345")
        result=rspragent.setResearchPaperUrlsAndMetadata(researchPaperData)
        # rspragent.setResearchPaperUrlsAndMetadata(result)
        return jsonify({"Response":result,"success": True}), 200
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500
    
@researchpaper_blueprint.route('/getResearchPaperData', methods=['POST'])
def getResearchPaperData():
    try:
        # data = request.get_json()
        # researchPaperData = data.get('researchPaperData')
        # print(researchPaperData)
        rspragent = ResearchPaperAgent(projectID="12345")
        result=rspragent.getResearchPaperUrlsAndMetadata()
        return jsonify({"researchPaperData": result, "success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500

