from .researcher_agent import ResearcherAgent
from .synthetic_agent import SyntheticAgent
from utils.firebase import db
from flask import jsonify
from utils.exceptions import ProjectNotFoundError, KeyNotFoundError

PROJECT_COLLECTION_NAME = "TrialProject"

class CustomDataAgent(ResearcherAgent):
    def __init__(self,  projectID, userEmail):
        super().__init__( projectID, userEmail)
        self.customData = None 

    # Video ID Functions
    def getCustomData(self):
        try: 
            if not self.customData:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No Project found with this ID.")

                record = docs[0].to_dict()

                if "customData" not in record:
                    raise KeyNotFoundError("No custom data is present in the database.")

                self.customData = record["customData"]

            return self.customData
        except:
            raise

    def setCustomData(self, customData):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"customData": customData})
            self.customData = customData
            
            return "Custom Data set successfully"
        except:
            raise
