from utils.firebase import db
from utils.exceptions import KeyNotFoundError, UserNotFoundError, NoProjectsExistError
from .project import Project

# from youtubesearchpython import Channel

USER_COLLECTION_NAME = "TrialUser"

class User:
    def __init__(self,userEmail):
        self.userEmail = userEmail
        self.userID = None
        self.channelID = None
        self.groqAPIKey = None
        self.serperAPIKey = None
        self.tavilyAPIKey = None
        self.ownedProjects = []

    def createUser(self, userID):
        try:
            collection_ref = db.collection(USER_COLLECTION_NAME)
            docs = collection_ref.where("userEmail", "==", self.userEmail).get()
            if docs:
                raise UserNotFoundError("User already exists with this email.")
            
            doc_ref = collection_ref.document()
            doc_ref.set({"userEmail": self.userEmail, "userID": userID})

            return "User created successfully"
        except:
            raise
    # def getChannelID(self):
    #     try: 
    #         if not self.channelID:
    #             collection_ref = db.collection(USER_COLLECTION_NAME)
    #             docs = collection_ref.where("userEmail", "==", self.userEmail).get()
    #             if not docs:
    #                 raise UserNotFoundError("No user found with this email.")

    #             record = docs[0].to_dict()

    #             if "channelID" not in record:
    #                 raise KeyNotFoundError("Channel ID is not set in the database.")

    #             self.channelID = record["channelID"]

    #         return self.channelID 
    #     except:
    #         raise

    # def setChannelID(self, channelID):
    #     try:
    #         collection_ref = db.collection(USER_COLLECTION_NAME)
    #         docs = collection_ref.where("userEmail", "==", self.userEmail).get()
    #         if not docs:
    #             raise UserNotFoundError("No user found with this email.")
            
    #         doc_ref = docs[0].reference
    #         doc_ref.update({"channelID": channelID})
    #         self.channelID = channelID
            
    #         return "Channel ID set successfully"
    #     except:
    #         raise

    def getGroqAPIKey(self):
        try: 
            if not self.groqAPIKey:
                collection_ref = db.collection(USER_COLLECTION_NAME)
                docs = collection_ref.where("userEmail", "==", self.userEmail).get()
                if not docs:
                    raise UserNotFoundError("No user found with this email.")

                record = docs[0].to_dict()

                if "groqAPIKey" not in record:
                    raise KeyNotFoundError("Groq API Key is not set in the database.")

                self.groqAPIKey = record["groqAPIKey"]

            return self.groqAPIKey 
        except:
            raise

    def setGroqAPIKey(self, groqAPIKey):
        try:
            collection_ref = db.collection(USER_COLLECTION_NAME)
            docs = collection_ref.where("userEmail", "==", self.userEmail).get()
            if not docs:
                raise UserNotFoundError("No user found with this email.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"groqAPIKey": groqAPIKey})
            self.groqAPIKey = groqAPIKey
            
            return "Groq API Key set successfully"
        except:
            raise

    def getSerperAPIKey(self):
        try: 
            if not self.serperAPIKey:
                collection_ref = db.collection(USER_COLLECTION_NAME)
                docs = collection_ref.where("userEmail", "==", self.userEmail).get()
                if not docs:
                    raise UserNotFoundError("No user found with this email.")

                record = docs[0].to_dict()

                if "serperAPIKey" not in record:
                    raise KeyNotFoundError("Serper API Key is not set in the database.")

                self.serperAPIKey = record["serperAPIKey"]

            return self.serperAPIKey 
        except:
            raise

    def setSerperAPIKey(self, serperAPIKey):
        try:
            collection_ref = db.collection(USER_COLLECTION_NAME)
            docs = collection_ref.where("userEmail", "==", self.userEmail).get()
            if not docs:
                raise UserNotFoundError("No user found with this email.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"serperAPIKey": serperAPIKey})
            self.serperAPIKey = serperAPIKey
            
            return "Serper API Key set successfully"
        except:
            raise

    def getTavilyAPIKey(self):
        try: 
            if not self.tavilyAPIKey:
                collection_ref = db.collection(USER_COLLECTION_NAME)
                docs = collection_ref.where("userEmail", "==", self.userEmail).get()
                if not docs:
                    raise UserNotFoundError("No user found with this email.")

                record = docs[0].to_dict()

                if "tavilyAPIKey" not in record:
                    raise KeyNotFoundError("Tavily API Key is not set in the database.")

                self.tavilyAPIKey = record["tavilyAPIKey"]

            return self.tavilyAPIKey 
        except:
            raise

    def setTavilyAPIKey(self, tavilyAPIKey):
        try:
            collection_ref = db.collection(USER_COLLECTION_NAME)
            docs = collection_ref.where("userEmail", "==", self.userEmail).get()
            if not docs:
                raise UserNotFoundError("No user found with this email.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"tavilyAPIKey": tavilyAPIKey})
            self.tavilyAPIKey = tavilyAPIKey
            
            return "Tavily API Key set successfully"
        except:
            raise

    def getOwnedProjects(self):
        try: 
            collection_ref = db.collection(USER_COLLECTION_NAME)
            docs = collection_ref.where("userEmail", "==", self.userEmail).get()
            if not docs:
                raise UserNotFoundError("No user found with this email.")

            record = docs[0].to_dict()

            if "ownedProjects" not in record or not record["ownedProjects"]:
                raise NoProjectsExistError("No projects found for the given user.")

            self.ownedProjects = record["ownedProjects"]
            print("ownedProjects user:", self.ownedProjects, type(self.ownedProjects))
            projectDetails = []
            for ownedProjectID in self.ownedProjects:
                project = Project(ownedProjectID)
                details=project.getProjectDetails(self.userEmail)
                projectDetails.append(details)
                # print("Project:", project)

            return projectDetails
        except:
            raise
    
    
    
    # Channel Details
    # def getChannelDetails(self):
    #     try:
    #         print("In getChannelDetails")
    #         user_email = self.userEmail  # Using the userEmail from the class instance (self)

    #         if not user_email:
    #             return jsonify({"success": "False", "message": "Entered email does not exist on the database"}), 404

    #         # Query Firestore to check if the user exists based on email
    #         user_ref = db.collection("TrialUser").document(user_email)  # Reference to the user document
    #         user_doc = user_ref.get()
    #         if user_doc.exists:
    #             user_data = user_doc.to_dict()
    #             print("User data:", user_data)
    #             channel_id = user_data.get("channelID")  # Fetch the channelID from the user data

    #             if channel_id:
    #                 # Directly fetch channel details
    #                 # result = db.collection("Channels").document(channel_id).get().to_dict()
    #                 print("****************************88")
                    
    #                 result = Channel.get(channel_id)
    #                 print("Channel: ", result)
    #                 return jsonify({
    #                     "success": "True",
    #                     "message": "User Channel Info Retrieved",
    #                     "channel_name": result['title'],
    #                     "channel_icon": result['thumbnails'][0]['url']
    #                 }), 200
                
    #             else:
    #                 return jsonify({
    #                     "success": "False",
    #                     "message": "Channel ID not associated with this user"
    #                 }), 404

    #         else:
    #             return jsonify({
    #                 "success": "False",
    #                 "message": "User not found"
    #             }), 404

    #     except Exception as e:
    #         print("In except: getChannelDetails", e)

    #         return jsonify({
    #             "success": "False",
    #             "message": f"An error occurred: {e}"
    #         }), 500



    # Delete User
    # def deleteUser(self):
    #     try:
    #         # Ensure userEmail is set
    #         if not self.userEmail:
    #             raise ValueError("User email is not set. Cannot delete user from the database.")

    #         print(f"Attempting to delete user with email {self.userEmail} from the database.")

    #         # Reference the document based on the userEmail
    #         user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)

    #         # Check if the document exists
    #         if not user_ref.get().exists:
    #             print(f"No user found with email {self.userEmail}. Nothing to delete.")
    #         else:
    #             # Delete the document
    #             user_ref.delete()
    #             print(f"User with email {self.userEmail} successfully deleted from the database.")

    #     except Exception as e:
    #         print(f"Error deleting user with email {self.userEmail}: {e}")
    #         raise

    # Update User
    # def updateUser(self, channelID=None, groqAPIKey=None, serperAPIKey=None, tavilyAPIKey=None):
    #     try:
    #         # Ensure userEmail is set
    #         if not self.userEmail:
    #             raise ValueError("User email is not set. Cannot update user in the database.")

    #         print(f"Updating user details for email {self.userEmail}")

    #         # Reference the user document
    #         user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)

    #         # Check if the user document exists
    #         if not user_ref.get().exists:
    #             raise ValueError(f"No user found with email {self.userEmail}. Cannot update non-existent user.")
    #             return jsonify({m})

    #         # Prepare the updated fields
    #         updated_fields = {}
    #         if channelID:
    #             self.setChannelID(channelID)
    #             updated_fields["channelID"] = channelID
    #         if groqAPIKey:
    #             self.setGroqAPIKey(groqAPIKey)
    #             updated_fields["groqAPIKey"] = groqAPIKey
    #         if serperAPIKey:
    #             self.setSerperAPIKey(serperAPIKey)
    #             updated_fields["serperAPIKey"] = serperAPIKey
    #         if tavilyAPIKey:
    #             self.setTavilyAPIKey(tavilyAPIKey)
    #             updated_fields["tavilyAPIKey"] = tavilyAPIKey

    #         # Update the fields in Firestore
    #         # if updated_fields:
    #         #     user_ref.update(updated_fields)
    #         #     print(f"User with email {self.userEmail} successfully updated in the database.")
    #         # else:
    #         #     print("No fields to update.")

    #     except Exception as e:
    #         print(f"Error updating user with email {self.userEmail}: {e}")
    #         raise

