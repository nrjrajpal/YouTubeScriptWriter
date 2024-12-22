from flask import Blueprint, request, jsonify
from PseudoAgents import YouTubeAgent
from utils.exceptions import KeyNotFoundError, ProjectNotFoundError

youtube_blueprint = Blueprint('youtube', __name__)

@youtube_blueprint.route('/fetchVideosFromYT', methods=['POST'])
def fetchVideosFromYT():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        ytagent = YouTubeAgent(projectID, userEmail)
        video_ids = ytagent.fetchVideosFromYT()
        urls = []
        for videoID in video_ids:
            urls.append("https://www.youtube.com/watch?v="+videoID)

        return jsonify({"message":"Successfully retrieved youtube video urls", "video_urls":urls, "success": True}), 200
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e, "success": False}), 500


@youtube_blueprint.route('/fetchVideoTranscript', methods=['POST'])
def fetchVideoTranscript():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        video_ids = data.get('video_ids')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        if not video_ids:
            return jsonify({"error": "Missing required field: video_ids", "success": False}), 400
        
        ytagent = YouTubeAgent(projectID, userEmail)
        transcripts = []
        for videoID in video_ids:
            transcripts.append(ytagent.fetchVideoTranscript(videoID = videoID))

        return jsonify({"message":"Successfully retrieved transcripts for youtube videos", "transcripts":transcripts, "success": True}), 200
    
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500


@youtube_blueprint.route('/fetchVideoMetadata', methods=['POST'])
def fetchVideoMetadata():
    try:
        pass
    except (KeyNotFoundError,ProjectNotFoundError) as e:
        return jsonify({"error": e.message, "success": False}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e, "success": False}), 500
  