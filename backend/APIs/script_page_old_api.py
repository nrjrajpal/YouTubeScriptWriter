from flask_cors import CORS
from flask import Flask, jsonify, Response, Blueprint, request
import time
import json
import yt_dlp
from utils.exceptions import KeyNotFoundError, ProjectNotFoundError, UserNotFoundError, EmailMismatchError
from datetime import datetime
from PseudoAgents import SyntheticAgent, ScriptAgent, YouTubeAgent, WebpageAgent, ResearchPaperAgent

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
    def generate():
        paragraphs = [
            {"paragraph": "As we embark on the journey of developing an AI-powered personal assistant, it's crucial to first understand the core problem we're addressing. In today's fast-paced world, individuals are overwhelmed with information, tasks, and decisions. Our AI assistant aims to alleviate this cognitive load by providing personalized, context-aware support across various aspects of daily life.", "color": "text-blue-500"},
            {"paragraph": "The foundation of our AI assistant lies in its ability to learn from user behavior and preferences. This involves implementing advanced machine learning algorithms, particularly in the realms of natural language processing and predictive analytics. By analyzing patterns in user interactions, the system can anticipate needs and offer proactive assistance.", "color": "text-green-500"},
            {"paragraph": "One of the key challenges we face is striking the right balance between functionality and user privacy. While deep learning models benefit from vast amounts of data, we must ensure that user information is handled ethically and securely. This necessitates the implementation of robust data encryption methods and giving users granular control over their data sharing preferences.", "color": "text-red-500"},
            {"paragraph": "Another critical aspect of our development process is creating an intuitive and seamless user interface. The AI assistant should feel like a natural extension of the user's thought process, rather than a separate entity to be commanded. This involves designing conversational AI that can understand context, maintain coherent dialogues, and adapt its communication style to individual users.", "color": "text-purple-500"},
            {"paragraph": "As we progress, we'll need to continuously evaluate and refine our AI models. This iterative process will involve extensive testing, gathering user feedback, and staying abreast of the latest advancements in AI research. By doing so, we can ensure that our personal assistant remains at the cutting edge of technology while providing tangible benefits to its users.", "color": "text-yellow-500"}
        ]
        
        for paragraph in paragraphs:
            time.sleep(3)  # Simulate delay between paragraphs
            yield f"data: {json.dumps(paragraph)}\n\n"

    return Response(generate(), content_type='text/event-stream')

@scripts_old_blueprint.route('/getFinalScript', methods=['POST'])
def getFinalScript():
    time.sleep(1.2)  # Simulating API delay
    return jsonify("""
        Lorem ipsum odor amet, consectetuer adipiscing elit. Viverra varius montes purus nec elit rutrum convallis. Feugiat nascetur tempor hendrerit habitasse iaculis. Magnis scelerisque sollicitudin risus sem fusce fusce felis. Commodo aenean aliquet ex lacinia ornare ad. Praesent rutrum sollicitudin sit diam ullamcorper nibh. Condimentum vel morbi phasellus sem; ornare tincidunt inceptos pharetra. Himenaeos lectus senectus maximus euismod tempus dapibus adipiscing non.
        Ligula tempor urna ad habitasse congue nunc, a id elit. Nisi non parturient dis non nisl faucibus. Orci torquent lacinia tristique sit ut posuere. Dapibus ex pulvinar ligula egestas fames ultricies est torquent. Curae duis at maecenas libero sit proin vestibulum. Mollis ridiculus praesent praesent ipsum mattis purus scelerisque. Alibero nisi hendrerit purus pretium suscipit ultricies luctus. Quisque suspendisse augue lacus primis aliquam sem viverra. Conubia quis aenean vitae nunc erat facilisi adipiscing curae hac. Litora mauris potenti duis ultricies leo metus.
        Odio etiam non orci tristique nisi fermentum maximus. Ante facilisis morbi praesent nibh, lacinia fusce aliquet nisl. Vivamus pretium consectetur turpis varius finibus auctor nec sollicitudin. Libero erat neque justo interdum dignissim; dignissim vitae nunc. Tincidunt eros dictum, ornare maximus maecenas litora dictum nisl. Ultricies primis auctor vestibulum a commodo. Fames finibus in efficitur volutpat integer blandit aliquam.
        Felis accumsan etiam ligula aliquet arcu luctus. Platea pharetra aptent per diam nascetur parturient odio id. Egestas eros orci id malesuada lorem nisl orci ex dolor. Integer iaculis lacinia pulvinar dignissim ad consequat risus. Curabitur facilisi volutpat ullamcorper mauris est libero taciti nostra ipsum. Eleifend magna vel nibh metus vitae ornare. Pretium nunc nullam ante nibh magnis malesuada massa. Imperdiet interdum tincidunt volutpat mattis purus ac duis. Turpis nunc inceptos ridiculus erat sem massa ornare. Nunc consequat convallis etiam tempus sociosqu metus pretium.
        Nisl lectus hac sed nec eget parturient platea tristique sociosqu. Inceptos ut orci imperdiet imperdiet per curabitur in penatibus fringilla. Consectetur parturient nullam, vel tincidunt egestas morbi fermentum. Parturient laoreet hendrerit consectetur in eros massa; justo vel posuere. Adipiscing maximus amet mauris parturient; condimentum dictum orci. Eleifend ligula lobortis nam justo nunc mauris nisl ornare. Posuere netus habitant habitasse faucibus habitasse litora.
    """)