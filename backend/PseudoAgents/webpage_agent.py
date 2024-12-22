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
        self.webPageContent = []  
        self.webPageSummaries = []  

    # Getter for research paper URLs and metadata
    def fetchWebPagesFromWeb(self):
        try:
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

            
    # Generate summary (inherited from ResearcherAgent)
    def generateSummary(self):
        pass