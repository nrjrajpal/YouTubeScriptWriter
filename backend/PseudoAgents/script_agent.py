from .synthetic_agent import SyntheticAgent
from utils.firebase import db
import ast
from utils.exceptions import ProjectNotFoundError, KeyNotFoundError

PROJECT_COLLECTION_NAME = "TrialProject"

class ScriptAgent(SyntheticAgent):
    def __init__(self,  projectID, userEmail):
        super().__init__(projectID, userEmail)
        self.selectedQuestions = None

    def generateQuestionsBasedOnTitle(self):
        try:
            self.getVideoTitle()
            self.getIdeaDescription()
            
            print("Generating questions based on video title and idea description...")
            sys_prompt="You are a scriptwriting assistant, and your task is to generate 5 concise, engaging questions based on the provided video title and idea description. These questions should reflect potential viewers' expectations, concerns, and reasons to watch the video. Assume the role of a curious viewer who is considering watching the video and wants to know what value it offers."
            user_prompt=f"""
                Instructions:
                Imagine you're a viewer about to click on the video. Based on the title and description, think about what key questions or concerns you would have.
                Generate 5 distinct and concise questions that reflect a viewer's curiosity.
                The output must only contain short, distinct questions—no explanations or additional information. Each question should be clear and simple.
                Format the output exactly as a Python list of strings, with each question as a separate string.
                Video title: {self.videoTitle}
                Idea description: {self.ideaDescription}

                Output format:
                Return the questions as an array of strings that can be type casted using the python list function
                Output: Only generate 5 questions in the form of an array of strings in a single line and nothing else.

            """
            response = self.getLLMResponse(sys_prompt, user_prompt)
            questions = ast.literal_eval(response)
            
            return questions
        except:
            raise


    def getSelectedQuestions(self):
        try:
            if not self.selectedQuestions:
                collection_ref = db.collection(PROJECT_COLLECTION_NAME)
                docs = collection_ref.where("projectID", "==", self.projectID).get()
                if not docs:
                    raise ProjectNotFoundError("No project found with this ID.")
                
                record = docs[0].to_dict()

                if "selectedQuestions" not in record:
                    raise KeyNotFoundError("Selected questions are not set in the database.")

                self.selectedQuestions = record["selectedQuestions"]

            return self.selectedQuestions
        except:
            raise


    def setSelectedQuestions(self, selectedQuestions):
        try:
            collection_ref = db.collection(PROJECT_COLLECTION_NAME)
            docs = collection_ref.where("projectID", "==", self.projectID).get()
            if not docs:
                raise ProjectNotFoundError("No project found with this ID.")
            
            doc_ref = docs[0].reference
            doc_ref.update({"selectedQuestions": selectedQuestions})
            self.selectedQuestions = selectedQuestions
            
            return "Set selected questions successfully"
        except:
            raise
