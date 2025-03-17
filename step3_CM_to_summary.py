import json
import os

import openai
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(override=True)
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Load JSON data (historic trends)
import re


def read_credentials_from_file(file_path):
    """Read Azure OpenAI credentials from a text file."""
    credentials = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    credentials[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: Credentials file not found at {file_path}")
        exit(1)

    return credentials

# creds_file_path = "azure_openai_creds.txt"
# credentials = read_credentials_from_file(creds_file_path)

# def extract_summary(text):
#     match = re.search(r"<Summary>(.*?)</Summary>", text, re.DOTALL)
#     return match.group(1).strip() if match else text.split("<Summary>")[-1] if len(text.split("<Summary>")) > 1 else None

def extract_summary(TEXT1):
    # Regular expression to capture the summary content
    pattern = r"```Summary\n(.*?)\n```"

    # Extracting the summary
    match = re.search(pattern, TEXT1, re.S)
    if match:
        text2 = match.group(1).strip()
        # print("Extracted text2:", text2)
        return text2
    else:
        text2=" "
        print("Summary not found")
        return text2

def generate_summary_from_causal_link(summary, filtered_df, brand):
    """Compare trends and generate a business summary using LLM."""
    kb = summary
    prompt = f"""You are Data Describer. You just interpret Raw Data and Knowledge Base to produce a meaningful sequence of information.

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

<Instructions Set 1>
1. Make a list of all the nodes mentioned in "edges" in the knowledge base <Knowledge Base>
2. On the "edges" mentioned in <Knowledge Base> perform group by "end node" and collect the names of all the "Start Node". Produce collection of **start nodes** for each **end node**
3. For each group in 2 for each "Start Nodes" do the following:
   a. Definition of #Start Node Name#. For BRAND related Node use just the brand name.
   b. Expected impact of #Start Node Name# on Current Node (Description and reason)
   c. Observed impact of #Start Node Name# on Current Node as seen in the <Data JSON> (Description)
   d. Do the Expected and Observed impact the same? (Yes/No)
   e. Link word. If the expected and observed impact match, then "driven by" otherwise "despite"
4. List down all the "nodes_ids" mentioned under *nodes* from the <Knowledge Base>. Check for each node and then tell if it has an incoming or outgoing edge. if yes mention the edge.
5. From 4. List all nodes without an edge along with its change numbers in a format seen in the <Example Description>
</Instructions Set 1>


<Instruction Set 2>
- Using 3.from <Instruction Set 1> produce a Description that is very similar in structure and language to the <Example Description>.
- Make sure not to include any reasons or impact beyond what is mentioned in 3.
- You should simply describe the causal links with the change numbers for 3.
- Change should be described as:
    a.  AOS -> you should mention change like (<$AOS> VS LY <$AOS_LY>). Bracket is important.
    a.  Other KPIs -> you should mention change like (%change VS LY). Bracket is important.
- Add information in 5. using one line statement just describing the values and (%change VS LY). Bracket is important.
- The Description should be a single paragraph.
- Dont talk about anything else apart from what you see as the output 3. and 5.
- Dont make use of terms like "edge" and "node". Do not make use of terms like "Edge" and "Node"
- Make use of exact names present in the <Knowledge Base> except for Brand_Contribution.
- For Demand alone make sure to show the actual $ amount before (%change vs LY). Trim the number using K, M etc.
- If Demand declined, produce the summary in order of top retractors first.
- If Demand increased, produce the summary in order of top drivers first.
</Instruction Set 2>


Just Follow Instructions one by one."""

    extraction_prompt = """Extract only the final description exactly from the input.

    INPUT
    {output}

    Produce just the final description and nothing else."""

    correction_prompt = """You need reformat a provided summary to match the structure and tonality of a reference paragraph.

    Actual Data Schema:
        - All keys that contain the suffix "YoY" contain % change from last year.
        - All keys that contain the suffix "LY" show the last year numbers.

    Actual Data: {filtered_df}

    Generated Summary: {generated_summary}


    Reference Summary: Demand at 59.3M (+4.3% vs LY) with the launch of SleekTech Activewear and promotional pricing on activewear (LY 50% Off Sleepwear). Traffic was down (-4% vs LY). Conversion rate (2% vs LY) for second consecutive week. AOS was up ($77 vs LY $22) was driven by more UPT.

    Checks:
    - Change in all metrics should be represented by comparing "VS LY"
    - The change number must be under a bracket in this format (%change VS LY) or ($ThisYear VS LY $LastYear). This is very important.
    - The %change or $Change value must be inside the bracket like
       a. For AOS : ""($213 VS LY $245)
       b. For Other Metrics: ""(+5% VS LY)""

    - Change any repeating % numbers or $ numbers like
       a. For AOS: ""$514 ($514 VS LY $413)"" to ""($514 VS LY $413)"".
       b. For Other Metrics: ""4% (+4% VS LY)"" to ""(+4% VS LY)"".

    - Change any formatting issues like
       a. For AOS:  ""$415 (VS LY $560)"" to ""($415 VS LY $560)"".
       b. For Other Metrics:  ""-2% (VS LY)"" to ""(-2% VS LY)"" and .

    - For AOS, the change number must be presented using change in the actual dollar amount every time. Like ($321 VS LY $213).


    Now scrutinize every sentence in the Generated Summary one by one and suggest modifications where ever needed. Proper use of brackets is important as the reference summary is a business document.
    For all the checks for each sentence in Generated Summary and mention you comments for each check.
    You are just a **format checker**. You should not add any new information to the generated Summary.
    Make use of Actual Data to fact check the numbers.

    At the end produce a modified summary enclosed within ```Summary```
"""

    client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )

    response = client.chat.completions.create(model='pfz-gpt-4o',
        messages=[
            {"role": "system", "content": "You are a summary creator from causal link creator summarizing business performance."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.1
    )

    summary = response.choices[0].message.content.replace("YoY", "vs LY")
    # print(summary)

    with open(f"summary/{brand}_final_summary.txt", "w", encoding="utf-8") as file:
        if summary is not None:
            file.write(summary)
        else:
            file.write("")

    response = client.chat.completions.create(
        model='pfz-gpt-4o',
        messages=[
            {"role": "system", "content": "You are a summary creator from causal link creator summarizing business performance."},
            {"role": "user", "content": extraction_prompt.format(output = summary)}
        ],
        temperature = 0.1
    )

    summary = response.choices[0].message.content.replace("YoY", "vs LY")
    # print(filtered_df)
    # filtered_df_trim = {}

    # for key in kb["nodes"]:
    #     if key["id"] in filtered_df[0]:
    #         filtered_df_trim.update({key["id"]:filtered_df[0][key["id"]]})
    #     if key["id"]+"_LY" in filtered_df[0]:
    #         filtered_df_trim.update({key["id"]+"_LY":filtered_df[0][key["id"]+"_LY"]})
    #     if key["id"]+"_YoY" in filtered_df[0]:
    #         filtered_df_trim.update({key["id"]+"_YoY":filtered_df[0][key["id"]+"_YoY"]})

    # print(filtered_df_trim)

    correct_summary = response = client.chat.completions.create(
        model='pfz-gpt-4o',
        messages=[
            {"role": "system", "content": "You are a summary creator from causal link creator summarizing business performance."},
            {"role": "user", "content": correction_prompt.format(generated_summary = summary, filtered_df=filtered_df)}
        ],
        temperature = 0.1
    )
    #correct_summary = extract_summary(correct_summary.choices[0].message.content.replace("YoY", "vs LY"))
    correct_summary = (correct_summary.choices[0].message.content.replace("YoY", "vs LY"))
    correct_summary = extract_summary(correct_summary)
    # print("correct_summary:",correct_summary)

    with open(f"edited_summary/{brand}_edit_summary.txt", "w", encoding="utf-8") as file:
        if correct_summary is not None:
            file.write(correct_summary)
        else:
            file.write("")

    print(f"summary saved successfully for {brand}")



# with open("derived/fil_data_causal_map.json", "r") as file:
#     map = json.load(file)

# with open("derived/filtered_df.json", "r") as file:
#     filtered_df = json.load(file)

# generate_summary_from_causal_link(map, filtered_df)

def process_causal_maps(cm_folder, derived_folder, brand_selected="All"):
    cm_files = {f.split('_causal_map.json')[0]: os.path.join(cm_folder, f) for f in os.listdir(cm_folder) if f.endswith('_causal_map.json')}
    derived_files = {f.split('_filtered_data.json')[0]: os.path.join(derived_folder, f) for f in os.listdir(derived_folder) if f.endswith('_filtered_data.json')}

    common_brands = cm_files.keys() & derived_files.keys()
    if brand_selected == "All":
        pass
    else:
        common_brands = {brand_selected}
    print("common_brands:", common_brands)
    for brand in common_brands:
        cm_file_path = cm_files[brand]
        derived_file_path = derived_files[brand]

        with open(cm_file_path, 'r') as cm_file:
            causal_map = cm_file.read()


        with open(derived_file_path, 'r') as derived_file:
            filtered_df = json.load(derived_file)

        generate_summary_from_causal_link(causal_map, filtered_df, brand)

