import json
sample = "medicalCardiac"

with open('./src/templates/medical.json') as f:
    data = json.load(f)
for key, value in data.items(): 
    print(f"KEY: {key}")
    updated = key.split('medical')[1]
    print(f"Update: -> {updated.upper()}")

