from utils.exceptions import KeyNotFoundError, UserNotFoundError, ProjectNotFoundError
from flask import Blueprint, jsonify, request
from PseudoAgents import SyntheticAgent,ResearcherAgent,YouTubeAgent,User, ScriptAgent
import ast
import json
import os

temp_blueprint = Blueprint('temp', __name__)

@temp_blueprint.route('/temp', methods=['POST'])
def temp():
    try:

        researcher = SyntheticAgent(projectID="11223")
        # Set an idea title and generate a search query
        # researcher.setIdeaTitle("Quantum Computing in Cryptography")
        # researcher.generateSearchQuery()
        # response=researcher.getLLMResponse("You are a helpful Ai Assistant", "Hello", model="llama-3.1-70b-versatile")
        # print("1"+response)
        # response=researcher.getLLMResponse("You are a helpful Ai Assistant", "Hello", model="llama-3.1-70b-versatile")
        # print("2"+response)
        idea_title="Master Time Management: 5 Simple Strategies for Productivity"
        idea_desc="This video explores five actionable time management strategies that can significantly boost your productivity. These strategies focus on breaking down tasks, prioritizing your day, and overcoming procrastination. The video will also dive into the psychological principles behind why these techniques work and how you can apply them to both your personal and professional life. Whether you're a student, professional, or entrepreneur, these tips will help you make the most of your time and achieve your goals."
        researcher.setIdeaTitle(idea_title)
        researcher.setIdeaDescription(idea_desc)
        response=researcher.generateVideoTitles()
        print(response)
        temp=""
        try:
            titles = ast.literal_eval(response)
            print(titles)
            researcher.setVideoTitle(titles[0])
            temp=researcher.getVideoTitle()
        except:
            return jsonify({"message":"error"})
        
        return jsonify({"Titles":titles,"response":response,"finaltitle":temp})
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e})

    
    # response=researcher.getLLMResponse("You are a professional youtube title generator who generates a youtube title that can get maximum audience attention, from the idea title and idea description that is provided.",f"""Generate a YouTube video title based on the following video idea title and description:Video Idea Title: {idea_title} Video Idea Description: {idea_desc} The title should meet the following criteria:Be accurate and clearly represent the video's content to ensure viewers do not stop watching mid-video.Preferably be 50-60 characters, and no more than 100 characters.Highlight the key benefit or value viewers will gain from the video.Include major keywords or search terms that are frequently searched by users related to this content.Use CAPS to emphasize one or two key words for impact, but avoid excessive use of all caps.Keep the title brief, direct, and to the point, as viewers may only see part of it on YouTube.Consider using brackets or parentheses to add additional context or perceived value, but don’t force it unless it adds clarity.Address challenges or pain points that the target audience has, and create a title that speaks directly to solving those issues.If the content relates to lists or rankings, create a listicle-style title (e.g., '5 Tips for Boosting Productivity').Add a sense of urgency to encourage immediate clicks, if appropriate.Know the target audience and tailor the title to appeal to them.Include a hook or special element to capture attention and distinguish the video from competing content.Clearly communicate what viewers can expect from the video and why it is special or unique. Output format:Return the titles as an array of strings that can be type casted using the python list function Output: Only generate 3 titles in the form of an array of strings in a single line and nothing else.""")
    # llmoutput = chat_completion.choices[0].message.content
    # Retrieve and print the generated search query
    # search_query = researcher.getSearchQuery()
    # print(f"Search Query: {search_query}")

@temp_blueprint.route('/getSearchQuery', methods=['POST'])
def getSearchQuery():
    try:
        researcher = ResearcherAgent(projectID="11223")
        # Set an idea title and generate a search query
        # researcher.setIdeaTitle("Quantum Computing in Cryptography")
        # researcher.generateSearchQuery()
        # response=researcher.getLLMResponse("You are a helpful Ai Assistant", "Hello", model="llama-3.1-70b-versatile")
        # print("1"+response)
        # response=researcher.getLLMResponse("You are a helpful Ai Assistant", "Hello", model="llama-3.1-70b-versatile")
        # print("2"+response)
        # idea_title="Master Time Management: 5 Simple Strategies for Productivity"
        # idea_desc="This video explores five actionable time management strategies that can significantly boost your productivity. These strategies focus on breaking down tasks, prioritizing your day, and overcoming procrastination. The video will also dive into the psychological principles behind why these techniques work and how you can apply them to both your personal and professional life. Whether you're a student, professional, or entrepreneur, these tips will help you make the most of your time and achieve your goals."
        # videoTitle="Master TIME MANAGEMENT: 5 Productivity Hacks to Achieve Your Goals"
        # researcher.setVideoTitle(videoTitle)
        # researcher.setIdeaTitle(idea_title)
        # researcher.setIdeaDescription(idea_desc)
        response=researcher.generateSearchQuery()
        print(response)
        researcher.setSearchQuery(response)
        temp=researcher.getSearchQuery()
        return jsonify({"Video Title":researcher.getVideoTitle(), "finalsearchquery":temp})
        
        # response=researcher.getLLMResponse("You are a professional youtube title generator who generates a youtube title that can get maximum audience attention, from the idea title and idea description that is provided.",f"""Generate a YouTube video title based on the following video idea title and description:Video Idea Title: {idea_title} Video Idea Description: {idea_desc} The title should meet the following criteria:Be accurate and clearly represent the video's content to ensure viewers do not stop watching mid-video.Preferably be 50-60 characters, and no more than 100 characters.Highlight the key benefit or value viewers will gain from the video.Include major keywords or search terms that are frequently searched by users related to this content.Use CAPS to emphasize one or two key words for impact, but avoid excessive use of all caps.Keep the title brief, direct, and to the point, as viewers may only see part of it on YouTube.Consider using brackets or parentheses to add additional context or perceived value, but don’t force it unless it adds clarity.Address challenges or pain points that the target audience has, and create a title that speaks directly to solving those issues.If the content relates to lists or rankings, create a listicle-style title (e.g., '5 Tips for Boosting Productivity').Add a sense of urgency to encourage immediate clicks, if appropriate.Know the target audience and tailor the title to appeal to them.Include a hook or special element to capture attention and distinguish the video from competing content.Clearly communicate what viewers can expect from the video and why it is special or unique. Output format:Return the titles as an array of strings that can be type casted using the python list function Output: Only generate 3 titles in the form of an array of strings in a single line and nothing else.""")
        # llmoutput = chat_completion.choices[0].message.content
        # Retrieve and print the generated search query
        # search_query = researcher.getSearchQuery()
        # print(f"Search Query: {search_query}")
    except Exception as e:
        return jsonify({"error": "An error occurred: " + e.message or e})
    
