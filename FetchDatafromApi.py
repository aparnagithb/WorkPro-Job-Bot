import serpapi
import os
from dotenv import load_dotenv

def get_trends_data(query):
    # Load API key from environment variables
    load_dotenv()
    api_key = os.getenv('api_key')

    # Initialize SerpApi client
    client = serpapi.Client(api_key=api_key)

    # Perform search query
    results = client.search({
        "engine": "bing",
        "q": query,
        "hl": "en",
    })

    # Extract answer box snippet and link
    answer_box = results.get("answer_box", {})
    answer_box_snippet = answer_box.get("snippet", "")
    answer_box_link = answer_box.get("link", "")

    # Extract snippets and links from organic results
    organic_results = results.get("organic_results", [])
    organic_data = [(result.get("snippet", ""), result.get("link", "")) for result in organic_results]

    # Combine snippets and links from both sections
    all_data = [(answer_box_snippet, answer_box_link)] + organic_data

    # Format output
    formatted_output = ""
    for snippet, link in all_data:
        formatted_output += f"Snippet: {snippet}\nLink: {link}\n\n"
    print(formatted_output)
    return formatted_output
get_trends_data("Learning resources for python")
'''import serpapi
import os

from dotenv import load_dotenv
load_dotenv()

api_key= os.getenv('api_key')
client=serpapi.Client(api_key=api_key)
results= client.search({
  "engine": "google_jobs",
  "q": "python developer delhi ",
  "hl": "en",

})

results= client.search({
  "engine": "bing",
  "q": "Trends in Zoho",
  "hl": "en",
})


#print(results)


search = GoogleSearch(params)
results = search.get_dict()
jobs_results = results["jobs_results"]

# Print job results

answer_box = results.get("answer_box", {})
answer_box_snippet = answer_box.get("snippet", "")
answer_box_link = answer_box.get("link", "")

# Extract snippets and links from organic results
organic_results = results.get("organic_results", [])
organic_data = [(result.get("snippet", ""), result.get("link", "")) for result in organic_results]

# Combine snippets and links from both sections
all_data = [(answer_box_snippet, answer_box_link)] + organic_data

# Generate formatted output with snippets and links
formatted_output = ""
for snippet, link in all_data:
    formatted_output += f"Snippet: {snippet}\nLink: {link}\n\n"

# Print the formatted output
print("Combined Snippets with Links:")
print(formatted_output) '''