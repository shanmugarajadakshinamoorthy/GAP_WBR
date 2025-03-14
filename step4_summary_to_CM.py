import openai
import pandas as pd
import json
import re
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
load_dotenv(override=True)
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Load JSON data (historic trends)


def generate_causal_link(summary, brand_name):
    """Compare trends and generate a business summary using LLM."""
    

    prompt = f"""You are a causal link creator.
    I will give you a summary that has been generated by a user. I need to turn this into a Causal Chain.

    Do the following:
    1. Create a list of nodes.
    -- Schema
        id = String(description:"ID of node", example : "product launch")
        value = String(description:"Actual text present in the summary", example = "Demand at 13 (+4.3% vs LY)", constraint = "must be a substring of the summary")
        correct = Literal(description:"has this been expicitlely specified in the summary",  possibles_values = ['True', 'False'])

    2. Create a list of edges.
    -- Schema
        start = String(description:"start node of the edge", example : "product launch")
        end = String(description:"end node of the edge", example : "product launch")
        impact = Literal(description:"the impact the start node has on the end node", possible_values= ["positive","negative","neutral"], example = "positive")
        value = String(description:"Actual text present in the summary", example = "AOS was up ($77 vs LY $22) was driven by more UPT", constraint = "must be a substring of the summary")

        correct = Literal(description:"has this been expicitlely specified in the summary",  possibles_values = ['True', 'False'])


    Possible Ids for Events:
    Promotion
    Product Launch

    Possible Ids for KPIs
    demand
    discount
    traffic
    Order
    UPT
    ATV
    AOS
    AUR
    Conversion Rate

    Hint:
    Mostly Events will be impacting KPIs

    <Summary>
    {summary}
    </Summary>


    Now give me the Causal Chain as a json

    Just produce the JSON and nothing else.
    """

    
    client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
    response = client.chat.completions.create(
        model="pfz-gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a causal link creator summarizing business performance."},
            {"role": "user", "content": prompt}
        ]
    )
    
    json_output = response.choices[0].message.content
    cleaned_text = re.sub(r"^```json|\n```$", "", json_output.strip(), flags=re.MULTILINE)

    with open(f"recreated_CM/{brand_name}_recreated_CM.json", "w") as file:
        
        file.write(cleaned_text)

    print("JSON file saved successfully.")
    


# with open("derived/edit_summary.txt", "r", encoding="utf-8") as file:
#     content = file.read()


# generate_causal_link(content)

