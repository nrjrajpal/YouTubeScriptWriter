from .synthetic_agent import SyntheticAgent

class ResearcherAgent(SyntheticAgent):
    def __init__(self, projectID):
        super().__init__(projectID)
        self.searchQuery = None
        self.__masterSummary = None
        self.__masterYTSummary = None
        self.__masterWebpageSummary = None
        self.__masterResearchPaperSummary = None
        self.__customDataSummary = None

    # Search Query Functions
    def getSearchQuery(self):
        if not self.searchQuery:
            print("If called")
            self.searchQuery = self._fetch_from_db("searchQuery")  # Fetch from DB later
        return self.searchQuery

    def __setSearchQuery(self, query):
        self.searchQuery = query  # Update in DB later

    def __generateSearchQuery(self):
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
        response=self.getLLMResponse(sys_prompt,user_prompt)
        return response

    # Summary Functions
    def generateSummary(self):
        pass

    def __getMasterSummary(self):
        if not self.masterSummary:
            print("If called")
            self.masterSummary = "Consolidated summary of all data."
        return self.masterSummary

    def __generateMasterSummary(self):
        self.masterSummary = "Consolidated summary of all data."
        print("Master summary generated.")

    def __getMasterYTSummary(self):
        if not self.masterYTSummary:
            print("If called")
            self.masterYTSummary = "Summary of relevant YouTube content."
        return self.masterYTSummary

    def __generateMasterYTSummary(self):
        self.masterYTSummary = "Summary of relevant YouTube content."
        print("YouTube summary generated.")

    def __getMasterWebpageSummary(self):
        if not self.masterWebpageSummary:
            print("If called")
            self.masterWebpageSummary = "Summary of relevant webpages."
        return self.masterWebpageSummary

    def __generateMasterWebpageSummary(self):
        self.masterWebpageSummary = "Summary of relevant webpages."
        print("Webpage summary generated.")

    def __getMasterResearchPaperSummary(self):
        if not self.masterResearchPaperSummary:
            print("If called")
            self.masterResearchPaperSummary = "Summary of relevant research papers."
        return self.masterResearchPaperSummary

    def __generateMasterResearchPaperSummary(self):
        self.masterResearchPaperSummary = "Summary of relevant research papers."
        print("Research paper summary generated.")

    def __getCustomDataSummary(self):
        if not self.customDataSummary:
            print("If called")
            self.customDataSummary = "Summary of custom data provided by the user."
        return self.customDataSummary

    def __generateCustomDataSummary(self):
        self.customDataSummary = "Summary of custom data provided by the user."
        print("Custom data summary generated.")

    # Fetch all summaries based on the content type
    def __getAllSummaries(self, type):
        if type == "youtube":
            return self.getMasterYTSummary()
        elif type == "webpage":
            return self.getMasterWebpageSummary()
        elif type == "researchpaper":
            return self.getMasterResearchPaperSummary()
        elif type == "customdata":
            return self.getCustomDataSummary()
        else:
            raise ValueError("Invalid content type. Valid types: 'youtube', 'webpage', 'researchpaper', 'customdata'.")
