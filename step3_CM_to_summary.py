import openai
import pandas as pd
import json

# Load JSON data (historic trends)
import re

def extract_summary(text):
    match = re.search(r"Summary:\n(.*)", text, re.DOTALL)
    return match.group(1).strip() if match else None

def generate_summary_from_causal_link(summary, filtered_df):
    """Compare trends and generate a business summary using LLM."""
    

    prompt = f"""You are Data summarizer.

<Your Inputs>
1. Data JSON
 - This is financial data.
 - All keys are self explanatory
 - All keys that contain the suffix "YoY" contain % change from last year.
 - All keys that contain the suffix "LY" show the last year numbers.

2. Knowledge Base
 - This contains nodes and edges
 - Nodes : All the KPIs that should be explained as part of the summary.
   -- Schema : "id" -> Name of the KPI/Event
	       "value" -> %change year over year.
 - Edges : All the KPIs that impact the other KPIs. The summary should contain a causal reason for these.
   -- Schema : "start" -> KPI that makes the impact
	       "end" -> KPI that receives the impact
               "value" -> %change year over year for start node.

 - All nodes of this should be a part of the summary.
 - All edges here should be mentioned as a cause effect in the summary.
3. Sample Summary
 - This is a sample summary.
 - Use the tonality and language construction used in this summary.
 - This is the standard format used in the company.

</Your Inputs>

Now Look at the inputs below


<Data JSON>
      {filtered_df[0]}

</Data JSON>


<Knowledge Base>

{summary}

</Knowledge Base>


<Sample Summary>
Demand at 59.3M (+4.3% vs LY) with the launch of SleekTech Activewear and promotional pricing on activewear (LY 50% Off Sleepwear). Traffic was down -4% vs LY. Conversion rate (2% vs LY) for second consecutive week. AOS was up ($77 vs LY $22) was driven by more UPT.
</Sample Summary>


How to Draw Causal Relations:
- For every edge in the <Knowledge Base> think about whether the Start KPI would be positively or negatively correlated with the End KPI based on intuition. (Expected Correlation)
- Also check what is the actual correlation seen in the <Data JSON>. (Actual Correlation)
- If the expected and observed correlation align, make a statement like "driven by"
- Else make a statement like "despite"



How to produce the output as follows:
1. Node KPI 1:
   Driven By:
   a. Driving KPI 1 (Name)
      - Definition of Driving KPI 1.
      - Expected Correlation with Node KPI (Description and reason)
      - Observed Correlation with Node KPI
      - Does the Expected and Observed KPI match? (Yes/No)
      - Clause to be used in the summary

First produce this list based on the "end" nodes in the edges, and then do it for the remaining nodes.

Then produce the final summary under ```Summary```.


Make sure to use just the Acronyms as shown in the Data JSON.
Make sure to describe only the nodes in the <Knowledge Base>.
Make sure to use only the causal reasons that appear in edges of the <Knowledge Base>.
Make use of words and phrases similar to <Sample Summary>.
Avoid comments about the how significant or insignificant the %change is.
When the observed and expected correlation match use phrase like "driven by", "leading to"
When the observed and expected correlation don't match use phase like "despite", "even though".
Always mention the time frame of change like "vs LY" as seen in <Sample Summary>
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
    with open("derived/final_summary.txt", "w", encoding="utf-8") as file:
        file.write(summary)

    summary = extract_summary(summary)
    with open("derived/edit_summary.txt", "w", encoding="utf-8") as file:
        file.write(summary)

    print("JSON file saved successfully.")
    


with open("derived/fil_data_causal_map.json", "r") as file:
    map = json.load(file)

with open("derived/filtered_df.json", "r") as file:
    filtered_df = json.load(file)

generate_summary_from_causal_link(map, filtered_df)
