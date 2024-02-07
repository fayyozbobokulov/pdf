from os import listdir, remove
import json
from typing import List, Dict
def filter_out_matches(array1, array2):
    titles = {item['title'] for item in array2}  # Use a set for faster lookup
    # Keep items where the description does not match any title
    filtered_array1 = [item for item in array1 if item['description'] not in titles]
    return filtered_array1
def main():
    filenames = listdir('./src/templates/')
    with open('./sample.json', 'r') as templates:
        data = json.load(templates)
        i = 0
    for f in filenames:
        with open(f"./src/templates/{f}", "r") as file:
            template = json.load(file)
        for [key, value] in data.items():
            if value['name'].strip() == template['name'].strip() or value['title'].strip() == template['name'].strip():
                i+=1
                print({"their": value["name"], "my": template['name']})
                template['title'] = value['title']
                template['certifications'] = value['certifications']
                for skill in value['skills']:
                    # print(skill)
                    for [s, sv] in template['skills'].items():
                        if(skill['type'] == 'ratingsTable' and skill['identifier'] == s):
                            sv['title'] = skill['title']
                            sv['type'] = skill['type']
                            if skill.get('items', False):
                                sv['items'] = skill['items']
                                sv['questions'] = filter_out_matches(sv['questions'], skill['items'])
                with open(f"./src/full/{f}", 'w') as file:
                    file.write(json.dumps(template))          
    print(i)

main()