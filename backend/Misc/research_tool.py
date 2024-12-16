import os
import requests
import json
import time
from groq import Groq
from tavily import TavilyClient
from colorama import Fore, Style, init
import asyncio
from dotenv import load_dotenv
load_dotenv()

# Initialize colorama
init()

# Set up environment variables and API clients
client = Groq(api_key=os.getenv("GROQAPIKEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILYAPIKEY"))

# Global variables to store paper URLs and formatted content
paper_urls = []
research_formatted_content = []
final_research_formatted_content = []

def get_links(query: str):
    url = "https://google.serper.dev/scholar"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.getenv("SERPAPIKEY"),
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.text
    data_dict = json.loads(data)

    try:
        for i in range(0, 10):
            research_formatted_content.append({
                "paper_title": data_dict["organic"][i]["title"],
                "paper_url": data_dict["organic"][i]["link"],
                "paper_publication_info": data_dict["organic"][i]["publicationInfo"],
                "year": data_dict["organic"][i]["year"],
                "paper_raw_content": ""
            })
            paper_urls.append(data_dict["organic"][i]["link"])
            print("Added Paper: ", data_dict["organic"][i]["link"])
    except Exception as e:
        print("Error: ", str(e))

    print(Fore.BLUE + "\n\n\n\nPapers to use:\n", research_formatted_content)
    print(Style.RESET_ALL)

def get_data(research_formatted_content: list):
    try:
        response = tavily_client.extract(urls=paper_urls)
        i = 0
        for output in response["results"]:
            if i == 3: break
            raw = output["raw_content"]
            if len(raw) > 50000:
                raw = raw[:50000]
            
            for formatted_output in research_formatted_content:
                if output["url"] == formatted_output["paper_url"]:
                    formatted_output["paper_raw_content"] = raw
                    print(f"Processed raw data for: {output['url']}")
                    i += 1
                    break
        
        for formatted_output in research_formatted_content:
            if "paper_raw_content" in formatted_output and formatted_output["paper_raw_content"]:
                final_research_formatted_content.append(formatted_output)

    except Exception as e:
        print("Error: ", str(e))

    print(Fore.YELLOW + "\n\n\n\nFinal raw research content size: ", len(final_research_formatted_content))
    print(Style.RESET_ALL)
    print("\n\n\n\nRaw research content formed:\n", final_research_formatted_content)

# Define the main function to test get_links and get_data
async def main():
    query = "Artificial Intelligence in Healthcare"
    print(f"Running search with query: {query}")

    # Fetch paper links
    get_links(query)
    print(f"Finished fetching links for query: {query}")

    # Process the raw content for each paper
    get_data(research_formatted_content)
    print("Finished processing raw data.")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

