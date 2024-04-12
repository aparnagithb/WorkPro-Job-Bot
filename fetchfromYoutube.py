import serpapi
import os
from dotenv import load_dotenv

def get_learning_resources(query):
    # Load API key from environment variables
    load_dotenv()
    api_key = os.getenv('api_key')

    # Initialize SerpApi client
    client = serpapi.Client(api_key=api_key)

    # Perform search query
    resultsvideolinks = client.search({
        "engine": "google_videos",
        "q": "youtube " + query,
        "hl": "en",
    })
    resultscourselinks = client.search({
        "engine": "google_videos",
        "q": "youtube "+query,
        "hl": "en",
    })

    # Extract top 3 video links
    top_video_links = []
    for video in resultsvideolinks['video_results']:
        title = video['title']
        link = video['link']
        top_video_links.append((title, link))
        if len(top_video_links) == 3:
            break

    # Extract top 3 course links
    top_course_links = []
    for ad in resultscourselinks.get('ads', []):
        if 'displayed_link' in ad:
            top_course_links.append(ad['displayed_link'])
        if len(top_course_links) == 3:
            break

    # Combine video and course links
    combined_links = top_video_links + top_course_links

    # Combine and format links as a string
    resultant_links = ""
    for i, link_info in enumerate(combined_links, start=1):
        if isinstance(link_info, tuple):
            title, link = link_info
            resultant_links += f"{i}. {title}: {link}\n"
        else:
            resultant_links += f"{i}. {link_info}\n"

    # Print or return the resultant links
    return resultant_links


