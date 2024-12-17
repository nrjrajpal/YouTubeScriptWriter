from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from config import Config  # Assuming config handles DB interactions
import os
from youtubesearchpython import Channel
from dotenv import load_dotenv
from utils.exceptions import KeyNotFoundError
load_dotenv()

cred = credentials.Certificate("scriptwriter-firebase-adminsdk.json")
# firebase_admin.initialize_app(cred)

db = firestore.client()

COLLECTION_NAME = "TrialUser"

class User:
    def __init__(self,userEmail):
        self.userEmail = userEmail
        self.channelID = None
        self.groqAPIKey = None
        self.serperAPIKey = None
        self.tavilyAPIKey = None
        self.ownedProjects = []

    # Channel ID Functions
    def getChannelID(self):
        try: 
            print(f"Fetching channel ID for user {self.userEmail}")

            # Access the document directly
            user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)
            user_doc = user_ref.get()

            if not user_doc.exists:
                raise UserNotFoundError(f"No document found for user {self.userEmail}")

            user_data = user_doc.to_dict()
            if "channelID" not in user_data:
                raise KeyNotFoundError("ChannelID field is not set in the database.")

            self.channelID = user_data["channelID"]


            return self.channelID 
        except:
            raise
            

    def setChannelID(self, newChannelID):
        self.channelID = newChannelID  # Update the local attribute

        if not self.userEmail:
            print("Error: Cannot set ChannelID without a valid userEmail.")
            raise UserNotFoundError("No valid user found")
            return

        try:
            users_ref = db.collection(COLLECTION_NAME).document(self.userEmail)  # Reference the user document
            users_ref.update({"channelID": newChannelID})  # Update the ChannelID field in Firestore
            print(f"Successfully updated ChannelID to {newChannelID} for user {self.userEmail}.")
        except:
            # print(f"Failed to update ChannelID for user {self.userEmail}. Error: {e}")
            raise

    def getGroqAPIKey(self):
        if not self.groqAPIKey:
            print("Fetching Groq API Key")
            user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)  # Reference the user document
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()  # Convert document to dictionary
                self.groqAPIKey = user_data.get("GROQAPIKEY")  # Fetch Groq API Key field
                if not self.groqAPIKey:
                    raise GroqAPIKeyNotFoundError("Groq API Key is not set in the database.")
            else:
                raise UserNotFoundError(f"No user found with email {self.userEmail}")

        return self.groqAPIKey

    def setGroqAPIKey(self, newGroqAPIKey):
        if not self.userEmail:
            print("Error: Cannot set Groq API Key without a valid email.")
            return

        try:
            self.groqAPIKey = newGroqAPIKey
            user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)  # Reference the user document
            user_ref.update({"GROQAPIKEY": newGroqAPIKey})  # Update the Groq API Key in Firestore
            print(f"Successfully updated Groq API Key to {newGroqAPIKey} for user {self.userEmail}.")
        except Exception as e:
            print(f"Failed to update Groq API Key for user {self.userEmail}. Error: {e}")

