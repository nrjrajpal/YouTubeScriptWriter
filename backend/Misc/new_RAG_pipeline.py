import json
import os
import sys
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from groq import Groq
load_dotenv() 

# Suppress stdout for specific operations
class SuppressStdout:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr


# Initialize Groq Client (Ensure API Key is set in environment variables)
api_key = os.getenv("GROQAPIKEY")
if not api_key:
    raise ValueError("Missing Groq API key. Set GROQ_API_KEY as an environment variable.")
client = Groq(api_key=api_key)


# Function to preprocess the transcript
def preprocess_transcript(transcript, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(transcript)


from langchain.docstore.document import Document

# Build vectorstore for a transcript
def build_vectorstore(transcript_splits):
    # Wrap splits as Document objects
    documents = [Document(page_content=split) for split in transcript_splits]
    with SuppressStdout():
        vectorstore = Chroma.from_documents(documents=documents, embedding=GPT4AllEmbeddings())
    return vectorstore


# Query Groq for QA extraction
def query_groq_qa(client, context, question, model="llama3-8b-8192"):
    prompt = f"Answer the following question based on the context provided. Do not hallucinate. Do not makeup any information or facts. If the answer is not in the context, respond only with 'NULL' and nothing else.\nQuestion: {question}\nContext: {context}\nAnswer:"
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model=model,
    )
    return chat_completion.choices[0].message.content.strip()


# QA-based RAG pipeline for a single transcript
def extract_answers_from_transcript(client, transcript, questions):
    splits = preprocess_transcript(transcript)
    vectorstore = build_vectorstore(splits)

    answers = {}

    for question in questions:
        # Extract answers for each question across all chunks
        combined_answer = ""
        for chunk in splits:
            answer = query_groq_qa(client, chunk, question)
            if answer.lower() != "i don't know":
                combined_answer += answer + " "
            print("\n\n\nQuestion: "+ question + "\n\n\nAnswer: " + answer)
        answers[question] = combined_answer.strip()

    return answers


# Process the API response structure
def process_transcripts_with_questions(client, api_response_file, questions):
    # Load the API response file
    with open(api_response_file, 'r') as file:
        api_response = json.load(file)

    all_answers = []

    # Process each video transcript
    for video_data in api_response:
        metadata = video_data["Metadata"]
        transcript = video_data["Transcript"]

        print(f"Processing video: {metadata['title']} (ID: {metadata['id']})")

        # Extract answers for the transcript
        answers = extract_answers_from_transcript(client, transcript, questions)
        all_answers.append({"video_id": metadata['id'], "title": metadata['title'], "answers": answers})

    return all_answers


if __name__ == "__main__":
    # Specify the path to your API response file
    api_response_file = "/mnt/d/YT-Project/backend/APIs/api_response.json"  # Replace with your file path

    # List of questions based on the outline
    questions = [
    "What are the most effective time management strategies for increasing productivity?",
    "How do psychological principles influence time management and productivity?",
    "What are the key factors that contribute to procrastination and how can they be overcome?",
    "How can breaking down tasks and prioritizing them enhance daily productivity?",
    "What are some practical techniques to apply time management strategies in both personal and professional life?",
    "Who is Barack Obama's dad?"
    ]

    # Run the QA-based pipeline
    print("Starting QA-based extraction...")
    extracted_answers = process_transcripts_with_questions(client, api_response_file, questions)

    # Save the answers to a JSON file
    with open("video_answers.json", "w") as f:
        json.dump(extracted_answers, f, indent=4)

    # Combine all answers for a polished final script
    final_script = ""
    for video in extracted_answers:
        final_script += f"\nVideo Title: {video['title']}\n"
        for question, answer in video['answers'].items():
            final_script += f"\n{question}\n{answer}\n"

    # Save the final script to a file
    with open("final_script.txt", "w") as f:
        f.write(final_script)

    print("QA-based extraction complete. Results saved to video_answers.json and final_script.txt")
