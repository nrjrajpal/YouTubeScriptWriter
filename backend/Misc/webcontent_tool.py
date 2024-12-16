import os
from groq import Groq
from tavily import TavilyClient
import asyncio
import json
import requests
from colorama import Fore

# Set up the API keys and clients
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key="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")

# Global variables
website_formatted_content = []

def get_data(query: str):
    try:
        response = tavily_client.search(query=query, search_depth="advanced", max_results=5, include_raw_content=True)
        count = 0
        for i in range(0, len(response['results'])):
            if (count < 3) and (not response['results'][i]['raw_content'] == None):
                print("\n\n\n\n\n\n\n")
                print("\nProcessed: ", response['results'][i]['url'])
                raw_content = response['results'][i]['raw_content']
                print("Original Length Raw Content: \n", len(raw_content))
                if len(raw_content) > 50000:
                    raw_content = raw_content[:50000]
                print("New Length Raw Content: \n", len(raw_content))
                website_formatted_content.append({
                    'webpage_url': response['results'][i]['url'],
                    'webpage_title': response['results'][i]['title'],
                    'webpage_raw_content': raw_content.replace("\n"," "),
                })
                count += 1
            
            else:
                print(Fore.RED + "Skipped: ", response['results'][i]['url'])

    except Exception as e:
        print("Error Occured: ", str(e))

    print(Fore.LIGHTMAGENTA_EX + "\n\n\n\n\nFormatted Content: \n", website_formatted_content)

# Define the main function to test get_data
async def main():
    query = "Artificial Intelligence in Healthcare"
    print(f"Running search with query: {query}")
    get_data(query)
    print("Finished fetching data.")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

