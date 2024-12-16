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


# Build vectorstore for a transcript
# def build_vectorstore(transcript_splits):
#     with SuppressStdout():
#         vectorstore = Chroma.from_documents(documents=transcript_splits, embedding=GPT4AllEmbeddings())
#     return vectorstore
from langchain.docstore.document import Document

# Build vectorstore for a transcript
def build_vectorstore(transcript_splits):
    # Wrap splits as Document objects
    documents = [Document(page_content=split) for split in transcript_splits]
    with SuppressStdout():
        vectorstore = Chroma.from_documents(documents=documents, embedding=GPT4AllEmbeddings())
    return vectorstore



# Query Groq for summarization
def query_groq(client, context, model="llama3-8b-8192"):
    # prompt = f"Summarize the following transcript:\n{context}\nSummary:"
    # print("\n\n\n\n\n\n Context:" +context+"\n\n\n\n\n\n")
    prompt = f"Why does he get angry after spending time with his kids? Only give me the reason and nothing else. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n{context}\n"
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model=model,
    )
    return chat_completion.choices[0].message.content


# RAG pipeline for a single transcript
def summarize_single_transcript(client, transcript):
    splits = preprocess_transcript(transcript)
    vectorstore = build_vectorstore(splits)

    # Summarize each chunk
    summary = ""
    for chunk in splits:
        summary += query_groq(client, chunk) + "\n"
    print(summary.strip()+"\n\n\n\n\n\n")
    return summary.strip()


# Process the API response structure
def summarize_videos_from_file(client, api_response_file):
    # Load the API response file
    with open(api_response_file, 'r') as file:
        api_response = json.load(file)

    final_summaries = []

    # Process each video transcript
    for video_data in api_response:
        metadata = video_data["Metadata"]
        transcript = video_data["Transcript"]

        # Summarize the transcript
        print(f"Summarizing video: {metadata['title']} (ID: {metadata['id']})")
        summary = summarize_single_transcript(client, transcript)
        final_summaries.append(summary)

    # Combine all individual summaries into a master summary
    master_summary = query_groq(client, " ".join(final_summaries))
    return final_summaries, master_summary


if __name__ == "__main__":
    # Specify the path to your API response file
    api_response_file = "/mnt/d/YT-Project/backend/APIs/api_response.json"  # Replace with your file path

    # Run summarization pipeline
    print("Starting summarization...")
    summaries, master_summary = summarize_videos_from_file(client, api_response_file)

    # Save summaries to file
    with open("video_summaries.txt", "w") as f:
        for i, summary in enumerate(summaries, start=1):
            f.write(f"Summary for Video {i}:\n{summary}\n\n")
        f.write(f"Master Summary:\n{master_summary}\n")

    print("Summarization complete. Results saved to video_summaries.txt")
