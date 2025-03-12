import openai
import pandas as pd
import json
import os

# Load JSON data (historic trends)
import re
def extract_summary(text):
    # Define regex patterns for different summary formats
    patterns = [
        r"Summary:\s*(.*?)$",  # Case with "Summary:" in plain text
        r"<Summary>(.*?)</Summary>",  # XML-like case
        r"```Summary```\s*(.*?)$",  # Markdown-style case
        r"<Output>\s*<Summary>(.*?)</Output>",  # Output wrapped summary
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return None

# def extract_summary(text):
#     match = re.search(r"Summary:\n(.*)", text, re.DOTALL)
#     return match.group(1).strip() if match else None

def generate_summary_from_causal_link(summary, filtered_df, brand):
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
      {filtered_df}

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
    with open(f"summary/{brand}_final_summary.txt", "w", encoding="utf-8") as file:
        if summary is not None:
            file.write(summary)
        else:
            file.write("")

    summary = extract_summary(summary)
    with open(f"edited_summary/{brand}_edit_summary.txt", "w", encoding="utf-8") as file:
        if summary is not None:
            file.write(summary)
        else:
            file.write("")

    print("JSON file saved successfully.")
    


# with open("derived/fil_data_causal_map.json", "r") as file:
#     map = json.load(file)

# with open("derived/filtered_df.json", "r") as file:
#     filtered_df = json.load(file)

# generate_summary_from_causal_link(map, filtered_df)

def process_causal_maps(cm_folder, derived_folder):
    cm_files = {f.split('_causal_map.json')[0]: os.path.join(cm_folder, f) for f in os.listdir(cm_folder) if f.endswith('_causal_map.json')}
    derived_files = {f.split('_filtered_data.json')[0]: os.path.join(derived_folder, f) for f in os.listdir(derived_folder) if f.endswith('_filtered_data.json')}
    
    common_brands = cm_files.keys() & derived_files.keys()

    for brand in common_brands:
        cm_file_path = cm_files[brand]
        derived_file_path = derived_files[brand]



        with open(cm_file_path, 'r') as cm_file:
            causal_map = cm_file.read()
        
        with open(derived_file_path, 'r') as derived_file:
            filtered_df = json.load(derived_file)
        
        generate_summary_from_causal_link(causal_map, filtered_df, brand)

# Example usage
cm_folder = "CM_filtered"
derived_folder = "derived"


os.makedirs("summary", exist_ok=True)
os.makedirs("edited_summary", exist_ok=True)

process_causal_maps(cm_folder, derived_folder)
