from flask import Blueprint, request, jsonify
from PseudoAgents import YouTubeAgent, ScriptAgent, WebpageAgent, ResearchPaperAgent
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
        wpAgent = WebpageAgent(projectID, userEmail)
        rpAgent = ResearchPaperAgent(projectID, userEmail)
        try:
            ytSummariesOnDB = False
            try:
                ytSummaries = scriptAgent.getYouTubeSummaries()
                if ytSummaries:
                    ytSummariesOnDB = True
                    print("\n\nYTSummaries set\n\n")
                    videoIDs = ytAgent.getVideoIDs()
                    for ytSummary, videoID in zip(ytSummaries, videoIDs):
                        print(f"\n\n\n\nSummary for https://www.youtube.com/watch?v={videoID}:\n{ytSummary}")
            except KeyNotFoundError as ke:
                pass
            except:
                raise

            masterYTSummaryOnDB = False
            try:
                masterYTSummary = scriptAgent.getMasterYouTubeSummary()
                if masterYTSummary:
                    masterYTSummaryOnDB = True
                    print("\n\nMasterYTSummary set\n\n")
                    print(f"\n\n\n\nMaster YouTube Summary:\n{masterYTSummary}")
            except KeyNotFoundError as ke:
                pass
            except:
                raise

            if not ytSummariesOnDB:
                print("\n\nYTSummaries not set\n\n")
                videoIDs = ytAgent.getVideoIDs()
                ytSummaries = []
                for videoID in videoIDs:
                    # try:
                    # videoTranscripts.append(ytAgent.fetchVideoTranscript(videoID))
                    # except TranscriptsDisabled as td:
                    #     videoTranscripts.append("Transcript is unavailable for this video")
                    print(f"\n\n\n\nFetching transctpit for https://www.youtube.com/watch?v={videoID}")
                    transcript = ytAgent.fetchVideoTranscript(videoID)
                    if transcript == "Transcript not available":
                        continue
                    print(f"Generating YT summary")
                    ytSummary = scriptAgent.generateSummaryFromRawData(transcript[0:20000])
                    scriptAgent.setYouTubeSummary(ytSummary)
                    print(f"\n\n\n\nSummary for https://www.youtube.com/watch?v={videoID}:\n{ytSummary}")
                # for videoTranscript in videoTranscripts:
            
            if not masterYTSummaryOnDB:
                print("\n\nMasterYTSummary not set\n\n")
                ytSummaries = scriptAgent.getYouTubeSummaries()
                print(f"Generating master YT summary")
                masterYTSummary = scriptAgent.generateSummaryFromSummaries(ytSummaries)
                scriptAgent.setMasterYouTubeSummary(masterYTSummary)
                print(f"\n\n\n\nMaster YouTube Summary:\n{masterYTSummary}")

            wpSummariesOnDB = False
            try:
                wpSummaries = scriptAgent.getWebPageSummaries()
                if wpSummaries:
                    wpSummariesOnDB = True
                    print("\n\nwpSummaries set\n\n")
                    webPageData = wpAgent.getWebPageData()
                    webPageURLs = [webPage["webpage_url"] for webPage in webPageData if "webpage_url" in webPage]
                    for wpSummary, webPageURL in zip(wpSummaries, webPageURLs):
                        print(f"\n\n\n\nSummary for {webPageURL}:\n{wpSummary}")
            except KeyNotFoundError as ke:
                pass
            except:
                raise

            masterWPSummaryOnDB = False
            try:
                masterWPSummary = scriptAgent.getMasterWebPageSummary()
                if masterWPSummary:
                    masterWPSummaryOnDB = True
                    print("\n\nMasterWPSummary set\n\n")
                    print(f"\n\n\n\nMaster Web Page Summary:\n{masterWPSummary}")
            except KeyNotFoundError as ke:
                pass
            except:
                raise

            if not wpSummariesOnDB:
                print("\n\nwpSummaries not set\n\n")
                webPageData = wpAgent.getWebPageData()
                webPageURLs = [webPage["webpage_url"] for webPage in webPageData if "webpage_url" in webPage]
                wpSummaries = []
                for webPageURL in webPageURLs:
                    print(f"\n\n\n\nFetching raw content for {webPageURL}")
                    rawContent = wpAgent.fetchWebPageRawContent(webPageURL)
                    print(f"Generating WP summary")
                    wpSummary = scriptAgent.generateSummaryFromRawData(rawContent[0:20000])
                    scriptAgent.setWebPageSummary(wpSummary)
                    print(f"\n\n\n\nSummary for {webPageURL}:\n{wpSummary}")
            
            if not masterWPSummaryOnDB:
                print("\n\nMasterWPSummary not set\n\n")
                wpSummaries = scriptAgent.getWebPageSummaries()
                print(f"Generating master WP summary")
                masterWPSummary = scriptAgent.generateSummaryFromSummaries(wpSummaries)
                scriptAgent.setMasterWebPageSummary(masterWPSummary)
                print(f"\n\n\n\nMaster WebPage Summary:\n{masterWPSummary}")

            rpSummariesOnDB = False
            try:
                rpSummaries = scriptAgent.getResearchPaperSummaries()
                if rpSummaries:
                    rpSummariesOnDB = True
                    print("\n\nrpSummaries set\n\n")
                    researchPaperData = rpAgent.getResearchPaperUrlsAndMetadata()
                    researchPaperURLs = [researchPaper["research_paper_url"] for researchPaper in researchPaperData if "research_paper_url" in researchPaper]
                    for rpSummary, researchPaperURL in zip(rpSummaries, researchPaperURLs):
                        print(f"\n\n\n\nSummary for {researchPaperURL}:\n{rpSummary}")
            except KeyNotFoundError as ke:
                pass
            except:
                raise

            masterRPSummaryOnDB = False
            try:
                masterRPSummary = scriptAgent.getMasterResearchPaperSummary()
                if masterRPSummary:
                    masterRPSummaryOnDB = True
                    print("\n\nMasterRPSummary set\n\n")
                    print(f"\n\n\n\nMaster Research Paper Summary:\n{masterRPSummary}")
            except KeyNotFoundError as ke:
                pass
            except:
                raise

            if not rpSummariesOnDB:
                print("\n\nrpSummaries not set\n\n")
                researchPaperData = rpAgent.getResearchPaperUrlsAndMetadata()
                researchPaperURLs = [researchPaper["research_paper_url"] for researchPaper in researchPaperData if "research_paper_url" in researchPaper]
                rpSummaries = []
                for researchPaperURL in researchPaperURLs:
                    print(f"\n\n\n\nFetching raw content for {researchPaperURL}")
                    rawContent = rpAgent.fetchResearchPaperContent(researchPaperURL)
                    print(f"Generating RP summary")
                    rpSummary = scriptAgent.generateSummaryFromRawData(rawContent[0:20000])
                    scriptAgent.setResearchPaperSummary(rpSummary)
                    print(f"\n\n\n\nSummary for {researchPaperURL}:\n{rpSummary}")
            
            if not masterRPSummaryOnDB:
                print("\n\nMasterRPSummary not set\n\n")
                rpSummaries = scriptAgent.getResearchPaperSummaries()
                print(f"Generating master RP summary")
                masterRPSummary = scriptAgent.generateSummaryFromSummaries(rpSummaries)
                scriptAgent.setMasterResearchPaperSummary(masterRPSummary)
                print(f"\n\n\n\nMaster Research Paper Summary:\n{masterRPSummary}")

            return jsonify({"message": "done", "success": True}), 200
        except KeyNotFoundError as ke:
            pass
        except (ProjectNotFoundError) as e:
            return jsonify({"error": e.message, "success": False}), 500
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}", "success": False}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}", "success": False}), 500