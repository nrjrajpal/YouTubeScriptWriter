from flask_cors import CORS
from flask import Flask, jsonify, Response, Blueprint, request
import time
import json
import yt_dlp
from utils.exceptions import KeyNotFoundError, ProjectNotFoundError, UserNotFoundError, EmailMismatchError
from datetime import datetime
from PseudoAgents import SyntheticAgent, ScriptAgent, YouTubeAgent, WebpageAgent, ResearchPaperAgent, CustomDataAgent

scripts_old_blueprint = Blueprint('scripts_old', __name__)

def fetch_video_metadata(video_url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            video_info = ydl.extract_info(video_url, download=False)
            video_details = {}
            # {
            #     "id": "d5gf9dXbPi0",
            #     "title": "Exploring the Future of AI: Innovations and Challenges in Artificial Intelligence",
            #     "views": "1.2M views",
            #     "duration": "15:32",
            #     "publishedTime": "2 weeks ago"
            # }
            duration = ""
            hours, remainder = divmod(video_info.get('duration'), 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours > 0:
                duration = f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"
            else:
                duration = f"{int(minutes)}:{int(seconds):02}"

            video_details["id"] = video_info.get('id')
            video_details["title"] = video_info.get('title')
            video_details["views"] = format_views(video_info.get('view_count')) + " views"
            video_details["duration"] = duration
            video_details["publishedTime"] = datetime.strptime(video_info.get('upload_date'), "%Y%m%d").strftime("%B %d, %Y")
            # print("ID: ", video_info.get('id'))
            # print("Title: ", video_info.get('title'))
            # views = format_views(video_info.get('view_count'))
            # print("Views: ", views)
            # # print("Duration: ", video_info.get('duration'))
            # hours, remainder = divmod(video_info.get('duration'), 3600)
            # minutes, seconds = divmod(remainder, 60)
            # duration = ""
            # if hours > 0:
            #     duration = f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"
            # else:
            #     duration = f"{int(minutes)}:{int(seconds):02}"
            # # print(f"Duration: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
            # print("duration: ", duration)

            # date = datetime.strptime(video_info.get('upload_date'), "%Y%m%d").strftime("%B %d, %Y")
            # print("upload_date: ", date)
            return video_details
        except Exception as e:
            print(f"Error: {e}")
            return None

def format_views(view_count):
    try:
        num = int(view_count)

        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f}B".rstrip('0').rstrip('.')
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M".rstrip('0').rstrip('.')
        elif num >= 1_000:
            return f"{num / 1_000:.2f}K".rstrip('0').rstrip('.')
        else:
            return str(num)
    except ValueError:
        return "Invalid number"

@scripts_old_blueprint.route('/getVideoTitle', methods=['POST'])
def getVideoTitle():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400
        
        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        synagent = SyntheticAgent(projectID, userEmail)
        videoTitle = synagent.getVideoTitle()
        print(videoTitle)

        return jsonify({"success": True, "message": "Successfully retrieved video title", "title": videoTitle}), 200
    except (KeyNotFoundError, UserNotFoundError, ProjectNotFoundError) as e:   
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500


@scripts_old_blueprint.route('/getIdeaDetails', methods=['POST'])
def getIdeaDetails():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        synagent = SyntheticAgent(projectID, userEmail)
        ideaTitle = synagent.getIdeaTitle()
        ideaDescription = synagent.getIdeaDescription()

        return jsonify({"success": True, "message": "Successfully retrieved idea details", "title": ideaTitle, "description": ideaDescription}), 200
    except (KeyNotFoundError, UserNotFoundError, ProjectNotFoundError) as e:   
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500
    
    # return jsonify({
    #     "title": "Innovative AI-powered Personal Assistant",
    #     "description": "A cutting-edge AI personal assistant that learns from user behavior and preferences to provide highly personalized recommendations and automate daily tasks, enhancing productivity and improving quality of life."
    # })

@scripts_old_blueprint.route('/getSelectedQuestions', methods=['POST'])
def getSelectedQuestions():
    # time.sleep(1.5)  # Simulating API delay
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        sagent = ScriptAgent(projectID, userEmail)
        selectedQuestions = sagent.getSelectedQuestions()

        return jsonify(selectedQuestions), 200
    except (KeyNotFoundError, UserNotFoundError, ProjectNotFoundError) as e:   
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500
    
    # return jsonify([
    #     "What inspired you to develop this AI personal assistant?",
    #     "How does your solution differ from existing AI assistants in the market?",
    #     "Can you walk us through a typical user interaction with your AI assistant?"
    # ])

@scripts_old_blueprint.route('/getYoutubeVideos', methods=['POST'])
def getYoutubeVideos():
    # time.sleep(5.5)  # Simulating API delay
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        ytagent = YouTubeAgent(projectID, userEmail)
        # get yt links from db
        yt_ids = ytagent.getVideoIDs()

        yt_links = []
        for id in yt_ids:
            yt_links.append("https://www.youtube.com/watch?v="+ id)
        
        yt_data = []
        data = []
        for link in yt_links:
            data.append(fetch_video_metadata(link))

        return jsonify({"available": True, "data" : data, "success": True, "message": "Successfully retrieved youtube video details"}), 200
    except (KeyNotFoundError) as e:
        return jsonify({"available": False, "message": "YouTube was not selected as a data source."})
    except (UserNotFoundError, ProjectNotFoundError) as e:   
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500


@scripts_old_blueprint.route('/getWebPages', methods=['POST'])
def getWebPages():
    # time.sleep(2.2)  # Simulating API delay

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

        formattedWebPageData = []
        for webdata in webPageData:
            formattedWebPageData.append({"title": webdata["webpage_title"], "url": webdata["webpage_url"]})

        return jsonify({"available": True, "data" : formattedWebPageData, "success": True, "message": "Successfully retrieved webpages' details"}), 200
    except (KeyNotFoundError) as e:
        return jsonify({"available": False, "message": "Webpages were not selected as a data source."})
    except (UserNotFoundError, ProjectNotFoundError) as e:   
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500


@scripts_old_blueprint.route('/getResearchPapers', methods=['POST'])
def getResearchPapers():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')

        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400
        
        ragent = ResearchPaperAgent(projectID, userEmail)
        researchPaperData = ragent.getResearchPaperUrlsAndMetadata()

        formattedResearchPaperData = []
        for record in researchPaperData:
            formattedResearchPaperData.append({"title": record["research_paper_title"], "url": record["research_paper_url"]})

        return jsonify({"available": True, "data" : formattedResearchPaperData, "success": True, "message": "Successfully retrieved webpages' details"}), 200
    except (KeyNotFoundError) as e:
        return jsonify({"available": False, "message": "Research papers were not selected as a data source."})
    except (UserNotFoundError, ProjectNotFoundError) as e: 
        return jsonify({"error": e, "success": False}), 404
    except Exception as e:
        return jsonify({"error": e, "success": False}), 500
    
    # return jsonify({
    #     "available": True,
    #     "data": [
    #         { "title": "Advancements in AI Personal Assistants", "authors": "John Doe, Jane Smith", "url": "https://example.com/paper1" },
    #         { "title": "User Behavior Prediction in AI Systems", "authors": "Alice Johnson, Bob Williams", "url": "https://example.com/paper2" },
    #         { "title": "Ethical Considerations in AI Assistants", "authors": "Eva Brown, Michael Green", "url": "https://example.com/paper3" }
    #     ]
    # })

@scripts_old_blueprint.route('/getCustomData', methods=['POST'])
def getCustomData():
    time.sleep(2)  # Simulating API delay
    return jsonify({
        "available": True,
        "data": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
    })

@scripts_old_blueprint.route('/getThoughtProcess', methods=['POST'])
def getThoughtProcess():
    def generate(projectID, userEmail):
        print("In gen")
        # paragraphs = [
        #     {"paragraph": "As we embark on the journey of developing an AI-powered personal assistant, it's crucial to first understand the core problem we're addressing. In today's fast-paced world, individuals are overwhelmed with information, tasks, and decisions. Our AI assistant aims to alleviate this cognitive load by providing personalized, context-aware support across various aspects of daily life.", "color": "text-blue-500"},
        #     {"paragraph": "The foundation of our AI assistant lies in its ability to learn from user behavior and preferences. This involves implementing advanced machine learning algorithms, particularly in the realms of natural language processing and predictive analytics. By analyzing patterns in user interactions, the system can anticipate needs and offer proactive assistance.", "color": "text-green-500"},
        #     {"paragraph": "One of the key challenges we face is striking the right balance between functionality and user privacy. While deep learning models benefit from vast amounts of data, we must ensure that user information is handled ethically and securely. This necessitates the implementation of robust data encryption methods and giving users granular control over their data sharing preferences.", "color": "text-red-500"},
        #     {"paragraph": "Another critical aspect of our development process is creating an intuitive and seamless user interface. The AI assistant should feel like a natural extension of the user's thought process, rather than a separate entity to be commanded. This involves designing conversational AI that can understand context, maintain coherent dialogues, and adapt its communication style to individual users.", "color": "text-purple-500"},
        #     {"paragraph": "As we progress, we'll need to continuously evaluate and refine our AI models. This iterative process will involve extensive testing, gathering user feedback, and staying abreast of the latest advancements in AI research. By doing so, we can ensure that our personal assistant remains at the cutting edge of technology while providing tangible benefits to its users.", "color": "text-yellow-500"}
        # ]
        
        # for paragraph in paragraphs:
        #     time.sleep(3)  # Simulate delay between paragraphs
        #     yield f"data: {json.dumps(paragraph)}\n\n"
        try:
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
                        print("tryyy")
                        ytSummariesOnDB = True
                        print("\n\nYTSummaries set\n\n")
                        videoIDs = ytAgent.getVideoIDs()
                        for ytSummary, videoID in zip(ytSummaries, videoIDs):
                            # print(f"\n\n\nSummary for https://www.youtube.com/watch?v={videoID}:\n{ytSummary}")
                            # text = {"paragraph": "BAs we embark on the journey of developing an AI-powered personal assistant, it's crucial to first understand the core problem we're addressing. In today's fast-paced world, individuals are overwhelmed with information, tasks, and decisions. Our AI assistant aims to alleviate this cognitive load by providing personalized, context-aware support across various aspects of daily life.", "color": "text-blue-500"}
                            
                            # text = {"paragraph": "CAs we embark on the journey of developing an AI-powered personal assistant, it's crucial to first understand the core problem we're addressing. In today's fast-paced world, individuals are overwhelmed with information, tasks, and decisions. Our AI assistant aims to alleviate this cognitive load by providing personalized, context-aware support across various aspects of daily life.", "color": "text-blue-500"}
                            text = {"paragraph": "\n\n\nSummary for https://www.youtube.com/watch?v="+videoID+":\n\n"+ytSummary, "color": "text-blue-500"}
                            yield f"data: {json.dumps(text)}\n\n"
                            # yield f"data: {json.dumps(text)}"
                    else:
                        print("ELSE tryyy")

                except KeyNotFoundError:
                    print("KEY tryyy")
                    pass
                except Exception as e:
                    print("ERR tryyy")
                    print(e)
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
                            # print(f"\n\nSummary for https://www.youtube.com/watch?v={videoID}:\n{ytSummary}")
                            text = {"paragraph": "\n\n\nSummary for https://www.youtube.com/watch?v="+videoID+":\n\n"+ytSummary, "color": "text-red-500"}
                            yield f"data: {json.dumps(text)}\n\n"
                        # for videoTranscript in videoTranscripts:
                    except KeyNotFoundError:
                        pass
                    except:
                        raise

                masterYTSummaryOnDB = False
                try:
                    masterYTSummary = scriptAgent.getMasterYouTubeSummary()
                    if masterYTSummary:
                        masterYTSummaryOnDB = True
                        text = {"paragraph": f"Master YouTube Summary:\n{masterYTSummary}", "color": "text-yellow-500"}
                        yield f"data: {json.dumps(text)}\n\n"
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
                        # print(f"\n\n\nMaster YouTube Summary:\n{masterYTSummary}")
                        text = {"paragraph": f"\n\nSet Master YouTube Summary:\n{masterYTSummary}", "color": "text-yellow-500"}
                        yield f"data: {json.dumps(text)}\n\n"
                    except KeyNotFoundError:
                        pass
                    except:
                        raise

                # --------------------------------------------------------

                wpSummariesOnDB = False
                try:
                    wpSummaries = scriptAgent.getWebPageSummaries()
                    if wpSummaries:
                        wpSummariesOnDB = True
                        print("\n\nwpSummaries set\n\n")
                        webPageData = wpAgent.getWebPageData()
                        webPageURLs = [webPage["webpage_url"] for webPage in webPageData if "webpage_url" in webPage]
                        for wpSummary, webPageURL in zip(wpSummaries, webPageURLs):
                            # print(f"\n\n\nSummary for {webPageURL}:\n{wpSummary}")
                            text = {"paragraph": "\n\n\nSummary for: "+webPageURL+":\n\n"+wpSummary, "color": "text-purple-500"}
                            yield f"data: {json.dumps(text)}\n\n"
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
                            # print(f"\n\n\nSummary for {webPageURL}:\n{wpSummary}")
                            text = {"paragraph": "\n\n\nSummary for: "+webPageURL+":\n\n"+wpSummary, "color": "text-purple-500"}
                            yield f"data: {json.dumps(text)}\n\n"

                    except KeyNotFoundError:
                        pass
                    except:
                        raise

                masterWPSummaryOnDB = False
                try:
                    masterWPSummary = scriptAgent.getMasterWebPageSummary()
                    if masterWPSummary:
                        masterWPSummaryOnDB = True
                        # print(f"\n\nMasterWPSummary set\n\nMaster Web Page Summary:\n{masterWPSummary}")
                        text = {"paragraph": f"\n\nMaster Webpage Summary:\n{masterWPSummary}", "color": "text-yellow-500"}
                        yield f"data: {json.dumps(text)}\n\n"
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
                        # print(f"\n\nMaster WebPage Summary:\n{masterWPSummary}")
                        text = {"paragraph": f"\n\nSet Master Webpage Summary:\n{masterYTSummary}", "color": "text-yellow-500"}
                        yield f"data: {json.dumps(text)}\n\n"
                    except KeyNotFoundError:
                        pass
                    except:
                        raise

                # --------------------------------------------------------

                rpSummariesOnDB = False
                try:
                    rpSummaries = scriptAgent.getResearchPaperSummaries()
                    if rpSummaries:
                        rpSummariesOnDB = True
                        print("\n\nrpSummaries set\n\n")
                        researchPaperData = rpAgent.getResearchPaperUrlsAndMetadata()
                        researchPaperURLs = [researchPaper["research_paper_url"] for researchPaper in researchPaperData if "research_paper_url" in researchPaper]
                        for rpSummary, researchPaperURL in zip(rpSummaries, researchPaperURLs):
                            # print(f"\n\n\nSummary for {researchPaperURL}:\n{rpSummary}")
                            text = {"paragraph": "\n\n\nSummary for: "+researchPaperURL+":\n\n"+rpSummary, "color": "text-blue-500"}
                            yield f"data: {json.dumps(text)}\n\n"
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
                            # print(f"\n\n\nSummary for {researchPaperURL}:\n{rpSummary}")
                            text = {"paragraph": "\n\n\nSummary for: "+researchPaperURL+":\n\n"+rpSummary, "color": "text-blue-500"}
                            yield f"data: {json.dumps(text)}\n\n"
                    except KeyNotFoundError:
                        pass
                    except:
                        raise

                masterRPSummaryOnDB = False
                try:
                    masterRPSummary = scriptAgent.getMasterResearchPaperSummary()
                    if masterRPSummary:
                        masterRPSummaryOnDB = True
                        # print(f"\n\nMaster Research Paper Summary:\n{masterRPSummary}")
                        text = {"paragraph": f"\n\nMaster Research Paper Summary:\n{masterRPSummary}", "color": "text-yellow-500"}
                        yield f"data: {json.dumps(text)}\n\n"
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
                        # print(f"\n\n\nMaster Research Paper Summary:\n{masterRPSummary}")
                        text = {"paragraph": f"\n\nSet Master Research Paper Summary:\n{masterRPSummary}", "color": "text-yellow-500"}
                        yield f"data: {json.dumps(text)}\n\n"
                    except KeyNotFoundError:
                        pass
                    except:
                        raise
            

            # --------------------------------------------------------
            

                cdSummaryOnDB = False
                try:
                    cdSummary = scriptAgent.getCustomDataSummary()
                    if cdSummary:
                        cdSummaryOnDB = True
                        # print(f"\n\ncdSummary set\n\nCustom Data Summary:\n{cdSummary}")
                        text = {"paragraph": f"\n\nCustom Data Summary:\n{cdSummary}", "color": "text-yellow-500"}
                        yield f"data: {json.dumps(text)}\n\n"
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
                        # print(f"\n\n\nCustom Data Summary:\n{cdSummary}")
                        text = {"paragraph": f"\n\nSet Custom Data Summary:\n{cdSummary}", "color": "text-yellow-500"}
                        yield f"data: {json.dumps(text)}\n\n"
                    except KeyNotFoundError:
                        pass
                    except:
                        raise
                

            # --------------------------------------------------------


                masterSummaryOnDB = False
                try:
                    masterSummary = scriptAgent.getMasterSummary()
                    if masterSummary:
                        masterSummaryOnDB = True
                        # print(f"\n\nmasterSummary set\n\nMaster Summary:\n{masterSummary}")
                        text = {"paragraph": f"\n\nMaster Summary:\n{masterSummary}", "color": "text-green-500"}
                        yield f"data: {json.dumps(text)}\n\n"
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
                        # print(f"\n\n\nMaster Summary:\n{masterSummary}")
                        text = {"paragraph": f"\n\nSet Master Summary:\n{masterSummary}", "color": "text-green-500"}
                        yield f"data: {json.dumps(text)}\n\n"
                    except KeyNotFoundError:
                        pass
                    except:
                        raise


            # --------------------------------------------------------


                introductionOnDB = False
                try:
                    introduction = scriptAgent.getIntroduction()
                    if introduction:
                        introductionOnDB = True
                        # print(f"\n\Introduction set\n\nIntroduction:\n{introduction}")
                        # text = {"paragraph": f"\n\nIntroduction:\n{introduction}", "color": "text-green-500"}
                        # yield f"data: {json.dumps(text)}\n\n"
                except KeyNotFoundError:
                    pass
                except:
                    raise

                if not introductionOnDB:
                    try:
                        print("\n\nIntroduction not set\n\nGenerating Introduction")
                        introduction = scriptAgent.generateIntroduction(customData)
                        scriptAgent.setIntroduction(introduction)
                        # print(f"\n\n\nIntroduction:\n{introduction}")
                        # text = {"paragraph": f"\n\nSet Introduction:\n{introduction}", "color": "text-green-500"}
                        # yield f"data: {json.dumps(text)}\n\n"
                    except KeyNotFoundError:
                        pass
                    except:
                        raise
                
            
            # ---------------------------------------------------------
                
                finalScriptOnDB = False
                try:
                    finalScript = scriptAgent.getScript()
                    if finalScript:
                        finalScriptOnDB = True
                        # print(f"\n\Final Script set\n\nFinal Script:\n{finalScript}")
                        # text = {"paragraph": f"\n\nScript: \n{finalScript}", "color": "text-green-500"}
                        # yield f"data: {json.dumps(text)}\n\n"
                except KeyNotFoundError:
                    pass
                except:
                    raise

                if not finalScriptOnDB:
                    try:
                        print("\n\nFinal Script not set\n\nGenerating Final Scrip")
                        finalScript = scriptAgent.generateScript()
                        scriptAgent.setScript(finalScript)
                        # print(f"\n\n\nFinal Script:\n{finalScript}")
                        # text = {"paragraph": f"\n\nSet Script: \n{finalScript}", "color": "text-green-500"}
                        # yield f"data: {json.dumps(text)}\n\n"
                    except KeyNotFoundError:
                        raise
                    except:
                        raise
                
                # return jsonify({"message": "done", "success": True}), 200
            
            except KeyNotFoundError:
                raise
                # return jsonify({"error": e.message, "success": False}), 500
            except (ProjectNotFoundError) as e:
                raise
                # return jsonify({"error": e.message, "success": False}), 500
            except Exception as e:
                raise
                # return jsonify({"error": f"An error occurred: {e}", "success": False}), 500

        except Exception as e:
            raise
            # return jsonify({"error": f"An error occurred: {e}", "success": False}), 500

    data = request.get_json()
    userEmail = data.get('userEmail')
    projectID = data.get('projectID')
    if not userEmail:
        print("UserEmail not found")
        # return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

    if not projectID:
        print("projectID not found")
        # return jsonify({"error": "Missing required field: projectID", "success": False}), 400
    print("CALLED!", projectID)
    return Response(generate(projectID, userEmail), content_type='text/event-stream')

@scripts_old_blueprint.route('/getFinalScript', methods=['POST'])
def getFinalScript():
    time.sleep(5)  # Simulating API delay

    data = request.get_json()
    userEmail = data.get('userEmail')
    projectID = data.get('projectID')
    if not userEmail:
        print("UserEmail not found")

    if not projectID:
        print("projectID not found")

    scriptagent = ScriptAgent(projectID, userEmail)
    finalScript = scriptagent.getScript()

    return jsonify(finalScript)