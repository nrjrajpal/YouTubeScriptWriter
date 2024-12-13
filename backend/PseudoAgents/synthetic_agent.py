from groq import Groq
from config import Config               
import os
from dotenv import load_dotenv
load_dotenv()  

class SyntheticAgent:
    def __init__(self, projectID):
        self.projectID = projectID
        self.ideaTitle = "Master Time Management: 5 Simple Strategies for Productivity"
        self.ideaDescription = "This video explores five actionable time management strategies that can significantly boost your productivity. These strategies focus on breaking down tasks, prioritizing your day, and overcoming procrastination. The video will also dive into the psychological principles behind why these techniques work and how you can apply them to both your personal and professional life. Whether you're a student, professional, or entrepreneur, these tips will help you make the most of your time and achieve your goals."
        self.videoTitle = None
        self.groqAPIKey = None
        self.serperAPIKey = None
        self.tavilyAPIKey = None

    # Placeholder database operations
    # def _fetch_from_db(self, field):
    #     print(f"Fetching {field} for projectID {self.projectID} from DB...")
    #     return "Sample Data"

    # def _update_to_db(self, field, value):
    #     print(f"Updating {field} to '{value}' for projectID {self.projectID} in DB...")

    # LLM Response Function
    def getLLMResponse(self, system_query, user_query, model="llama-3.1-70b-versatile"):
        # print(f"Generating response for prompt: {prompt}")
        # return f"Generated response for: {prompt}"

        client = Groq(api_key=self.getGroqAPIKey())
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_query
                },
                {
                    "role": "user",
                    "content": user_query,
                }
            ],
            model=model,
        )

        return chat_completion.choices[0].message.content

    # Idea Title Functions
    def getIdeaTitle(self):
        if not self.ideaTitle:
            print("If called")
            self.ideaTitle = self._fetch_from_db("ideaTitle") #Fetch this from DB later
        
        return self.ideaTitle

    def setIdeaTitle(self,newIdeaTitle):
        self.ideaTitle = newIdeaTitle   #Set this on DB later
        
    # Idea Description Functions
    def getIdeaDescription(self):
        if not self.ideaDescription:
            print("If Called")
            self.ideaDescription = self._fetch_from_db("ideaDescription") #Fetch this from DB later
        
        
        return self.ideaDescription

    def setIdeaDescription(self, newDescription):
        self.ideaDescription = newDescription #Set this on DB later

    # Video Title Functions
    def getVideoTitle(self):
        if not self.videoTitle:
            print("If called")
            self.videoTitle = self._fetch_from_db("videoTitle") 
        
        return self.videoTitle

    def setVideoTitle(self, newVideoTitle):
        self.videoTitle = newVideoTitle #Set this on DB later

    # API Key Functions
    def getGroqAPIKey(self):
        if not self.groqAPIKey:
            print("If called")
            self.groqAPIKey = os.getenv("GROQAPIKEY")  #Fetch this from DB later
        
        return self.groqAPIKey
        
    def getSerperAPIKey(self):
        # return self.serperAPIKey
        if not self.serperAPIKey:
            print("If called")
            self.serperAPIKey = os.getenv("SERPAPIKey")  #Fetch this from DB later
        
        return self.serperAPIKey

    def getTavilyAPIKey(self):
        if not self.tavilyAPIKey:
            print("If called")
            self.tavilyAPIKey = os.getenv("TAVILYAPIKEY")  #Fetch this from DB later
        
        return self.tavilyAPIKey

    # Generate Video Titles
    def generateVideoTitles(self):
        if not self.ideaTitle or not self.ideaDescription:
            print("Idea title and description are required to generate video titles.")
            return []

        print("Generating video titles based on idea...")
        # videoTitles = [
        #     f"{self.ideaTitle} - Explained",
        #     f"The Future of {self.ideaTitle}",
        #     f"{self.ideaTitle}: What You Need to Know",
        #     f"{self.ideaTitle} and Beyond",
        #     f"How {self.ideaDescription} Will Change the World"
        # ]
        # response=self.getLLMresponse()
        # videoTitles = ast.literal_eval(response)
        #LLM CAll
        # return videoTitles
