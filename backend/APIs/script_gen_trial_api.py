from flask import Blueprint, request, jsonify
from PseudoAgents import YouTubeAgent, ScriptAgent, WebpageAgent, ResearchPaperAgent, CustomDataAgent
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
        cdAgent = CustomDataAgent(projectID, userEmail)
        try:
            ytSummariesOnDB = False
            try:
                ytSummaries = scriptAgent.getYouTubeSummaries()
                if ytSummaries:
                    ytSummariesOnDB = True
                    print("\n\nYTSummaries set\n\n")
                    videoIDs = ytAgent.getVideoIDs()
                    for ytSummary, videoID in zip(ytSummaries, videoIDs):
                        print(f"\n\n\nSummary for https://www.youtube.com/watch?v={videoID}:\n{ytSummary}")
            except KeyNotFoundError:
                pass
            except:
                raise

            masterYTSummaryOnDB = False
            try:
                masterYTSummary = scriptAgent.getMasterYouTubeSummary()
                if masterYTSummary:
                    masterYTSummaryOnDB = True
                    print(f"\n\nMasterYTSummary set\n\n\nMaster YouTube Summary:\n{masterYTSummary}")
            except KeyNotFoundError:
                pass
            except:
                raise

            if not ytSummariesOnDB:
                try:
                    videoIDs = ytAgent.getVideoIDs()
                    print("\n\nYTSummaries not set\n\n")
                    ytSummaries = []
                    for videoID in videoIDs:
                        # try:
                        # videoTranscripts.append(ytAgent.fetchVideoTranscript(videoID))
                        # except TranscriptsDisabled as td:
                        #     videoTranscripts.append("Transcript is unavailable for this video")
                        print(f"\n\n\nFetching transctpit for https://www.youtube.com/watch?v={videoID}")
                        transcript = ytAgent.fetchVideoTranscript(videoID)
                        if transcript == "Transcript not available":
                            continue
                        print(f"Generating YT summary")
                        ytSummary = scriptAgent.generateSummaryFromRawData(transcript[0:20000])
                        scriptAgent.setYouTubeSummary(ytSummary)
                        print(f"\n\nSummary for https://www.youtube.com/watch?v={videoID}:\n{ytSummary}")
                    # for videoTranscript in videoTranscripts:
                except KeyNotFoundError:
                    pass
                except:
                    raise

            if not masterYTSummaryOnDB:
                try:

                    ytSummaries = scriptAgent.getYouTubeSummaries()
                    print("\n\nMasterYTSummary not set\n\nGenerating master YT summary")
                    masterYTSummary = scriptAgent.generateSummaryFromSummaries(ytSummaries)
                    scriptAgent.setMasterYouTubeSummary(masterYTSummary)
                    print(f"\n\n\nMaster YouTube Summary:\n{masterYTSummary}")
                except KeyNotFoundError:
                    pass
                except:
                    raise

            wpSummariesOnDB = False
            try:
                wpSummaries = scriptAgent.getWebPageSummaries()
                if wpSummaries:
                    wpSummariesOnDB = True
                    print("\n\nwpSummaries set\n\n")
                    webPageData = wpAgent.getWebPageData()
                    webPageURLs = [webPage["webpage_url"] for webPage in webPageData if "webpage_url" in webPage]
                    for wpSummary, webPageURL in zip(wpSummaries, webPageURLs):
                        print(f"\n\n\nSummary for {webPageURL}:\n{wpSummary}")
            except KeyNotFoundError:
                pass
            except:
                raise

            masterWPSummaryOnDB = False
            try:
                masterWPSummary = scriptAgent.getMasterWebPageSummary()
                if masterWPSummary:
                    masterWPSummaryOnDB = True
                    print(f"\n\nMasterWPSummary set\n\nMaster Web Page Summary:\n{masterWPSummary}")
            except KeyNotFoundError:
                pass
            except:
                raise

            if not wpSummariesOnDB:
                try:

                    webPageData = wpAgent.getWebPageData()
                    print("\n\nwpSummaries not set\n\n")
                    webPageURLs = [webPage["webpage_url"] for webPage in webPageData if "webpage_url" in webPage]
                    wpSummaries = []
                    for webPageURL in webPageURLs:
                        print(f"\n\n\nFetching raw content for {webPageURL}")
                        rawContent = wpAgent.fetchWebPageRawContent(webPageURL)
                        print(f"Generating WP summary")
                        wpSummary = scriptAgent.generateSummaryFromRawData(rawContent[0:20000])
                        scriptAgent.setWebPageSummary(wpSummary)
                        print(f"\n\n\nSummary for {webPageURL}:\n{wpSummary}")
                except KeyNotFoundError:
                    pass
                except:
                    raise

            if not masterWPSummaryOnDB:
                try:
                    wpSummaries = scriptAgent.getWebPageSummaries()
                    print("\n\nMasterWPSummary not set\n\nGenerating master WP summary")
                    masterWPSummary = scriptAgent.generateSummaryFromSummaries(wpSummaries)
                    scriptAgent.setMasterWebPageSummary(masterWPSummary)
                    print(f"\n\nMaster WebPage Summary:\n{masterWPSummary}")
                except KeyNotFoundError:
                    pass
                except:
                    raise

            rpSummariesOnDB = False
            try:
                rpSummaries = scriptAgent.getResearchPaperSummaries()
                if rpSummaries:
                    rpSummariesOnDB = True
                    print("\n\nrpSummaries set\n\n")
                    researchPaperData = rpAgent.getResearchPaperUrlsAndMetadata()
                    researchPaperURLs = [researchPaper["research_paper_url"] for researchPaper in researchPaperData if "research_paper_url" in researchPaper]
                    for rpSummary, researchPaperURL in zip(rpSummaries, researchPaperURLs):
                        print(f"\n\n\nSummary for {researchPaperURL}:\n{rpSummary}")
            except KeyNotFoundError:
                pass
            except:
                raise

            masterRPSummaryOnDB = False
            try:
                masterRPSummary = scriptAgent.getMasterResearchPaperSummary()
                if masterRPSummary:
                    masterRPSummaryOnDB = True
                    print(f"\n\nMasterRPSummary set\n\nMaster Research Paper Summary:\n{masterRPSummary}")
            except KeyNotFoundError:
                pass
            except:
                raise

            if not rpSummariesOnDB:
                try:

                    researchPaperData = rpAgent.getResearchPaperUrlsAndMetadata()
                    print("\n\nrpSummaries not set\n\n")
                    researchPaperURLs = [researchPaper["research_paper_url"] for researchPaper in researchPaperData if "research_paper_url" in researchPaper]
                    rpSummaries = []
                    for researchPaperURL in researchPaperURLs:
                        print(f"\n\n\nFetching raw content for {researchPaperURL}")
                        rawContent = rpAgent.fetchResearchPaperContent(researchPaperURL)
                        print(f"Generating RP summary")
                        rpSummary = scriptAgent.generateSummaryFromRawData(rawContent[0:20000])
                        scriptAgent.setResearchPaperSummary(rpSummary)
                        print(f"\n\n\nSummary for {researchPaperURL}:\n{rpSummary}")
                except KeyNotFoundError:
                    pass
                except:
                    raise
            
            if not masterRPSummaryOnDB:
                try: 
                    rpSummaries = scriptAgent.getResearchPaperSummaries()
                    print("\n\nMasterRPSummary not set\n\nGenerating master RP summary")
                    masterRPSummary = scriptAgent.generateSummaryFromSummaries(rpSummaries)
                    scriptAgent.setMasterResearchPaperSummary(masterRPSummary)
                    print(f"\n\n\nMaster Research Paper Summary:\n{masterRPSummary}")
                except KeyNotFoundError:
                    pass
                except:
                    raise
        
            cdSummaryOnDB = False
            try:
                cdSummary = scriptAgent.getCustomDataSummary()
                if cdSummary:
                    cdSummaryOnDB = True
                    print(f"\n\ncdSummary set\n\nCustom Data Summary:\n{cdSummary}")
            except KeyNotFoundError:
                pass
            except:
                raise

            if not cdSummaryOnDB:
                try:
                    customData = cdAgent.getCustomData()
                    print("\n\nCustom Data Summary not set\n\nGenerating CD summary")
                    cdSummary = scriptAgent.generateSummaryFromRawData(customData)
                    scriptAgent.setCustomDataSummary(cdSummary)
                    print(f"\n\n\nCustom Data Summary:\n{cdSummary}")
                except KeyNotFoundError:
                    pass
                except:
                    raise
            
            masterSummaryOnDB = False
            try:
                masterSummary = scriptAgent.getMasterSummary()
                if masterSummary:
                    masterSummaryOnDB = True
                    print(f"\n\nmasterSummary set\n\nMaster Summary:\n{masterSummary}")
            except KeyNotFoundError:
                pass
            except:
                raise

            if not masterSummaryOnDB:
                try:
                    summaries = []
                    try:
                        try:
                            summaries.append(scriptAgent.getMasterYouTubeSummary())
                        except KeyNotFoundError:
                            pass
                        try:
                            summaries.append(scriptAgent.getMasterWebPageSummary())
                        except KeyNotFoundError:
                            pass
                        try:
                            summaries.append(scriptAgent.getMasterResearchPaperSummary())
                        except KeyNotFoundError:
                            pass
                        try:
                            summaries.append(scriptAgent.getCustomDataSummary())
                        except KeyNotFoundError:
                            pass
                    except:
                        raise
                    print("\n\nMaster Summary not set\n\nGenerating master summary")
                    masterSummary = scriptAgent.generateSummaryFromSummaries(summaries)
                    scriptAgent.setMasterSummary(masterSummary)
                    print(f"\n\n\nMaster Summary:\n{masterSummary}")
                except KeyNotFoundError:
                    pass
                except:
                    raise
                        
            introductionOnDB = False
            try:
                introduction = scriptAgent.getIntroduction()
                if introduction:
                    introductionOnDB = True
                    print(f"\n\Introduction set\n\nIntroduction:\n{introduction}")
            except KeyNotFoundError:
                pass
            except:
                raise

            if not introductionOnDB:
                try:
                    print("\n\nIntroduction not set\n\nGenerating Introduction")
                    introduction = scriptAgent.generateIntroduction(customData)
                    scriptAgent.setIntroduction(introduction)
                    print(f"\n\n\nIntroduction:\n{introduction}")
                except KeyNotFoundError:
                    pass
                except:
                    raise
            
            finalScript = False
            try:
                finalScript = scriptAgent.getScript()
                if finalScript:
                    finalScript = True
                    print(f"\n\Final Script set\n\nFinal Script:\n{finalScript}")
            except KeyNotFoundError:
                pass
            except:
                raise

            if not finalScript:
                try:
                    print("\n\nFinal Scrip not set\n\nGenerating Final Scrip")
                    finalScript = scriptAgent.generateScript()
                    scriptAgent.setScript(finalScript)
                    print(f"\n\n\nFinal Script:\n{finalScript}")
                except KeyNotFoundError:
                    pass
                except:
                    raise

            return jsonify({"message": "done", "success": True}), 200
        except KeyNotFoundError:
            pass
        except (ProjectNotFoundError) as e:
            return jsonify({"error": e.message, "success": False}), 500
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}", "success": False}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}", "success": False}), 500