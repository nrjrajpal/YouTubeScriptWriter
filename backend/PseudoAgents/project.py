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
        self.nextStage=None
        
    def createProject(self,projectIdeaTitle,projectIdeaDescription,userEmail):
        try:
            user_collection_ref = db.collection(USER_COLLECTION_NAME)            
            
            user_docs = user_collection_ref.where("userEmail", "==", userEmail).get()
            if not user_docs:
                raise UserNotFoundError("No user found with this email.")
            
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            projectID = ""
            while True:
                projectID=''.join(random.choices(string.ascii_letters + string.digits, k=7))
                existing_record = collection_ref.where("projectID", "==", projectID).get()
                if not existing_record:
                    break
            
            self.projectID = projectID
            # Add a new record
            doc_ref = collection_ref.document()
            projectDetails={
                "projectID": self.projectID,
                "ideaTitle":projectIdeaTitle,
                "ideaDescription":projectIdeaDescription,
                "dateCreated":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "ownerEmail":userEmail,
                "nextStage":"videoTitle"
            }
            doc_ref.set(projectDetails)
            
            user_doc_ref = user_docs[0].reference  # Document reference
            user_data = user_docs[0].to_dict()    # Document data (dictionary)
            # print("user_doc_ref", user_doc_ref, type(user_doc_ref))
            
            ownedProjects = user_data.get("ownedProjects", [])
            
            if self.projectID not in ownedProjects:
                ownedProjects.append(self.projectID)
            print("ownedProjects old:", user_data.get("ownedProjects", []))
            print("ownedProjects new:", ownedProjects)
            
            print("ownedProjects new", ownedProjects, type(ownedProjects))
            # print("ownedProjects", ownedProjects, type(ownedProjects))
            
            user_doc_ref.update({"ownedProjects": ownedProjects})
            
            return projectDetails
        except:
            raise
        
    def deleteProject(self, projectID, userEmail):
        try:
            user_collection_ref = db.collection(USER_COLLECTION_NAME)
            
            # Get the user document using the email
            user_docs = user_collection_ref.where("userEmail", "==", userEmail).get()
            if not user_docs:
                raise UserNotFoundError("No user found with this email.")
            
            # Get the project collection reference
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            
            # Check if the project exists
            project_docs = collection_ref.where("projectID", "==", projectID).get()
            if not project_docs:
                raise ProjectNotFoundError("No project found with this projectID.")
            
            # Delete the project from the project collection
            project_doc_ref = project_docs[0].reference
            project_doc_ref.delete()
            
            # Update the user's ownedProjects array to remove the deleted projectID
            user_doc_ref = user_docs[0].reference  # Document reference
            user_data = user_docs[0].to_dict()    # Document data (dictionary)
            
            ownedProjects = user_data.get("ownedProjects", [])
            
            if projectID in ownedProjects:
                ownedProjects.remove(projectID)
            
            print("ownedProjects old:", user_data.get("ownedProjects", []))
            print("ownedProjects new:", ownedProjects)
            
            user_doc_ref.update({"ownedProjects": ownedProjects})
            
            return {"message": "Project deleted successfully.", "projectID": projectID}
        
        except Exception as e:
            print(f"Error deleting project: {e}")
            raise

    # def deleteProject(self):
    #     collection_ref = db.collection(PROJECT_COLLECTION_NAME)
    #     docs = collection_ref.where("projectID", "==", self.projectID).get()
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
                docs = collection_ref.where("projectID", "==", self.projectID).get()
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
                docs = collection_ref.where("projectID", "==", self.projectID).get()
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
                docs = collection_ref.where("projectID", "==", self.projectID).get()
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
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No Project found with this ID.")

                record = docs[0].to_dict()

                if "ownerEmail" not in record:
                    raise KeyNotFoundError("Project Owner Email is not set in the database.")

                self.projectOwnerEmail = record["ownerEmail"]

            return self.projectOwnerEmail 
        except:
            raise
        
    def getProjectNextState(self):
        try: 
            if not self.nextStage:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No Project found with this ID.")

                record = docs[0].to_dict()

                if "nextStage" not in record:
                    raise KeyNotFoundError("Next Stage is not set in the database.")

                self.nextStage = record["nextStage"]

            return self.nextStage 
        except:
            raise
    
    def getProjectDetails(self,userEmail):
        try:
            collection_ref = db.collection(USER_COLLECTION_NAME)
            docs = collection_ref.where("userEmail", "==", userEmail).get()
            if not docs:
                raise UserNotFoundError("No user found with this email.")
            
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No valid project found")

            record = docs[0].to_dict()
            if "ownerEmail" not in record:
                raise KeyNotFoundError("Owner email is not set for this project in the database.")
            if record["ownerEmail"]!=userEmail:
                raise EmailMismatchError("Email not matching with project owner's email")
            result = {
                "projectID": self.projectID,
                "ideaTitle": record["ideaTitle"],
                "ideaDescription": record["ideaDescription"],
                "dateCreated": record["dateCreated"]
            }

            return result
        except:
            raise