@temp_blueprint.route('/getYTids', methods=['POST'])
def YtIds():
    researcher = YouTubeAgent(projectID=1234)
    try:
        researcher.setSearchQuery("productivity hacks based on time management psychology")
        print(researcher.getSearchQuery())
        temp = researcher.fetchVideosFromYT()
        Data = []
        # for i in temp:
        #     # Fetch metadata
        #     # metadata = researcher.fetchVideoMetadata(i)

        #     # Fetch transcript and make sure to extract data if it's a Response object
        #     transcript = researcher.fetchVideoTranscript(i)
        #     print("Done transcript")
        #     print("transcript"+transcript)
        #     Data.append({"ID": i, "Metadata": metadata, "Transcript": transcript})
        for i in temp:
            # Fetch transcript and process the Response object
            
            metadata = researcher.fetchVideoMetadata(i)
            transcript_response = researcher.fetchVideoTranscript(i)
            transcript = (
                transcript_response.get('formatted_transcript') 
                if isinstance(transcript_response, dict) and 'formatted_transcript' in transcript_response 
                else str(transcript_response)
            )
            
            print("Done transcript")
            # print(f"Transcript: {transcript}")
            
            Data.append({
            "Metadata": metadata,
            "Transcript": transcript if isinstance(transcript, str) else "Transcript not available"
            }) 

        print(Data)
        current_directory = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
        output_file = os.path.join(current_directory, "api_response.json")  # Specify file path
        with open(output_file, "w") as file:
            json.dump(Data, file)

    except Exception as e:
        print(f"Error: {e}")
        # In case of error, return None or a proper error message
        return None
    
    return {"Data": Data}

@temp_blueprint.route('/user', methods=['POST'])
def user():
    try:
        usr=User(userEmail="temp@email.com")
        print(usr.userEmail)
        temp=usr.getChannelDetails()
        return jsonify({"Message":temp})
        
    except Exception as e:
        print(f"Error: {e}")
        # In case of error, return None or a proper error message
        return None


# @temp_blueprint.route('/getSelectedQuestions', methods=['POST'])
# def getSelectedQuestions():
#     try:
        
#         sa=ScriptAgent(projectID="Dx1qIVN", userEmail="ishanvyavahare+real@gmail.com")
#         temp=sa.getSelectedQuestions()
#         return jsonify({"Message":temp})
        
#     except (UserNotFoundError, KeyNotFoundError, ProjectNotFoundError) as e:
#         return jsonify({"error": e.message, "success": False}), 404
#     except Exception as e:
#         print("\n\n\nError: ", e)
#         return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500


@temp_blueprint.route('/tempIntro', methods=['POST'])
def tempIntro():
    try:
        sa=ScriptAgent(projectID="Dx1qIVN", userEmail="ishanvyavahare+real@gmail.com")
        intro = sa.generateIntroduction()
        return jsonify({"Introduction":intro})
        # yt_agent = YouTubeAgent(projectID="11223")
    except:
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500

@temp_blueprint.route('/submitSources', methods=['POST'])
def submitSources():
    try:
        data = request.get_json()
        userEmail = data.get('userEmail')
        projectID = data.get('projectID')
        if not userEmail:
            return jsonify({"error": "Missing required field: userEmail", "success": False}), 400

        if not projectID:
            return jsonify({"error": "Missing required field: projectID", "success": False}), 400

        syntheticAgent = SyntheticAgent(projectID, userEmail)
        syntheticAgent.updateProjectState('script')
        return jsonify({"success":True}),200
        # yt_agent = YouTubeAgent(projectID="11223")
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500
    
@temp_blueprint.route('/getTranscript', methods=['POST'])
def getTranscript():
    try:
        data = request.get_json()
        videoID = data.get('videoID')
        ytAgent = YouTubeAgent(None, None)
        transcript = ytAgent.fetchVideoTranscript(videoID)
        print(transcript)
        return jsonify({"transcript": transcript}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred. Check the logs.", "success": False}), 500