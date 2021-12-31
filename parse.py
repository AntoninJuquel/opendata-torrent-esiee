import os, json

def sizeToIntervalStr(size):
  sizeint = int(float(size))
  hundreds = sizeint-sizeint%100
  return f"{hundreds} - {hundreds + 99}"

def parse(path_to_json):
    """
    Cette fonction va lire les fichiers dans le dossiers runs et les parser
    pour ecrire les fichiers json/bar.json et json/geo.json
    """
    tmp = {}
    bar = {
        "abs": 
        {
            "sizes":[], 
            "amounts":[]
        }
    }
    geo = {}

    if os.path.exists(path_to_json) == False:
        with open('json/geo.json', 'w') as outfile:
            json.dump(geo, outfile, indent= 4)
        with open('json/bar.json', 'w') as outfile:
            json.dump(bar, outfile, indent= 4)
        return
    
    json_files_name = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for json_file_name in json_files_name:
        # Ouverture et ajout des données du fichier aux données geographiques
        with open(path_to_json + json_file_name,"r") as outfile:
            geo[json_file_name] = json.load(outfile)

        # Cumul du nombre de téléchargements par taille de fichier par pays
        for country in geo[json_file_name]["countries"]:
            if country in tmp:
                if geo[json_file_name]["size"] in tmp[country]:
                    tmp[country][geo[json_file_name]["size"]] += geo[json_file_name]["countries"][country]
                else:
                    tmp[country][geo[json_file_name]["size"]] = geo[json_file_name]["countries"][country]
            else:
                tmp[country] = { geo[json_file_name]["size"]: geo[json_file_name]["countries"][country] }

            # Calibrage de l'axe des abscisses
            if(geo[json_file_name]["size"] not in bar["abs"]["sizes"]):
                bar["abs"]["sizes"].append(geo[json_file_name]["size"])
                bar["abs"]["amounts"].append(0)
                bar["abs"]["sizes"] = sorted(bar["abs"]["sizes"])
            
            # On trie les tailles des fichier
            sorted_items = sorted(tmp[country].items())
            bar[country] = {"sizes":[], "amounts":[]}
            for item in sorted_items:
                bar[country]["sizes"].append(str(item[0]))
                bar[country]["amounts"].append(item[1])
            
            # Transformation des données chiffrées en intervales de 100mo
            bar[country]["sizes"] = [sizeToIntervalStr(size) for size in bar[country]["sizes"]]

    with open('json/geo.json', 'w') as outfile:
        json.dump(geo, outfile, indent= 4)
    
    # Calibrage de l'axe des abscisses
    bar["abs"]["sizes"] = [str(x) for x in bar["abs"]["sizes"]]
    bar["abs"]["sizes"] = [sizeToIntervalStr(size) for size in bar["abs"]["sizes"]]

    with open('json/bar.json', 'w') as outfile:
        json.dump(bar, outfile, indent= 4)