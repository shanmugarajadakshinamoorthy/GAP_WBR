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
        r"```Summary(.*?)```"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return None

# def extract_summary(text):
#     match = re.search(r"Summary:\n(.*)", text, re.DOTALL)
#     return match.group(1).strip() if match else None

def generate_summary_from_causal_link(summary, filtered_df, brand, destination_folder="edited_summary"):
    """Compare trends and generate a business summary using LLM."""
    """Compare trends and generate a business summary using LLM."""
    kb = summary
    graph = {"nodes":[], "edges":[]}
    found_demand = False
    for node in summary["nodes"]:
        temp = {}
        if node['id'] == "demand":
            found_demand = True
        if node["id"] != "AOS":
            temp = {"id":node["id"]}
            val = float(round(filtered_df[0][node["id"]],2))
            val = int(val) if int(val) == val else val
            temp["value"] = val
            change = round(float(filtered_df[0][node["id"] + "_YoY"]),1)
            change = int(change) if int(change) == change else change
            temp["change"] = f"""{"+" if change > 0 else ""}{str(change)}% VS LY"""

        else:
            temp = {"id":node["id"]}
            val = float(round(filtered_df[0][node["id"]],2))
            val = int(val) if int(val) == val else val
            temp["value"] = val
            curr = round(float(filtered_df[0][node["id"]]),0)
            last = round(float(filtered_df[0][node["id"]+"_LY"]),0)
            temp["change"] = f"""${curr} VS LY ${last}"""
        
        graph["nodes"].append(temp)
    
    if not found_demand:
        temp = {}
        temp = {"id":"demand"}
        val = float(round(filtered_df[0]["demand"],2))
        val = int(val) if int(val) == val else val
        temp["value"] = val
        change = round(float(filtered_df[0]["demand" + "_YoY"]),1)
        change = int(change) if int(change) == change else change
        temp["change"] = f"""{"+" if change > 0 else ""}{str(change)} VS LY"""
        graph["nodes"].insert(0, temp)

    graph["edges"] = [{"start":i["start"], "end":i["end"]} for i in summary["edges"]]


    prompt = f"""You are Data Describer. You just interpret Knowledge Base to produce a meaningful sequence of information.

<Your Inputs>

1. Knowledge Base
 - This contains nodes and edges
 - Nodes : All the KPIs that should be explained as part of the summary.
   -- Schema : "id" -> Name of the KPI/Event
	            "value" -> Current value of the KPI.
                "change" -> The change in value of KPI compared to last year. This is how the change should be described in the summary.
 - Edges : All the KPIs that impact the other KPIs. The summary should contain a causal reason for these.
   -- Schema : "start" -> KPI that makes the impact
	            "end" -> KPI that receives the impact.

</Your Inputs>

Now Look at the inputs below

<Knowledge Base>

{graph}

</Knowledge Base>


<Sample Description>
Demand at 59.3M (+4.3% vs LY) with the launch of SleekTech Activewear and promotional pricing on activewear (LY 50% Off Sleepwear). Traffic was down (-4% vs LY). Conversion (2% vs LY) for second consecutive week. AOS was up ($77 vs LY $22) was driven by more UPT.
</Sample Description>

<Instructions Set 1>
1. Make a list of all the nodes mentioned in "edges" in the knowledge base <Knowledge Base>
2. On the "edges" mentioned in <Knowledge Base> perform group by "end node" and collect the names of all the "Start Node". Produce collection of **start nodes** for each **end node**
3. For each group in 2 for each "Start Nodes" do the following:
   a. Definition of #Start Node Name#. For BRAND related Node use just the brand name.
   b. Expected impact of #Start Node Name# on Current Node (Description and reason)
   c. Observed impact of #Start Node Name# on Current Node as seen in the <Knowledge Base> (Description)
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
    Knowledge Base: {knowledge_base}

    Generated Summary: {generated_summary}


    Reference Summary: Demand at 59.3M (+4.3% vs LY) with the launch of SleekTech Activewear and promotional pricing on activewear (LY 50% Off Sleepwear). Traffic was down (-4% vs LY). Conversion (2% vs LY) for second consecutive week. AOS was up ($77 vs LY $22) was driven by more UPT.

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
    - $ symbol must be used before the Demand value. Example: Change ""Demand at 1.4M"" to ""Demand at $1.4M"".
    - Make sure units are used where needed. Use $ for price and demand related things and % for percentage change related things.

    Now scrutinize every sentence in the Generated Summary one by one and suggest modifications where ever needed. Proper use of brackets is important as the reference summary is a business document.
    For all the checks for each sentence in Generated Summary and mention you comments for each check.
    You are just a **format checker**. You should not add any new information to the generated Summary.
    Make use of Actual Data to fact check the numbers.
    If any change numbers for a KPI are missing, add it.

    At the end produce a modified summary enclosed within ```Summary```
"""

    client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
    print("step_0")
    response = client.chat.completions.create(model='pfz-gpt-4o',
        messages=[
            {"role": "system", "content": "You are a summary creator from causal link creator summarizing business performance."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.1
    )
    
    summary = response.choices[0].message.content.replace("YoY", "vs LY")
    
    print('step1')
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
    print('step2')
    # # print(filtered_df)
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
            {"role": "user", "content": correction_prompt.format(generated_summary = summary, knowledge_base=graph)}
        ],
        temperature = 0.1
    )
    print('step3')
    correct_summary = correct_summary.choices[0].message.content.replace("YoY", "vs LY")
    correct_summary = extract_summary(correct_summary).replace("_demand_contribution", "")
    correct_summary = correct_summary.split("```Summary")[-1].split("```")[0].replace("```", "").rstrip("\n").lstrip("\n")
    
    
    with open(f"{destination_folder}/{brand}_edit_summary.txt", "w", encoding="utf-8") as file:
        if correct_summary is not None:
            file.write(correct_summary)
        else:
            file.write("")

    print(f"summary saved successfully for {brand}")
    


# with open("CM_filtered/ATHL_causal_map.json", "r") as file:
#     map = json.load(file)

# with open("derived/ATHL_filtered_data.json", "r") as file:
#     filtered_df = json.load(file)

# print(generate_summary_from_causal_link(map, [filtered_df], "ATHL"))

def process_causal_maps(cm_folder, derived_folder, brand_selected="All", destination_folder = None):
    # cm_files = {f.split('_causal_map.json')[0]: os.path.join(cm_folder, f) for f in os.listdir(cm_folder) if f.endswith('_causal_map.json')}
    cm_files = {f.split('_causal_map_suppressed.json')[0]: os.path.join(cm_folder, f) for f in os.listdir(cm_folder) if f.endswith('_causal_map_suppressed.json')}
    derived_files = {f.split('_filtered_data.json')[0]: os.path.join(derived_folder, f) for f in os.listdir(derived_folder) if f.endswith('_filtered_data.json')}
    
    # print('cm_files', cm_files)
    # print('derived_files', derived_files)
    
    common_brands = cm_files.keys() & derived_files.keys()
    print('common_brands', common_brands)
    if brand_selected == "All":
        pass
    else:
        common_brands = {brand_selected}

    for brand in common_brands:
        cm_file_path = cm_files[brand]
        derived_file_path = derived_files[brand]



        with open(cm_file_path, 'r') as cm_file:
            causal_map = json.load(cm_file)
        
        with open(derived_file_path, 'r') as derived_file:
            filtered_df = json.load(derived_file)
        
        if destination_folder is None:
            generate_summary_from_causal_link(causal_map, [filtered_df], brand)
        else:
            generate_summary_from_causal_link(causal_map, [filtered_df], brand, 'overall')