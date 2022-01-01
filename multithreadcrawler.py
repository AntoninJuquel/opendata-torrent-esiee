from os import listdir
from os.path import isfile, join
from crawl import TorrentCrawler
from threading import Thread
from datetime import date
import os
import json
from progress import ProgressManager


def threaded_crawl(file,data):
    """
    Cette fonction lance l'analyse d'un fichier torrent
    """
    mypath = "bulkTorrents"
    crawler = TorrentCrawler(mypath + "/" + file,time=20)
    ip = crawler.get_peers_raw()
    info = crawler.get_countries_info()
    countries = info[0]
    locs = info[1]
    today = date.today()
    print(countries)
    res = { 'date' : str(today),
            'total people': len(ip),
            'size' : data[file]["size"],
            'cat' : data[file]["cat"],
            'lang' : data[file]["lang"],
            'ip' : ip,
            'locs': locs,
            'countries' : countries
            }
    filename = 'runs/{}.json'.format(file.split("/")[-1])
    filename.replace(" ","_")
    with open(filename, 'w') as outfile:
        jsonString = json.dumps(res)
        outfile.write(jsonString)

def crawl_by_batch():
    """
    Cette fonction lance les analyses par batch de 10 fichiers torrent en parralèle
    """
    mypath = "bulkTorrents"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    f = open('bulkTorrents/index.json','r')
    data = json.load(f)
    f.close()
    i = 0
    all_threads = []
    for file in files:
        if file != "index.json":
            if i<10:
                i += 1
                thread = Thread(target=threaded_crawl, args=(file,data))
                thread.start()
                all_threads.append(thread)
            else:
                threaded_crawl(file,data)
                i = 0
                ProgressManager().add_progress("crawling...")

    thread_still_running = 1
    while thread_still_running != 0:
        thread_still_running = 0
        for thread in all_threads:
            if thread.is_alive():
                thread_still_running += 1
    ProgressManager().write_line("finished crawling")


def purge_runs():
    """
    Cette fonction supprime tout les fichiers dans le dossier runs
    et ainsi supprime toutes les données récoltés
    """
    mypath = "runs/"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in files:
        os.remove("runs/"+f)
