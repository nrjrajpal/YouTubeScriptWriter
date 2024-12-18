from utils.firebase import db
from utils.exceptions import KeyNotFoundError,ProjectNotFoundError,UserNotFoundError,EmailMismatchError
import random
import string
from datetime import datetime

PROJECT_COLLECTION_NAME = "TrialProject"
USER_COLLECTION_NAME="TrialUser"

class Project:
    def __init__(self,projectID):
        self.projectID=projectID
        self.projectIdeaTitle=None
        self.projectIdeaDescription=None
        self.projectDateCreated=None
        self.projectOwnerEmail=None
        
    def createProject(self,projectIdeaTitle,projectIdeaDescription,userEmail):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            projectID = ""
            while True:
                projectID=''.join(random.choices(string.ascii_letters + string.digits, k=7))
                existing_record = collection_ref.where("ID", "==", projectID).get()
                if not existing_record:
                    break
            
            self.projectID = projectID
            # Add a new record
            doc_ref = collection_ref.document()
            projectDetails={
                "ID": self.projectID,
                "ideaTitle":projectIdeaTitle,
                "ideaDescription":projectIdeaDescription,
                "dateCreated":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "ownerEmail":userEmail
            }
            doc_ref.set(projectDetails)
            return projectDetails
        except:
            raise
        
    # def deleteProject(self):
    #     collection_ref = db.collection(PROJECT_COLLECTION_NAME)
    #     docs = collection_ref.where("ID", "==", self.projectID).get()
    #     if not docs:
    #         raise ProjectNotFoundError("No Project found with this ID.")

    #     # Delete the first matching record
    #     doc_ref = docs[0].reference
    #     doc_ref.delete()
    #     return "Project deleted successfully"
    
    def getProjectIdeaTitle(self):
        try: 
            if not self.projectIdeaTitle:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("ID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No Project found with this ID.")

                record = docs[0].to_dict()

                if "ideaTitle" not in record:
                    raise KeyNotFoundError("Project Idea Title is not set in the database.")

                self.projectIdeaTitle = record["ideaTitle"]

            return self.projectIdeaTitle 
        except:
            raise
    
    def getProjectIdeaDescription(self):
        try: 
            if not self.projectIdeaDescription:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("ID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No Project found with this ID.")

                record = docs[0].to_dict()

                if "ideaDescription" not in record:
                    raise KeyNotFoundError("Project Idea Description is not set in the database.")

                self.projectIdeaDescription = record["ideaDescription"]

            return self.projectIdeaDescription 
        except:
            raise
        
    def getProjectDateCreated(self):
        try: 
            if not self.projectDateCreated:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("ID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No Project found with this ID.")

                record = docs[0].to_dict()

                if "dateCreated" not in record:
                    raise KeyNotFoundError("Project Date Created is not set in the database.")

                self.projectDateCreated = record["dateCreated"]

            return self.projectDateCreated 
        except:
            raise
        
    def getProjectOwnerEmail(self):
        try: 
            if not self.projectOwnerEmail:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("ID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No Project found with this ID.")

                record = docs[0].to_dict()

                if "ownerEmail" not in record:
                    raise KeyNotFoundError("Project Owner Email is not set in the database.")

                self.projectOwnerEmail = record["ownerEmail"]

            return self.projectOwnerEmail 
        except:
            raise
        
    def getProjectDetails(self,userEmail,projectID):
        try:
            collection_ref = db.collection(USER_COLLECTION_NAME)
            docs = collection_ref.where("userEmail", "==", userEmail).get()
            if not docs:
                raise UserNotFoundError("No user found with this email.")
            
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("ID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No valid project found")

            record = docs[0].to_dict()
            if "ownerEmail" not in record:
                raise KeyNotFoundError("Owner email is not set for this project in the database.")
            if record["ownerEmail"]!=userEmail:
                raise EmailMismatchError("Email not matching with project owner's email")
            result = {
                "projectIdeaTitle": record["ideaTitle"],
                "projectIdeaDescription": record["ideaDescription"],
                "projectDateCreated": record["dateCreated"]
            }

            return result
        except:
            raise

