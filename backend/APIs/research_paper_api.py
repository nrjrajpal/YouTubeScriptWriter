from flask import Blueprint, request, jsonify
from PseudoAgents import ResearchPaperAgent
from utils.exceptions import KeyNotFoundError,ProjectNotFoundError

researchpaper_blueprint = Blueprint('researchpaper', __name__)

@researchpaper_blueprint.route('/setResearchPaperData', methods=['POST'])
def setResearchPaperData():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        researchPaperData = data.get('researchPaperData')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        if not researchPaperData:
            return jsonify({"error": "Missing required field: researchPaperData", "success": False}), 400
            
        ytagent = ResearchPaperAgent(projectID, userEmail)
        message = ytagent.setResearchPaperData(researchPaperData)

        return jsonify({"message":message, "success": True}), 200
    
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500


@researchpaper_blueprint.route('/fetchResearchPaperFromWeb', methods=['POST'])
def fetchResearchPaperFromWeb():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        rspragent = ResearchPaperAgent(projectID, userEmail)
        research_papers = rspragent.fetchResearchPaperFromWeb()

        # rspragent.setResearchPaperUrlsAndMetadata(result)
        return jsonify({"message":"Successfully retrieved research papers", "research papers":research_papers,"success": True}), 200
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}", "success": False}), 500
    
@researchpaper_blueprint.route('/fetchResearchPaperContent', methods=['POST'])
def fetchResearchPaperContent():
    try:
        data = request.get_json()
        userEmail = "ishanvyavahare+real@gmail.com" #data.get('userEmail')
        projectID = "Dx1qIVN" #data.get('projectID')
        researchPaperData = data.get('researchPaperData')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        if not researchPaperData:
            return jsonify({"error": "Missing required field: researchPaperData", "success": False}), 400
        
        rspragent = ResearchPaperAgent(projectID, userEmail)

        research_papers_raw_content = []
        for rpData in researchPaperData:
            research_papers_raw_content.append(rspragent.fetchResearchPaperContent(rpData["paper_url"])[0:200])

        # rspragent.setResearchPaperUrlsAndMetadata(result)
        return jsonify({"message": "Successfully retrieved research papers' raw content", "research_papers_raw_content":research_papers_raw_content,"success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500
    

@researchpaper_blueprint.route('/getResearchPaperUrlsAndMetadata', methods=['POST'])
def getResearchPaperUrlsAndMetadata():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        researchPaperURLS = data.get('researchPaperURLS')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        rspragent = ResearchPaperAgent(projectID, userEmail)
        result=rspragent.getResearchPaperUrlsAndMetadata()
        return jsonify({"researchPaperData": result, "success": True}), 200
    except KeyNotFoundError as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500
    

# @researchpaper_blueprint.route('/setResearchPaperData', methods=['POST'])
# def setResearchPaperData():
#     try:
#         data = request.get_json()
#         researchPaperData = data.get('researchPaperData')
#         print(researchPaperData)
#         rspragent = ResearchPaperAgent(projectID="12345")
#         result=rspragent.setResearchPaperUrlsAndMetadata(researchPaperData)
#         # rspragent.setResearchPaperUrlsAndMetadata(result)
#         return jsonify({"Response":result,"success": True}), 200
#     except (KeyNotFoundError,ProjectNotFoundError) as e:
#         return jsonify({"error": e.message, "success": False}), 404
#     except Exception as e:
#         return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500
    

