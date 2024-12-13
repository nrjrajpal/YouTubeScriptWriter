from flask import Blueprint, jsonify
from PseudoAgents import ResearcherAgent
import ast

temp_blueprint = Blueprint('temp', __name__)

@temp_blueprint.route('/temp', methods=['POST'])
def temp():
    researcher = ResearcherAgent(projectID=1234)
    # Set an idea title and generate a search query
    # researcher.setIdeaTitle("Quantum Computing in Cryptography")
    # researcher.generateSearchQuery()
    # response=researcher.getLLMResponse("You are a helpful Ai Assistant", "Hello", model="llama-3.1-70b-versatile")
    # print("1"+response)
    # response=researcher.getLLMResponse("You are a helpful Ai Assistant", "Hello", model="llama-3.1-70b-versatile")
    # print("2"+response)
    idea_title="Master Time Management: 5 Simple Strategies for Productivity"
    idea_desc="This video explores five actionable time management strategies that can significantly boost your productivity. These strategies focus on breaking down tasks, prioritizing your day, and overcoming procrastination. The video will also dive into the psychological principles behind why these techniques work and how you can apply them to both your personal and professional life. Whether you're a student, professional, or entrepreneur, these tips will help you make the most of your time and achieve your goals."
    researcher.generateVideoTitles()
    response=researcher.getLLMResponse("You are a professional youtube title generator who generates a youtube title that can get maximum audience attention, from the idea title and idea description that is provided.",f"""Generate a YouTube video title based on the following video idea title and description:Video Idea Title: {idea_title} Video Idea Description: {idea_desc} The title should meet the following criteria:Be accurate and clearly represent the video's content to ensure viewers do not stop watching mid-video.Preferably be 50-60 characters, and no more than 100 characters.Highlight the key benefit or value viewers will gain from the video.Include major keywords or search terms that are frequently searched by users related to this content.Use CAPS to emphasize one or two key words for impact, but avoid excessive use of all caps.Keep the title brief, direct, and to the point, as viewers may only see part of it on YouTube.Consider using brackets or parentheses to add additional context or perceived value, but don’t force it unless it adds clarity.Address challenges or pain points that the target audience has, and create a title that speaks directly to solving those issues.If the content relates to lists or rankings, create a listicle-style title (e.g., '5 Tips for Boosting Productivity').Add a sense of urgency to encourage immediate clicks, if appropriate.Know the target audience and tailor the title to appeal to them.Include a hook or special element to capture attention and distinguish the video from competing content.Clearly communicate what viewers can expect from the video and why it is special or unique. Output format:Return the titles as an array of strings that can be type casted using the python list function Output: Only generate 3 titles in the form of an array of strings in a single line and nothing else.""")
    # llmoutput = chat_completion.choices[0].message.content
    titles = ast.literal_eval(response)

    # Retrieve and print the generated search query
    # search_query = researcher.getSearchQuery()
    # print(f"Search Query: {search_query}")

    return jsonify({"message":titles})
