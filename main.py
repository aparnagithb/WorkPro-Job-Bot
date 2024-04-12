from fastapi import FastAPI
from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from db_helper import store_details,fetch_user_data_from_database
from FetchDatafromApi import get_trends_data
from fetchfromYoutube import get_learning_resources
import requests
import serpapi
import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import BackgroundTasks
app = FastAPI()

api_key= os.getenv('api_key')
client=serpapi.Client(api_key=api_key)

@app.post("/")
async def handle_request(request:Request,background_tasks: BackgroundTasks):
    payload = await request.json()  # webhook request coming from dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    fulfillment_text = ""
    if intent == "Find Job":

        '''return JSONResponse(content={
           "fulfillmentText":f"Received =={intent}== in the backend"
        })'''
        textos = find_job(parameters, intent)
        job_summaries = []
        for job in textos:
            job_summary = f"\nJob Title: {job['title']}\nCompany: {job['company_name']}\nLocation: {job['location']}\n\n"  # Double newline for spacing
            job_summaries.append(job_summary)
        concatenated_text = "".join(job_summaries)

        # Construct the fulfillment text with all job summaries (use triple quotes for multi-line text)
        fulfillment_text = f"""Here are the jobs I found matching your criteria:

        {concatenated_text}

        Would you like me to narrow down the search?"""



    elif intent == "Add new user Intent":
        query_text = payload['queryResult']['queryText']
        fulfillment_text = store_details(query_text)
    elif intent == "Find-Trends":
        query_text = payload['queryResult']['queryText']  # Extract the query text
        trends_data =  get_trends_data(query_text)
        fulfillment_text = f"Here are the trends for '{query_text}':\n\n{trends_data}"
    elif intent == "Learning-Resources":  # Handle the "Learning-Resources" intent
          # Call the get_learning_trends function
        query_text = payload['queryResult']['queryText']
        fulfillment_text = get_learning_resources(query_text )

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
        # "fulfillmentText": "Fetching job details in the background. Please wait. How many job titles should I display?"
    })


def find_job(parameters,intent):
    job_role="".join(parameters['Job-Role'])
    country="".join(parameters['geo-country'])
    user_id = parameters.get('id', [None])[0]
    user_data = fetch_user_data_from_database(user_id)
    # Extract user skills and educational qualifications from user data
    user_skills = user_data.get('Skills', [])
    user_education = user_data.get('Educational_Qualifications', [])
    # Convert skills and education to lowercase for case-insensitive matching
    user_skills = [skill.lower() for skill in user_skills.split(',')]
    user_education = [edu.lower() for edu in user_education.split(',')]
    query=f"{job_role} in {country}"
    results = client.search({
        "engine": "google_jobs",
        "q": query,
        "hl": "en",

    })
    jobs = []
    for job in results["jobs_results"]:
        job_skills = job["description"].lower().split()  # Extract skills mentioned in the job description

        # Extract educational qualifications mentioned in the job description
        job_education = job["description"].lower()

        # Check if any of the user's skills match with the job skills
        skill_matched = any(skill in job_skills for skill in user_skills)

        # Check if any of the user's educational qualifications are mentioned in the job description
        edu_matched = any(edu in job_education for edu in user_education)

        # Consider the job if either skill or education is matched
        if skill_matched or edu_matched:
            job_dict = {}
            job_dict["title"] = job["title"]
            job_dict["company_name"] = job["company_name"]
            job_dict["location"] = job["location"].strip()  # Remove extra spaces
            job_dict["description"] = job["description"].strip()  # Remove extra spaces
            job_dict["extensions"] = job["extensions"]
            jobs.append(job_dict)
    
    jobs_to_display = jobs[:5]
    return jobs_to_display











