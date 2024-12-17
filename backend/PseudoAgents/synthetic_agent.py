from groq import Groq
import os
from dotenv import load_dotenv
from utils.firebase import db
from utils.exceptions import ProjectNotFoundError, KeyNotFoundError

PROJECT_COLLECTION_NAME = "TrialProject"

load_dotenv()

class SyntheticAgent:
    def __init__(self, projectID):
        self.projectID = projectID
        self.ideaTitle = None
        self.ideaDescription = None
        self.videoTitle = None
        self.groqAPIKey = None
        self.serperAPIKey = None
        self.tavilyAPIKey = None

    # LLM Response Function
    def getLLMResponse(self, system_query, user_query, model="llama-3.1-70b-versatile"):
        try:
            client = Groq(api_key=self.getGroqAPIKey())

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_query},
                    {"role": "user","content": user_query}
                ],
                model=model,
            )

            return chat_completion.choices[0].message.content
        except Exception as e:
            raise

    # Idea Title Functions
    def getIdeaTitle(self):
        try: 
            if not self.ideaTitle:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("ID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")

                record = docs[0].to_dict()

                if "ideaTitle" not in record:
                    raise KeyNotFoundError("Idea title is not set in the database.")

                self.ideaTitle = record["ideaTitle"]

            return self.ideaTitle 
        except:
            raise
        
    # Idea Description Functions
    def getIdeaDescription(self):
        try:
            if not self.ideaDescription:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("ID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "ideaDescription" not in record:
                    raise KeyNotFoundError("Idea description is not set in the database.")

                self.ideaDescription = record["ideaDescription"]

            return self.ideaDescription
        except:
            raise

    # Video Title Functions
    def getVideoTitle(self):
        try:
            if not self.videoTitle:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("ID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "videoTitle" not in record:
                    raise KeyNotFoundError("Video title is not set in the database.")

                self.videoTitle = record["videoTitle"]

            return self.videoTitle
        except:
            raise
        
    def setVideoTitle(self, videoTitle):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("ID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")

            doc_ref = docs[0].reference
            doc_ref.update({"videoTitle": videoTitle})
            self.videoTitle = videoTitle

            return "Idea title set successfully"
        except:
            raise

    # API Key Functions
    def getGroqAPIKey(self):
        try:
            if not self.groqAPIKey:
                print("If called")
                self.groqAPIKey = os.getenv("GROQAPIKEY")  #Fetch this from DB later
            
            return self.groqAPIKey
        except:
            raise
        
    def getSerperAPIKey(self):
        try:
            # return self.serperAPIKey
            if not self.serperAPIKey:
                print("If called")
                self.serperAPIKey = os.getenv("SERPAPIKey")  #Fetch this from DB later
            
            return self.serperAPIKey
        except:
            raise

    def getTavilyAPIKey(self):
        if not self.tavilyAPIKey:
            print("If called")
            self.tavilyAPIKey = os.getenv("TAVILYAPIKEY")  #Fetch this from DB later
        
        return self.tavilyAPIKey

    def generateVideoTitles(self):
        try:
            self.getIdeaTitle()
            self.getIdeaDescription()

            print("Generating video titles based on idea...")
            sys_prompt="You are a professional youtube title generator who generates a youtube title that can get maximum audience attention, from the idea title and idea description that is provided."
            user_prompt=f"""Generate a YouTube video title based on the following video idea title and description:Video Idea Title: {self.ideaTitle} Video Idea Description: {self.ideaDescription} The title should meet the following criteria:Be accurate and clearly represent the video's content to ensure viewers do not stop watching mid-video.Preferably be 50-60 characters, and no more than 100 characters.Highlight the key benefit or value viewers will gain from the video.Include major keywords or search terms that are frequently searched by users related to this content.Use CAPS to emphasize one or two key words for impact, but avoid excessive use of all caps.Keep the title brief, direct, and to the point, as viewers may only see part of it on YouTube.Consider using brackets or parentheses to add additional context or perceived value, but don’t force it unless it adds clarity.Address challenges or pain points that the target audience has, and create a title that speaks directly to solving those issues.If the content relates to lists or rankings, create a listicle-style title (e.g., '5 Tips for Boosting Productivity').Add a sense of urgency to encourage immediate clicks, if appropriate.Know the target audience and tailor the title to appeal to them.Include a hook or special element to capture attention and distinguish the video from competing content.Clearly communicate what viewers can expect from the video and why it is special or unique. Output format:Return the titles as an array of strings that can be type casted using the python list function Output: Only generate 3 titles in the form of an array of strings in a single line and nothing else."""
            response=self.getLLMResponse(sys_prompt, user_prompt)
            return response
        except:
            raise
