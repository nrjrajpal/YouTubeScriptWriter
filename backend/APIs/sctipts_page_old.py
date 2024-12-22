from flask import Flask, jsonify, Response, Blueprint
from flask_cors import CORS
import time
import json
import yt_dlp

from datetime import datetime

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

@scripts_old_blueprint.route('/api/project-title', methods=['GET'])
def get_project_title():
    time.sleep(1)  # Simulating API delay
    return jsonify({
        "title": "AI-powered Personal Assistant Development Project"
    })

@scripts_old_blueprint.route('/api/idea-details', methods=['GET'])
def get_idea_details():
    time.sleep(2)  # Simulating API delay
    return jsonify({
        "title": "Innovative AI-powered Personal Assistant",
        "description": "A cutting-edge AI personal assistant that learns from user behavior and preferences to provide highly personalized recommendations and automate daily tasks, enhancing productivity and improving quality of life."
    })

@scripts_old_blueprint.route('/api/selected-questions', methods=['GET'])
def get_selected_questions():
    time.sleep(3.5)  # Simulating API delay
    return jsonify([
        "What inspired you to develop this AI personal assistant?",
        "How does your solution differ from existing AI assistants in the market?",
        "Can you walk us through a typical user interaction with your AI assistant?"
    ])

@scripts_old_blueprint.route('/api/youtube-videos', methods=['GET'])
def get_youtube_videos():
    # time.sleep(5.5)  # Simulating API delay
    yt_flag = True
    if not yt_flag:
        return jsonify({"available": False, "message": "YouTube videos were not selected as a data source."})
    yt_links = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=iqJ0kg9xvLs",
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
    ]
    data = []
    for link in yt_links:
        data.append(fetch_video_metadata(link))

    return jsonify({
        "available": True,
        "data" : data
        # "data": [
        #     {
        #         "id": "d5gf9dXbPi0",
        #         "title": "Exploring the Future of AI: Innovations and Challenges in Artificial Intelligence",
        #         "views": "1.2M views",
        #         "duration": "15:32",
        #         "publishedTime": "2 weeks ago"
        #     },
        #     {
        #         "id": "iqJ0kg9xvLs",
        #         "title": "Machine Learning Explained: From Basics to Advanced Concepts",
        #         "views": "890K views",
        #         "duration": "22:18",
        #         "publishedTime": "1 month ago"
        #     },
        #     {
        #         "id": "vwRTYMcpHt8",
        #         "title": "The Ethics of AI: Balancing Progress and Responsibility in the Age of Intelligent Machines",
        #         "views": "650K views",
        #         "duration": "18:45",
        #         "publishedTime": "3 weeks ago"
        #     }
        # ]
    })

@scripts_old_blueprint.route('/api/webpages', methods=['GET'])
def get_webpages():
    time.sleep(7.2)  # Simulating API delay
    wp_flag = True
    if not wp_flag:
        return jsonify({"available": False, "message": "Webpages were not selected as a data source."})
    return jsonify({
        "available": True,
        "data": [
            { "title": "AI Assistants Overview", "url": "https://example.com/ai-assistants" },
            { "title": "Machine Learning Techniques", "url": "https://example.com/machine-learning" },
            { "title": "User Behavior Analysis", "url": "https://example.com/user-behavior-analysis" }
        ]
    })

@scripts_old_blueprint.route('/api/research-papers', methods=['GET'])
def get_research_papers():
    time.sleep(6.8)  # Simulating API delay
    rp_flag = True
    if not rp_flag:
        return jsonify({"available": False, "message": "Research papers were not selected as a data source."})
    return jsonify({
        "available": True,
        "data": [
            { "title": "Advancements in AI Personal Assistants", "authors": "John Doe, Jane Smith", "url": "https://example.com/paper1" },
            { "title": "User Behavior Prediction in AI Systems", "authors": "Alice Johnson, Bob Williams", "url": "https://example.com/paper2" },
            { "title": "Ethical Considerations in AI Assistants", "authors": "Eva Brown, Michael Green", "url": "https://example.com/paper3" }
        ]
    })

@scripts_old_blueprint.route('/api/custom-data', methods=['GET'])
def get_custom_data():
    time.sleep(5.3)  # Simulating API delay
    ct_flag = True
    if not ct_flag:
        return jsonify({"available": False, "message": "Custom data was not provided for this project."})
    return jsonify({
        "available": True,
        "data": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
    })

@scripts_old_blueprint.route('/api/thought-process', methods=['GET'])
def get_thought_process():
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

@scripts_old_blueprint.route('/api/final-script', methods=['GET'])
def get_final_script():
    time.sleep(10.2)  # Simulating API delay
    return jsonify("This is the final script content. It's likely more concise and polished compared to the thought process. The AI-powered personal assistant we're developing represents a significant leap forward in how individuals manage their daily lives and interact with technology. By leveraging advanced machine learning algorithms, our assistant can provide highly personalized support, anticipating user needs and offering proactive assistance. Key features include natural language processing for intuitive interactions, predictive analytics for smart recommendations, and a robust privacy framework to ensure user data security. The user interface is designed to be seamless and adaptive, making the AI feel like a natural extension of the user's own cognitive processes. Through continuous refinement and updates based on user feedback and emerging AI technologies, our personal assistant aims to set a new standard in AI-driven productivity and lifestyle enhancement.")

if __name__ == '__main__':
    app.run(debug=True)