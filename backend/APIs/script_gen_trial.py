from flask import Blueprint, request, jsonify
from PseudoAgents import YouTubeAgent, ScriptAgent
from utils.exceptions import KeyNotFoundError, ProjectNotFoundError
from youtube_transcript_api import  TranscriptsDisabled, NoTranscriptFound


script_gen_trial_blueprint = Blueprint('script_gen_trial', __name__)

@script_gen_trial_blueprint.route('/generateScript', methods=['POST'])
def generateScript():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        scriptAgent = ScriptAgent(projectID, userEmail)
        
        # yt_summaries = []

        ytAgent = YouTubeAgent(projectID, userEmail)
        try:
            videoIDs = ytAgent.getVideoIDs()
            # videoTranscripts = []
            for videoID in videoIDs:
                # try:
                # videoTranscripts.append(ytAgent.fetchVideoTranscript(videoID))
                # except TranscriptsDisabled as td:
                #     videoTranscripts.append("Transcript is unavailable for this video")
                summary = scriptAgent.generateSummaryFromRawData(ytAgent.fetchVideoTranscript(videoID)[0:20000])
                scriptAgent.setYouTubeSummary(summary)
                print("\n\n\n\nSummary for video", videoID, ":\n", summary)
            # for videoTranscript in videoTranscripts:

        

            return jsonify({"message": "done", "success": True}), 200
        except KeyNotFoundError as ke:
            pass
        except (ProjectNotFoundError) as e:
            return jsonify({"error": e.message, "success": False}), 500
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}", "success": False}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}", "success": False}), 500