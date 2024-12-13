from .synthetic_agent import SyntheticAgent

class ResearcherAgent(SyntheticAgent):
    def __init__(self, projectID):
        super().__init__(projectID)
        self.searchQuery = None
        self.customData = None
        self.masterSummary = None
        self.masterYTSummary = None
        self.masterWebpageSummary = None
        self.masterResearchPaperSummary = None
        self.masterCustomDataSummary = None

    # Search Query Functions
    def getSearchQuery(self):
        return self.searchQuery

    def setSearchQuery(self, query):
        self.searchQuery = query

    # Custom Data Functions
    def getCustomData(self):
        return self.customData

    def setCustomData(self, data):
        self.customData = data

    # Generate Search Query
    def generateSearchQuery(self):
        if self.ideaTitle:
            self.searchQuery = f"Research about {self.ideaTitle}"
            print(f"Generated search query: {self.searchQuery}")
        else:
            print("Idea title is required to generate a search query.")

    # Summary Functions
    def getMasterSummary(self):
        return self.masterSummary

    def generateMasterSummary(self):
        self.masterSummary = "Consolidated summary of all data."
        print("Master summary generated.")

    def getMasterYTSummary(self):
        return self.masterYTSummary

    def generateMasterYTSummary(self):
        self.masterYTSummary = "Summary of relevant YouTube content."
        print("YouTube summary generated.")

    def getMasterWebpageSummary(self):
        return self.masterWebpageSummary

    def generateMasterWebpageSummary(self):
        self.masterWebpageSummary = "Summary of relevant webpages."
        print("Webpage summary generated.")

    def getMasterResearchPaperSummary(self):
        return self.masterResearchPaperSummary

    def generateMasterResearchPaperSummary(self):
        self.masterResearchPaperSummary = "Summary of relevant research papers."
        print("Research paper summary generated.")

    def getCustomDataSummary(self):
        return self.masterCustomDataSummary

    def generateCustomDataSummary(self):
        self.masterCustomDataSummary = "Summary of custom data provided by the user."
        print("Custom data summary generated.")

# Example usage
if __name__ == "__main__":
    researcher = ResearcherAgent(projectID=5678)
    researcher.setIdeaTitle("Artificial Intelligence")
    researcher.generateSearchQuery()
    print(researcher.getSearchQuery())
    researcher.generateMasterSummary()
    print(researcher.getMasterSummary())
    researcher.generateMasterYTSummary()
    print(researcher.getMasterYTSummary())
    researcher.generateMasterWebpageSummary()
    print(researcher.getMasterWebpageSummary())
    researcher.generateMasterResearchPaperSummary()
    print(researcher.getMasterResearchPaperSummary())
    researcher.generateCustomDataSummary()
    print(researcher.getCustomDataSummary())
