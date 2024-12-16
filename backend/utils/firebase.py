import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase App
if not firebase_admin._apps:  # Check if the app is already initialized
    cred = credentials.Certificate("scriptwriter-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()
