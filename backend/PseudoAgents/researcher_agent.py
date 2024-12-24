from .synthetic_agent import SyntheticAgent
from utils.firebase import db
from utils.exceptions import ProjectNotFoundError, KeyNotFoundError

PROJECT_COLLECTION_NAME = "TrialProject"

class ResearcherAgent(SyntheticAgent):
    def __init__(self,  projectID, userEmail):
        super().__init__( projectID, userEmail)
        self.searchQuery = None
        self.__masterSummary = None
        self.__masterYTSummary = None
        self.__masterWebpageSummary = None
        self.__masterResearchPaperSummary = None
        self.__customDataSummary = None

    # Search Query Functions
    def getSearchQuery(self):
        try:
            if not self.searchQuery:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "searchQuery" not in record:
                    raise KeyNotFoundError("Search query is not set in the database.")

                self.searchQuery = record["searchQuery"]

            return self.searchQuery
        except:
            raise

    def setSearchQuery(self, query):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"searchQuery": query})
            self.searchQuery = query
            
            return "Search query set successfully"
        except:
            raise

    def generateSearchQuery(self):
        try:
            self.getVideoTitle()
            self.getIdeaDescription()
            
            print("Generating SearchQuery based on idea...")
            sys_prompt="You are a professional assistant skilled at generating precise and comprehensive search queries to gather information for YouTube script creation. Your search queries must be highly relevant, concise, and optimized for retrieving information from YouTube videos, web pages, and research papers."
            user_prompt=f"""
                Analyze the following video title and idea description to generate a single, precise search query. The query will be used to gather information for creating a YouTube script. Ensure the search query:
                - Covers the main topic comprehensively.
                - Uses carefully chosen keywords in a single, straightforward query (avoid complex OR statements).
                - Is well-suited to retrieving diverse and relevant resources.
                - Avoids any additional text or explanation and only outputs the search query.

                Video title: {self.videoTitle}  
                Idea description: {self.ideaDescription}

                Output format: A single, well-constructed search query as plain text. Generate only one query and nothing else.
            """
            response=self.getLLMResponse(sys_prompt, user_prompt)
            return response
        except:
            raise

    # Summary Functions
    def generateSummary(self):
        pass

    def __getMasterSummary(self):
        pass
        # if not self.masterSummary:
        #     print("If called")
        #     self.masterSummary = "Consolidated summary of all data."
        # return self.masterSummary

    def __generateMasterSummary(self):
        pass
        # self.masterSummary = "Consolidated summary of all data."
        # print("Master summary generated.")

    def __getMasterYTSummary(self):
        pass
        # if not self.masterYTSummary:
        #     print("If called")
        #     self.masterYTSummary = "Summary of relevant YouTube content."
        # return self.masterYTSummary

    def __generateMasterYTSummary(self):
        pass
        # self.masterYTSummary = "Summary of relevant YouTube content."
        # print("YouTube summary generated.")

    def __getMasterWebpageSummary(self):
        pass
        # if not self.masterWebpageSummary:
        #     print("If called")
        #     self.masterWebpageSummary = "Summary of relevant webpages."
        # return self.masterWebpageSummary

    def __generateMasterWebpageSummary(self):
        pass
        # self.masterWebpageSummary = "Summary of relevant webpages."
        # print("Webpage summary generated.")

    def __getMasterResearchPaperSummary(self):
        pass
        # if not self.masterResearchPaperSummary:
        #     print("If called")
        #     self.masterResearchPaperSummary = "Summary of relevant research papers."
        # return self.masterResearchPaperSummary

    def __generateMasterResearchPaperSummary(self):
        pass
        # self.masterResearchPaperSummary = "Summary of relevant research papers."
        # print("Research paper summary generated.")

    def __getCustomDataSummary(self):
        pass
        # if not self.customDataSummary:
        #     print("If called")
        #     self.customDataSummary = "Summary of custom data provided by the user."
        # return self.customDataSummary

    def __generateCustomDataSummary(self):
        pass
        # self.customDataSummary = "Summary of custom data provided by the user."
        # print("Custom data summary generated.")

    # Fetch all summaries based on the content type
    def __getAllSummaries(self, type):
        pass
        if type == "youtube":
            pass
            # return self.getMasterYTSummary()
        elif type == "webpage":
            pass
            # return self.getMasterWebpageSummary()
        elif type == "researchpaper":
            pass
            # return self.getMasterResearchPaperSummary()
        elif type == "customdata":
            pass
            # return self.getCustomDataSummary()
        else:
            pass
            # raise ValueError("Invalid content type. Valid types: 'youtube', 'webpage', 'researchpaper', 'customdata'.")
