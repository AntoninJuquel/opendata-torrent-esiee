import os, json
import pandas as pd


def parse(path_to_json):
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    my_dict = {}
    data = {}
    for j in json_files:
        # Opening JSON file
        f = open(path_to_json + j,"r")
        
        # returns JSON object as
        # a dictionary
        data[j] = json.load(f)
        f.close()
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent= 4)

    data = {}
    final = {
        "abs": 
        {
            "sizes":[], 
            "amounts":[]
        }
    }
    for j in json_files:
        # Opening JSON file
        f = open(path_to_json + j,"r")
        
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        for country in data["countries"]:
            if country in my_dict:
                if data["size"] in my_dict[country]:
                    my_dict[country][data["size"]] += data["countries"][country]
                else:
                    my_dict[country][data["size"]] = data["countries"][country]
            else:
                my_dict[country] = { data["size"]: data["countries"][country] }

            if(data["size"] not in final["abs"]["sizes"]):
                final["abs"]["sizes"].append(data["size"])
                final["abs"]["amounts"].append(0)
                final["abs"]["sizes"] = sorted(final["abs"]["sizes"])
        f.close()
    
    final["abs"]["sizes"] = [str(x) for x in final["abs"]["sizes"]]

    with open('my_dict.json', 'w') as outfile:
        json.dump(my_dict, outfile, indent= 4)

    for country in my_dict:
        a_test = my_dict[country]
        dictionary_items = a_test.items()
        sorted_items = sorted(dictionary_items)
        new_dict = {"sizes":[], "amounts":[]}
        for tpl in sorted_items:
            new_dict["sizes"].append(str(tpl[0]))
            new_dict["amounts"].append(tpl[1])
        final[country] = new_dict
    with open('final.json', 'w') as outfile:
        json.dump(final, outfile, indent= 4)
        
    return my_dict

parse("runs/")