from .researcher_agent import ResearcherAgent
from .synthetic_agent import SyntheticAgent
from google.cloud import firestore
from flask import jsonify
from utils.firebase import db
import os
import requests
import json
import time
from groq import Groq
from tavily import TavilyClient
from utils.exceptions import ProjectNotFoundError, KeyNotFoundError,ContentNotFoundError
from dotenv import load_dotenv
load_dotenv()

PROJECT_COLLECTION_NAME = "TrialProject"

class ResearchPaperAgent(ResearcherAgent):
    def __init__(self, projectID):
        super().__init__(projectID)
        self.researchPaperData = []  # Initialize research paper URLs and metadata as an empty list
        self.researchPaperContent = []  # Initialize research paper content (not stored in DB)
        self.researchPaperSummaries = []  # Initialize research paper summaries as an empty list

    # Getter for research paper URLs and metadata
    def getResearchPaperUrlsAndMetadata(self):
        try: 
            print("self.researchPaperData: ", self.researchPaperData)
            if not self.researchPaperData:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("Project with the given id doesn't exist.")

                record = docs[0].to_dict()
                print("RECORD ", record)

                if "researchPaperData" not in record:
                    raise KeyNotFoundError("researchPaperData is not set in the database.")

                self.researchPaperData = record["researchPaperData"]
                print(record["researchPaperData"])

            return self.researchPaperData 
        except:
            raise

    def setResearchPaperUrlsAndMetadata(self, researchPaperData):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")

            doc_ref = docs[0].reference
            doc_ref.update({"researchPaperData": researchPaperData})
            self.researchPaperData = researchPaperData

            return "Research Paper Data set successfully"
        except:
            raise

    # Fetch research papers from the web
    def fetchResearchPaperContent(self, url):
        try:
            tavily_client = TavilyClient(api_key=os.getenv("TAVILYAPIKEY"))
            # paper_urls = [paper["paper_url"] for paper in self.researchPaperUrlsAndMetadata]
            # final_research_formatted_content = []
            # Fetch raw data from Tavily
            response = tavily_client.extract(urls=[url])
            if not response["results"]:
                raise ContentNotFoundError("Web content for the given URL not available")
            return response["results"][0]["raw_content"]
        # [0]["raw_content"]
            # for output in response["results"]:
            #     raw = output["raw_content"]
            #     # if len(raw) > 50000:
            #     # raw = raw[:50000]

            #     for formatted_output in self.researchPaperUrlsAndMetadata:
            #         if output["url"] == formatted_output["paper_url"]:
            #             formatted_output["paper_raw_content"] = raw
            #             print(f"Processed raw data for: {output['url']}")
            #             break

            # # Filter valid content
            # for formatted_output in self.researchPaperUrlsAndMetadata:
            #     if "paper_raw_content" in formatted_output and formatted_output["paper_raw_content"]:
            #         final_research_formatted_content.append(formatted_output)

            # print("\n\n\n\nFinal raw research content size: ", len(final_research_formatted_content))
            # print("\n\n\n\nRaw research content formed:\n", final_research_formatted_content)

            # # Update the agent's data members
            # self.researchPaperContent = [
            #     {"url": paper["paper_url"], "content": paper["paper_raw_content"]}
            #     for paper in final_research_formatted_content
            # ]

        except:
            raise

    
    def fetchResearchPaperFromWeb(self):
        try:
            query = self.getSearchQuery()
            # print("search Query" + query)
            # Fetch paper links
            url = "https://google.serper.dev/scholar"
            payload = json.dumps({"q": query+" filetype:pdf"})
            headers = {
                'X-API-KEY': os.getenv("SERPAPIKEY"),
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()

            researchPaperData = []
            for i in range(0, 3):
                researchPaperData.append({
                    "paper_title": data["organic"][i]["title"],
                    "paper_url": data["organic"][i]["link"]
                })
                # print("Added Paper: ", data["organic"][i]["link"])

            # print("\n\n\n\nPapers to use:\n", researchPaperData)
            return researchPaperData

            # Update the agent's URLs and metadata
        except Exception as e:
            raise
            
    # Generate summary (inherited from ResearcherAgent)
    def generateSummary(self):
        pass