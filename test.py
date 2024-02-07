from os import listdir, remove
import json
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
                            

                with open(f"./src/full/{f}", 'w') as file:
                    file.write(json.dumps(template))
                

                
                
    print(i)

main()