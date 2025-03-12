import json
import re

def extract_numeric_value(text):
    match = re.search(r"\(([-+]?[0-9]*\.?[0-9]+)", text)
    return float(match.group(1)) if match else None

def update_mappings(json_db, causal_map):
    # Extract user_id and brand_name from causal_map
    causal_user_id = causal_map.get("user_id", "").lower()
    causal_brand_name = causal_map.get("brand_name", "").lower()
    
    # Create a lookup dictionary for quick access, grouped by user_id and brand_name
    mapping_dict = {}
    for entry in json_db:
        key = (entry["user_id"].lower(), entry["brand_name"].lower())
        if key not in mapping_dict:
            mapping_dict[key] = {}
        for mapping in entry["mappings"]:
            mapping_dict[key][(mapping["source"].lower(), mapping["destination"].lower())] = mapping
    
    # Ensure causal map user_id and brand_name exist in mapping_dict
    key = (causal_user_id, causal_brand_name)
    if key not in mapping_dict:
        return json_db  # No matching user_id and brand_name, return unchanged
    
    # Iterate over causal map edges
    for edge in causal_map["edges"]:
        source = edge["start"].lower()
        destination = edge["end"].lower()
        impact_value = extract_numeric_value(edge["value"])
        
        if (source, destination) in mapping_dict[key] and impact_value is not None:
            mapping = mapping_dict[key][(source, destination)]
            
            if edge["impact"] == "positive":
                if impact_value < mapping["low"]:
                    mapping["low"] = impact_value
                if impact_value > mapping["high"]:
                    mapping["high"] = impact_value
            elif edge["impact"] == "negative":
                if impact_value > mapping["high"]:
                    mapping["high"] = impact_value
                if impact_value < mapping["low"]:
                    mapping["low"] = impact_value
    
    return json_db

# Sample input
# json_db = [
#     {
#         "user_id": "user_123",
#         "brand_name": "XYZ Corp",
#         "mappings": [
#             {
#                 "source": "Promotion",
#                 "destination": "Demand",
#                 "low": 7,
#                 "high": 10
#             },
#             {
#                 "source": "Traffic",
#                 "destination": "Sales",
#                 "low": 5,
#                 "high": 35
#             }
#         ]
#     }
# ]

# causal_map = {
#     "user_id": "user_456",
#     "brand_name": "XYZ Corp",
#     "nodes": [
#         {"id": "Promotion", "value": "promotional pricing on activewear"},
#         {"id": "Demand", "value": "Demand at 59.3M (+4.3% vs LY)"},
#         {"id": "Traffic", "value": "Traffic was down -4% vs LY"}
#     ],
#     "edges": [
#         {"start": "Promotion", "end": "Demand", "impact": "positive", "value": "Demand at 59.3M (+4.3% vs LY) with promotional pricing on activewear"},
#         {"start": "UPT", "end": "AOS", "impact": "positive", "value": "AOS was up ($77 vs LY $22) was driven by more UPT"}
#     ]
# }

with open("causal_map.json", "r") as file:
    causal_map = json.load(file)

with open("db_json.json", "r") as file:
    json_db = json.load(file)

print(causal_map)
# updated_json_db = update_mappings(json_db, causal_map)
# print(json.dumps(updated_json_db, indent=4))
