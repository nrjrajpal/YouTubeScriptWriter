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
from utils.exceptions import ProjectNotFoundError, KeyNotFoundError, ContentNotFoundError
from dotenv import load_dotenv
load_dotenv()

PROJECT_COLLECTION_NAME = "TrialProject"

class WebpageAgent(ResearcherAgent):
    def __init__(self,  projectID, userEmail):
        super().__init__( projectID, userEmail)
        self.webPageURLsAndMetadata = []  
        self.webPageData = []  
        self.webPageSummaries = []  

    # Getter for research paper URLs and metadata
    def fetchWebPagesFromWeb(self):
        try:
            print("TAVILY API KEY: ",self.getTavilyAPIKey())
            tavily_client = TavilyClient(api_key=self.getTavilyAPIKey())
            query = self.getSearchQuery()
            website_formatted_content = []
            response = tavily_client.search(query=query, search_depth="advanced", max_results=5, include_raw_content=True)
            count = 0
            for i in range(0, len(response['results'])):
                if (count < 3) and (not response['results'][i]['raw_content'] == None):
                    print("\nProcessed: ", response['results'][i]['url'])
                    raw_content = response['results'][i]['raw_content']
                    if len(raw_content) > 50000:
                        raw_content = raw_content[:50000]
                    print("Length Of Raw Content: \n", len(raw_content))
                    website_formatted_content.append({
                        'webpage_url': response['results'][i]['url'],
                        'webpage_title': response['results'][i]['title'],
                        'webpage_raw_content': raw_content.replace("\n"," "),
                    })
                    count += 1
                
                else:
                    print("Skipped: ", response['results'][i]['url'])
            return website_formatted_content
        except:
            raise

    def getWebPageData(self):
        try: 
            if not self.webPageData:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("Project with the given id doesn't exist.")

                record = docs[0].to_dict()
                # print("RECORD ", record)

                if "webPageData" not in record:
                    raise KeyNotFoundError("webPageData is not set in the database.")

                self.webPageData = record["webPageData"]
                # print(record["webPageData"])

            return self.webPageData 
        except:
            raise

    def setWebpageData(self, webPageData):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")

            doc_ref = docs[0].reference
            doc_ref.update({"webPageData": webPageData})
            self.webPageData = webPageData

            return "Webpage data set successfully"
        except:
            raise

    def fetchWebPageRawContent(self, url):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("Project with the given id doesn't exist.")
           
            dbrecord = docs[0].to_dict()
            # doc_ref = docs[0].reference

            if "webPageData" not in dbrecord:
                raise KeyNotFoundError("webPageData is not set in the database.")

            web_page_data = dbrecord["webPageData"]
            for record in web_page_data:
                if record["webpage_url"] == url and record["webpage_raw_content"] == "N/A":
                    tavily_client = TavilyClient(api_key=self.getTavilyAPIKey())
                    response = tavily_client.extract(urls=[url])
                    if response["results"]:
                        for output in response["results"]:
                            raw = output["raw_content"]
                            if len(raw) > 20000:
                                raw = raw[:20000]
                        # record["raw_content"] = raw
                        # doc_ref.update({"webPageData": web_page_data})
                        return raw
                        # return response["results"][0]["raw_content"]
                elif record["webpage_url"] == url and record["webpage_raw_content"] != "N/A":
                    return record["webpage_raw_content"]
           
            return "URL: " + url + " doesnt exist in the database"
        except:
            raise
            
    # Generate summary (inherited from ResearcherAgent)
    def generateSummary(self):
        pass