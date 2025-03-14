import openai
import pandas as pd
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
load_dotenv(override=True)
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

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
    """Compare trends and generate a business summary using LLM."""
    kb = summary
    prompt = f"""You are Data Describer.

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

3. Sample Description
 - This is a sample Description.
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


<Sample Description>
Demand at 59.3M (+4.3% vs LY) with the launch of SleekTech Activewear and promotional pricing on activewear (LY 50% Off Sleepwear). Traffic was down (-4% vs LY). Conversion rate (2% vs LY) for second consecutive week. AOS was up ($77 vs LY $22) was driven by more UPT.
</Sample Description>

<Instructions>
1. Make a list of all the nodes mentioned in "edges" in the knowledge base <Knowledge Base>
2. On the "edges" mentioned in <Knowledge Base> perform group by "end node" and collect the names of all the "Start Node". Produce collection of **start nodes** for each **end node**
3. For each group in 2 for each "Start Nodes" do the following:
   a. Definition of #Start Node Name#.
   b. Expected impact of #Start Node Name# on Current Node (Description and reason)
   c. Observed impact of #Start Node Name# on Current Node as seen in the <Data JSON> (Description)
   d. Do the Expected and Observed impact the same? (Yes/No)
   e. Link word to be used in the Description. If the expected and observed impact match, then "driven by" otherwise "despite"
4. List down all the "nodes" from the <Knowledge Base>. Check for each node and then tell if it has an incoming or outgoing edge. if yes mention the edge.
5. From 4. List all nodes without an edge aloong withh its change numbers in a format seen in the <Example Description>
</Instructions>

- Using 3.from <Instruction> produce a Description that is very similar in structure and language to the <Example Description>.
- Make sure not to include any reasons or impact beyond what is mentioned in 3.
- You should simply describe the causal links with the change numbers for 3.
- Make use of the % change value in the Description, enclosed in (%change vs LY).
- Add information in 5. using one line statement just describing the values and %change.
- The Description should be a single paragraph.
- Dont talk about anything else apart from what you see as the output 3. and 5.
- Dont make use of terms like "edge" and "node"
- Make use of exact names present in the <Knowledge Base>
- For Demand alone make sure to show the actual $ amount before (%change vs LY)

Just Follow instructions one by one."""
    extraction_prompt = """Extract only the final description exactly from the input.

    INPUT
    {output}

    Produce just the final description and nothing else.
"""

    correction_prompt = """You need reformat a provided summary to match the structure and tonality of a reference paragraph.
    
    Generated Summary: {generated_summary}

    Reference Summary: Demand at 59.3M (+4.3% vs LY) with the launch of SleekTech Activewear and promotional pricing on activewear (LY 50% Off Sleepwear). Traffic was down (-4% vs LY). Conversion rate (2% vs LY) for second consecutive week. AOS was up ($77 vs LY $22) was driven by more UPT.

    Now scrutinize every sentence in the Generated Summary one by one and suggest modifications where ever needed. Proper use of brackets is important as the reference summary is a business document.
    Make use of knowledge base to fact check the numbers.

    At the end produce a modified summary enclosed within ```Summary```
"""

    
    client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
    response = client.chat.completions.create(
        model="pfz-gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a summary creator from causal link creator summarizing business performance."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.1
    )
    
    summary = response.choices[0].message.content.replace("YoY", "vs LY")
    with open(f"summary/{brand}_final_summary.txt", "w", encoding="utf-8") as file:
        if summary is not None:
            file.write(summary)
        else:
            file.write("")

    response = client.chat.completions.create(
        model="pfz-gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a summary creator from causal link creator summarizing business performance."},
            {"role": "user", "content": extraction_prompt.format(output = summary)}
        ],
        temperature = 0.1
    )
    
    summary = response.choices[0].message.content.replace("YoY", "vs LY")
    with open(f"edited_summary/{brand}_edit_summary.txt", "w", encoding="utf-8") as file:
        if summary is not None:
            file.write(summary)
        else:
            file.write("")

    print(f"summary saved successfully for {brand}")
    


# with open("derived/fil_data_causal_map.json", "r") as file:
#     map = json.load(file)

# with open("derived/filtered_df.json", "r") as file:
#     filtered_df = json.load(file)

# generate_summary_from_causal_link(map, filtered_df)

def process_causal_maps(cm_folder, derived_folder, brand_selected):
    cm_files = {f.split('_causal_map.json')[0]: os.path.join(cm_folder, f) for f in os.listdir(cm_folder) if f.endswith('_causal_map.json')}
    derived_files = {f.split('_filtered_data.json')[0]: os.path.join(derived_folder, f) for f in os.listdir(derived_folder) if f.endswith('_filtered_data.json')}
    
    common_brands = cm_files.keys() & derived_files.keys()
    
    if brand_selected == "All":
        pass
    else:
        common_brands = {brand_selected}

    for brand in common_brands:
        cm_file_path = cm_files[brand]
        derived_file_path = derived_files[brand]



        with open(cm_file_path, 'r') as cm_file:
            causal_map = cm_file.read()
        
        with open(derived_file_path, 'r') as derived_file:
            filtered_df = json.load(derived_file)
        
        generate_summary_from_causal_link(causal_map, filtered_df, brand)

