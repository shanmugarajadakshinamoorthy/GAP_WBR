import openai
import pandas as pd
import json

# Load JSON data (historic trends)


def generate_summary_from_causal_link(summary):
    """Compare trends and generate a business summary using LLM."""
    

    prompt = f"""You are an AI assistant that converts structured causal map data into concise, insightful business summaries. Given a JSON input containing "nodes" and "edges," your task is to generate a well-structured summary in a professional and readable format.

Guidelines:

Identify key business events from the "nodes" list, focusing on quantitative changes.
Use "edges" to establish cause-and-effect relationships between events.
Maintain logical flow, grouping negative and positive impacts separately.
Use clear, natural language with numerical data to support insights.
Avoid redundancy while ensuring all critical connections are represented.
Example JSON Input:
{summary}

Example Output:
The business saw a noteworthy increase in actualized discount by 16.6% over the year, negatively impacting the yearly sales quantity, which shrunk by 6.3%. The effect on sales quantity was further compounded by low traffic count, with data unavailable for specific yearly percentage change. Closing inventory quantity has notably declined by 34.5% over the year, further contributing to the drop in sales quantity by 6.3%. However, improvement was observable in the units per transaction, recording a 13.8% growth year-on-year. This enhanced the average transaction value that grew significantly by 28.3% in the same span.

important:
make sure the output is very similar to the example output.
Make sure you dont take any value from example. just retain the structure
    """

    
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a summary creator from causal link creator summarizing business performance."},
            {"role": "user", "content": prompt}
        ]
    )
    
    summary = response.choices[0].message.content
    with open("final_summary.txt", "w", encoding="utf-8") as file:
        file.write(summary)

    print("JSON file saved successfully.")
    


with open("causal_map.json", "r") as file:
    map = json.load(file)


generate_summary_from_causal_link(map)
