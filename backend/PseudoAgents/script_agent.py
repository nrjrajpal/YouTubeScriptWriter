from .synthetic_agent import SyntheticAgent
from utils.firebase import db
import ast
from utils.exceptions import ProjectNotFoundError, KeyNotFoundError

PROJECT_COLLECTION_NAME = "TrialProject"

class ScriptAgent(SyntheticAgent):
    def __init__(self,  projectID, userEmail):
        print("proj", projectID)
        print("usr", userEmail)
        super().__init__(projectID=projectID, userEmail=userEmail)
        self.introduction = None
        self.selectedQuestions = None
        self.youTubeSummaries = None
        self.webpageSummaries = None
        self.researchPaperSummaries = None
        self.masterYouTubeSummary = None
        self.masterWebPageSummary = None
        self.masterResearchPaperSummary = None
        self.customDataSummary = None
        self.masterSummary = None
        self.script = None

    def generateQuestionsBasedOnTitle(self):
        try:
            self.getVideoTitle()
            self.getIdeaDescription()
            
            
            sys_prompt="You are a scriptwriting assistant, and your task is to generate introduction for a YouTube video based on the provided video title, idea description, and questions based on the video title."
            user_prompt=f"""
                Instructions:
                Imagine you're a viewer about to click on the video. Based on the title and description, think about what key questions or concerns you would have.
                Generate 5 distinct and concise questions that reflect a viewer's curiosity.
                The output must only contain short, distinct questions—no explanations or additional information. Each question should be clear and simple.
                Format the output exactly as a Python list of strings, with each question as a separate string.
                Video title: {self.videoTitle}
                Idea description: {self.ideaDescription}

                Output format:
                Return the questions as an array of strings that can be type casted using the python list function
                Output: Only generate 5 questions in the form of an array of strings in a single line and nothing else.
            """
            response = self.getLLMResponse(sys_prompt, user_prompt)
            questions = ast.literal_eval(response)
            
            return questions
        except:
            raise


    def getSelectedQuestions(self):
        try:
            if not self.selectedQuestions:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "selectedQuestions" not in record:
                    raise KeyNotFoundError("Selected questions are not set in the database.")

                self.selectedQuestions = record["selectedQuestions"]

            return self.selectedQuestions
        except:
            raise


    def setSelectedQuestions(self, selectedQuestions):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"selectedQuestions": selectedQuestions})
            self.selectedQuestions = selectedQuestions
            
            return "Selected questions set successfully"
        except:
            raise

    def generateIntroduction(self):
        try:
            self.getVideoTitle()
            self.getIdeaDescription()
            self.getSelectedQuestions()
            
            sys_prompt="You are a scriptwriting assistant, and your task is to generate 5 concise, engaging questions based on the provided video title and idea description. These questions should reflect potential viewers' expectations, concerns, and reasons to watch the video. Assume the role of a curious viewer who is considering watching the video and wants to know what value it offers."
            user_prompt=f"""
                Create a highly engaging introduction for a YouTube video based on the provided title, idea description, and viewer questions. The introduction should include the following:
                A captivating hook: Start with an attention-grabbing, one or two-line hook directly related to the video title and idea description. The hook should pose a compelling question or present an intriguing statement that makes viewers eager to watch.
                Context setting: Provide a brief but clear context for the video. Extend the expectations set by the title without overpromising, so viewers clearly understand what the video is about.
                Address viewer questions: Integrate answers to the 3 provided viewer questions in a concise and indirect way to assure viewers they’ll get what they expect from the video.
                Ensure the introduction flows naturally, maintains a conversational tone, and builds curiosity while reinforcing the value of watching the entire video.
                The output should include only the introduction text, formatted as a single paragraph. Avoid including any explanations or additional text.

                Input:
                Video Title: {self.videoTitle}
                Idea Description: {self.ideaDescription}
                Viewer Questions: {self.selectedQuestions}

                Output Format:
                Provide only the introduction in a single, well-written paragraph.
            """
            introduction = self.getLLMResponse(sys_prompt, user_prompt)
            self.setIntroduction(introduction)
            return introduction
        except:
            raise

    def getIntroduction(self):
        try:
            if not self.introduction:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "introduction" not in record:
                    raise KeyNotFoundError("Introduction is not set in the database.")

                self.introduction = record["introduction"]

            return self.introduction
        except:
            raise

    def setIntroduction(self, introduction):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"introduction": introduction})
            self.introduction = introduction
            
            return "Introduction set successfully"
        except:
            raise
        
    def generateSummaryFromRawData(self, rawData):
        try:
            self.getVideoTitle()
            self.getIdeaDescription()
            self.getIntroduction()
            
            
            sys_prompt="You are a professional summarizer tasked with extracting the most relevant and accurate information from raw data to create a detailed summary. Your summaries are concise, focused, and only include information derived from the input. You must not add or invent any details that are not explicitly provided in the raw data."
            user_prompt=f"""
                Using the provided video title, idea description, video introduction, and raw data, create a detailed and accurate summary. The summary should focus only on the information relevant to the video topic and script-writing requirements. Ensure the content is well-organized and avoids any assumptions or made-up details.

                Input:
                Video Title: {self.videoTitle}
                Idea Description: {self.ideaDescription}
                Video Introduction: {self.introduction}
                Raw Data: {rawData}
                Output Requirements:
                Use only the information provided in the raw data.
                Focus on extracting content directly relevant to the video's topic.
                Organize the summary into concise sections or paragraphs as needed.
                Output Format:
                A detailed summary in plain text of less than 1000 words, with no additional explanations or notes.
            """
            
            rawSummary = self.getLLMResponse(sys_prompt, user_prompt)
            return rawSummary
        except:
            raise
        
    
    def setYouTubeSummary(self, summary):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            project_doc_ref = docs[0].reference  # Document reference
            project_data = docs[0].to_dict()    # Document data (dictionary)
            
            summaries = project_data.get("youTubeSummaries", [])
            
            summaries.append(summary)
            project_doc_ref.update({"youTubeSummaries": summaries})
            
            return "YouTube Summary set successfully"
        except:
            raise

    def setWebPageSummary(self, summary):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            project_doc_ref = docs[0].reference  # Document reference
            project_data = docs[0].to_dict()    # Document data (dictionary)
            
            summaries = project_data.get("webpageSummaries", [])
            
            summaries.append(summary)
            project_doc_ref.update({"webpageSummaries": summaries})
            
            return "Web Page Summary set successfully"
        except:
            raise
        
    def setResearchPaperSummary(self, summary):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            project_doc_ref = docs[0].reference  # Document reference
            project_data = docs[0].to_dict()    # Document data (dictionary)
            
            summaries = project_data.get("researchPaperSummaries", [])
            
            summaries.append(summary)
            project_doc_ref.update({"researchPaperSummaries": summaries})
            
            return "Research Paper Summary set successfully"
        except:
            raise
        
    def getYouTubeSummaries(self):
        try:
            if not self.youTubeSummaries:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID..")
                record = docs[0].to_dict()
                if "youTubeSummaries" not in record:
                    raise KeyNotFoundError("YouTube Summaries are not set in the database.")
                self.youTubeSummaries = record["youTubeSummaries"]
            return self.youTubeSummaries
        except:
            raise
    
    def getWebPageSummaries(self):
        try:
            if not self.webpageSummaries:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                record = docs[0].to_dict()
                if "webpageSummaries" not in record:
                    raise KeyNotFoundError("Web Page Summaries are not set in the database.")
            
                self.webpageSummaries = record["webpageSummaries"]
            return self.webpageSummaries
        except:
            raise
    
    def getResearchPaperSummaries(self):
        try:
            if not self.researchPaperSummaries:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                record = docs[0].to_dict()
                if "researchPaperSummaries" not in record:
                    raise KeyNotFoundError("Research Paper Summaries are not set in the database.")
            
                self.researchPaperSummaries = record["researchPaperSummaries"]
            return self.researchPaperSummaries
        except:
            raise
        
    def generateSummaryFromSummaries(self, summaries):
        try:
            self.getVideoTitle()
            self.getIdeaDescription()
            self.getIntroduction()
            
            
            sys_prompt="You are an expert in synthesizing multiple summaries into a single, comprehensive main summary. Your job is to distil key points while ensuring no critical information is omitted. Only use the information provided in the input summaries; do not invent or assume any details."
            user_prompt=f"""
                Combine the provided summaries into one cohesive and comprehensive summary. Ensure that the final summary:

                Includes all critical details relevant to the video topic.
                Avoids redundancy while maintaining clarity and flow.
                Stays true to the content of the input summaries, without adding or making up any information.
                Input:
                Video Title: {self.videoTitle}
                Idea Description: {self.ideaDescription}
                Video Introduction: {self.introduction}
                Summaries: {summaries[0: 20000]}
                Output Requirements:
                Synthesize the provided summaries into a single, cohesive summary.
                Ensure clarity, focus, and logical organization of the final summary.
                Use only the content provided in the input summaries.
                Output Format:
                A single, well-organized summary in plain text, with no additional explanations or notes.
            """
            
            masterSummary = self.getLLMResponse(sys_prompt, user_prompt)
            return masterSummary
        except:
            raise
    
    def getMasterSummary(self):
        try:
            if not self.masterSummary:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "masterSummary" not in record:
                    raise KeyNotFoundError("Master Summary is not set in the database.")

                self.masterSummary = record["masterSummary"]

            return self.masterSummary
        except:
            raise

    def setMasterSummary(self, masterSummary):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"masterSummary": masterSummary})
            self.masterSummary = masterSummary
            
            return "Master Summary set successfully"
        except:
            raise

    def getMasterYouTubeSummary(self):
        try:
            if not self.masterYouTubeSummary:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "masterYouTubeSummary" not in record:
                    raise KeyNotFoundError("Master YouTube Summary is not set in the database.")

                self.masterYouTubeSummary = record["masterYouTubeSummary"]

            return self.masterYouTubeSummary
        except:
            print("Error in get Master YT summary")
            raise

    def setMasterYouTubeSummary(self, masterYouTubeSummary):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"masterYouTubeSummary": masterYouTubeSummary})
            self.masterYouTubeSummary = masterYouTubeSummary
            
            return "Master YouTube Summary set successfully"
        except:
            print("Error in set Master YT summary")
            raise

    def getMasterWebPageSummary(self):
        try:
            if not self.masterWebPageSummary:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "masterWebPageSummary" not in record:
                    raise KeyNotFoundError("Master Web Page Summary is not set in the database.")

                self.masterWebPageSummary = record["masterWebPageSummary"]

            return self.masterWebPageSummary
        except:
            raise

    def setMasterWebPageSummary(self, masterWebPageSummary):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"masterWebPageSummary": masterWebPageSummary})
            self.masterWebPageSummary = masterWebPageSummary
            
            return "Master Web Page Summary set successfully"
        except:
            raise

    def getMasterResearchPaperSummary(self):
        try:
            if not self.masterResearchPaperSummary:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "masterResearchPaperSummary" not in record:
                    raise KeyNotFoundError("Master Research Paper Summary is not set in the database.")

                self.masterResearchPaperSummary = record["masterResearchPaperSummary"]

            return self.masterResearchPaperSummary
        except:
            raise

    def setMasterResearchPaperSummary(self, masterResearchPaperSummary):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"masterResearchPaperSummary": masterResearchPaperSummary})
            self.masterResearchPaperSummary = masterResearchPaperSummary
            
            return "Master Research Paper Summary set successfully"
        except:
            raise    
    
    def getCustomDataSummary(self):
        try:
            if not self.customDataSummary:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "customDataSummary" not in record:
                    raise KeyNotFoundError("Custom Data Summary is not set in the database.")

                self.customDataSummary = record["customDataSummary"]

            return self.customDataSummary
        except:
            raise

    def setCustomDataSummary(self, customDataSummary):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"customDataSummary": customDataSummary})
            self.customDataSummary = customDataSummary
            
            return "Master YouTube Summary set successfully"
        except:
            raise

    def generateScript(self):
        try:
            self.getVideoTitle()
            self.getIdeaDescription()
            self.getIntroduction()
            self.getMasterSummary()
            
            
            sys_prompt="You are an expert scriptwriter tasked with creating engaging YouTube scripts designed to maximize audience retention. Your scripts follow a structured format with well-defined parts/chapters, each including hooks, build, tension, and payouts. You base your scripts entirely on the provided inputs, ensuring no additional or made-up information is included."
            user_prompt=f"""
                Using the provided video title, idea description, video introduction, and information summary, create a detailed script for a YouTube video. The script should:
                Start with the provided introduction verbatim.
                Be divided into logical sections or chapters.
                Include hooks at the beginning of each section to keep the audience engaged.
                Build tension and excitement, leading to a satisfying payout for the viewer at the end of each section.
                End with a resolution that ties back to the introduction's hook and leaves the audience feeling satisfied.
                Feature a climax where the conflict or primary question is resolved.
                Input:
                Video Title: {self.videoTitle}
                Idea Description: {self.ideaDescription}
                Video Introduction: {self.introduction}
                Information Summary: {self.masterSummary}
                Output Requirements:
                The script must use only the information provided in the summary.
                Hook: A compelling line to grab the viewer's attention.
                Each section should follow the structure:
                Content: Relevant details with gradual build and tension.
                Payout: Provide the answer or resolution for that section.
                The resolution should wrap up the story and relate to the introduction's hook.
                The climax should be the most exciting part, resolving the primary conflict or question.
                Output Format:
                The script should be divided into sections with clear headings, like this:
                Introduction  
                (Insert video introduction)  

                Chapter 1: (Insert chapter title)  
                **Hook**: (Insert hook for chapter)  
                (Insert content with build and tension)  
                **Payout**: (Insert resolution for this chapter)  

                Chapter 2: (Insert chapter title)  
                **Hook**: (Insert hook for chapter)  
                (Insert content with build and tension)  
                **Payout**: (Insert resolution for this chapter)  
                .
                .
                .
                Chapter n: (Insert chapter title)  
                **Hook**: (Insert hook for chapter)  
                (Insert content with build and tension)  
                **Payout**: (Insert resolution for this chapter)  

                Climax  
                (Insert the most exciting part of the script where the conflict is resolved)  

                Resolution  
                (Tie back to the introduction and leave the audience feeling satisfied) 
            """
            masterSummary = self.getLLMResponse(sys_prompt, user_prompt)
            return masterSummary
        except:
            raise
    
    def getScript(self):
        try:
            if not self.script:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                record = docs[0].to_dict()
                if "script" not in record:
                    raise KeyNotFoundError("Script is not set in the database.")
                self.script = record["script"]
            return self.script
        except:
            raise

    def setScript(self, script):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"script": script})
            self.script = script
            
            return "Script set successfully"
        except:
            raise