# Serper API Key Functions
    def getSerperAPIKey(self):
        if not self.serperAPIKey:
            print("Fetching Serper API Key")
            user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                self.serperAPIKey = user_data.get("SERPERAPIKEY")  # Fetch Serper API Key field
                if not self.serperAPIKey:
                    raise KeyError("Serper API Key is not set in the database.")
            else:
                raise ValueError(f"No user found with email {self.userEmail}")

        return self.serperAPIKey

    def setSerperAPIKey(self, newSerperAPIKey):
        if not self.userEmail:
            print("Error: Cannot set Serper API Key without a valid email.")
            return

        try:
            self.serperAPIKey = newSerperAPIKey
            user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)
            user_ref.update({"SERPERAPIKEY": newSerperAPIKey})  # Update Serper API Key in Firestore
            print(f"Successfully updated Serper API Key to {newSerperAPIKey} for user {self.userEmail}.")
        except Exception as e:
            print(f"Failed to update Serper API Key for user {self.userEmail}. Error: {e}")

    # Tavily API Key Functions
    def getTavilyAPIKey(self):
        if not self.tavilyAPIKey:
            print("Fetching Tavily API Key")
            user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)
            user_doc = user_ref.get()

            if user_doc.exists:
                user_data = user_doc.to_dict()
                self.tavilyAPIKey = user_data.get("TAVILYAPIKEY")  # Fetch Tavily API Key field
                if not self.tavilyAPIKey:
                    raise KeyError("Tavily API Key is not set in the database.")
            else:
                raise ValueError(f"No user found with email {self.userEmail}")

        return self.tavilyAPIKey

    def setTavilyAPIKey(self, newTavilyAPIKey):
        if not self.userEmail:
            print("Error: Cannot set Tavily API Key without a valid email.")
            return

        try:
            self.tavilyAPIKey = newTavilyAPIKey
            user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)
            user_ref.update({"TAVILYAPIKEY": newTavilyAPIKey})  # Update Tavily API Key in Firestore
            print(f"Successfully updated Tavily API Key to {newTavilyAPIKey} for user {self.userEmail}.")
        except Exception as e:
            print(f"Failed to update Tavily API Key for user {self.userEmail}. Error: {e}")


    def getTavilyAPIKeyStatus(self):
        if not self.tavilyAPIKey:
            self.tavilyAPIKey = self.getTavilyAPIKey()
        return self.isTavilyAPIKeySet

    # Owned Projects Functions
    def getOwnedProjects(self):
        try:
            # Check if userEmail exists
            if not self.userEmail:
                raise ValueError("User email is not set. Cannot fetch owned projects.")

            print(f"Fetching owned projects for user {self.userEmail} from the database.")

            # Query TrialProject collection for documents where projectOwnerEmail matches self.userEmail
            projects = db.collection('TrialProject').where('projectOwnerEmail', '==', self.userEmail).get()

            if not projects:
                print(f"No projects found for user {self.userEmail}")
                self.ownedProjects = []  # No projects found; set to empty list
            else:
                # Extract project IDs from the documents
                self.ownedProjects = [project.id for project in projects]
                print(f"Projects owned by {self.userEmail}: {self.ownedProjects}")

            return self.ownedProjects

        except Exception as e:
            print(f"Error fetching owned projects for user {self.userEmail}: {e}")
            raise

    # Channel Details
    def getChannelDetails(self):
        try:
            print("In getChannelDetails")
            user_email = self.userEmail  # Using the userEmail from the class instance (self)

            if not user_email:
                return jsonify({"success": "False", "message": "Entered email does not exist on the database"}), 404

            # Query Firestore to check if the user exists based on email
            user_ref = db.collection("TrialUser").document(user_email)  # Reference to the user document
            user_doc = user_ref.get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                print("User data:", user_data)
                channel_id = user_data.get("channelID")  # Fetch the channelID from the user data

                if channel_id:
                    # Directly fetch channel details
                    # result = db.collection("Channels").document(channel_id).get().to_dict()
                    print("****************************88")
                    
                    result = Channel.get(channel_id)
                    print("Channel: ", result)
                    return jsonify({
                        "success": "True",
                        "message": "User Channel Info Retrieved",
                        "channel_name": result['title'],
                        "channel_icon": result['thumbnails'][0]['url']
                    }), 200
                
                else:
                    return jsonify({
                        "success": "False",
                        "message": "Channel ID not associated with this user"
                    }), 404

            else:
                return jsonify({
                    "success": "False",
                    "message": "User not found"
                }), 404

        except Exception as e:
            print("In except: getChannelDetails", e)

            return jsonify({
                "success": "False",
                "message": f"An error occurred: {e}"
            }), 500



    # Delete User
    def deleteUser(self):
        try:
            # Ensure userEmail is set
            if not self.userEmail:
                raise ValueError("User email is not set. Cannot delete user from the database.")

            print(f"Attempting to delete user with email {self.userEmail} from the database.")

            # Reference the document based on the userEmail
            user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)

            # Check if the document exists
            if not user_ref.get().exists:
                print(f"No user found with email {self.userEmail}. Nothing to delete.")
            else:
                # Delete the document
                user_ref.delete()
                print(f"User with email {self.userEmail} successfully deleted from the database.")

        except Exception as e:
            print(f"Error deleting user with email {self.userEmail}: {e}")
            raise

    # Update User
    def updateUser(self, channelID=None, groqAPIKey=None, serperAPIKey=None, tavilyAPIKey=None):
        try:
            # Ensure userEmail is set
            if not self.userEmail:
                raise ValueError("User email is not set. Cannot update user in the database.")

            print(f"Updating user details for email {self.userEmail}")

            # Reference the user document
            user_ref = db.collection(COLLECTION_NAME).document(self.userEmail)

            # Check if the user document exists
            if not user_ref.get().exists:
                raise ValueError(f"No user found with email {self.userEmail}. Cannot update non-existent user.")
                return jsonify({m})

            # Prepare the updated fields
            updated_fields = {}
            if channelID:
                self.setChannelID(channelID)
                updated_fields["channelID"] = channelID
            if groqAPIKey:
                self.setGroqAPIKey(groqAPIKey)
                updated_fields["groqAPIKey"] = groqAPIKey
            if serperAPIKey:
                self.setSerperAPIKey(serperAPIKey)
                updated_fields["serperAPIKey"] = serperAPIKey
            if tavilyAPIKey:
                self.setTavilyAPIKey(tavilyAPIKey)
                updated_fields["tavilyAPIKey"] = tavilyAPIKey

            # Update the fields in Firestore
            # if updated_fields:
            #     user_ref.update(updated_fields)
            #     print(f"User with email {self.userEmail} successfully updated in the database.")
            # else:
            #     print("No fields to update.")

        except Exception as e:
            print(f"Error updating user with email {self.userEmail}: {e}")
            raise

