from os import listdir
from os.path import isfile, join
from crawl import TorrentCrawler
from threading import Thread
from datetime import date
import os
import json

mypath = "bulkTorrents"
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
f = open('bulkTorrents/index.json','r')
data = json.load(f)

def threaded_crawl(file):
    crawler = TorrentCrawler(mypath + "/" + file,time=20)
    ip = crawler.get_peers_raw()
    countries = crawler.get_countries()
    today = date.today()
    print(countries)
    res = { 'date' : str(today),
            'total people': len(ip),
            'size' : data[file]["size"],
            'cat' : data[file]["cat"],
            'lang' : data[file]["lang"],
            'ip' : ip,
            'countries' : countries
            }
    #jsonString = json.dumps(res)
    filename = 'runs/{}.json'.format(file.split("/")[-1])
    filename.replace(" ","_")
    with open(filename, 'w') as outfile:
        jsonString = json.dumps(res)
        outfile.write(jsonString)
        #json.dump(jsonString, outfile)

for file in files:
    if file != "index.json":
        print(file)
        threaded_crawl(file)
        thread = Thread(target=threaded_crawl, args=(file,)) 
        thread.start()



