import undetected_chromedriver.v2 as uc
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import requests

category_urls = [
        "https://ettv.unblockit.bz/torrents.php?parent_cat=TV&parent_cat=TV&sort=seeders&order=desc",
        "https://ettv.unblockit.bz/torrents.php?parent_cat=Movies&parent_cat=Movies&sort=seeders&order=desc",
        "https://ettv.unblockit.bz/torrents.php?parent_cat=Software&parent_cat=Software&sort=seeders&order=desc",
        "https://ettv.unblockit.bz/torrents.php?parent_cat=Music&parent_cat=Music&sort=seeders&order=desc",
        "https://ettv.unblockit.bz/torrents.php?parent_cat=Games&parent_cat=Games&sort=seeders&order=desc",
        "https://ettv.unblockit.bz/torrents.php?parent_cat=Anime&parent_cat=Anime&sort=seeders&order=desc",
        "https://ettv.unblockit.bz/torrents.php?parent_cat=Books&parent_cat=Books&sort=seeders&order=desc",
        "https://ettv.unblockit.bz/torrents.php?parent_cat=Adult&parent_cat=Adult&sort=seeders&order=desc",
]

def getfilesize(filesize):
    filesize = filesize.split(" ")
    num = float(filesize[0])
    unit = filesize[1]
    if unit == "MB":
        return num
    elif unit == "GB":
        return num * 1000
    elif unit == "KB":
        return num / 1000
    else :
        return None 

options = webdriver.ChromeOptions()
p = {"download.default_directory": "/home/porus/Coding/opendata-torrent/bulkTorrents/"}
options.add_argument("user-agent=Mozilla/5.0 (Linux; {Android Version}; {Build Tag etc.})  AppleWebKit/{WebKit Rev} (KHTML, like Gecko) Chrome/{Chrome Rev} Mobile Safari/{WebKit Rev}")
options.add_experimental_option("prefs", p)
#driver = webdriver.Chrome(options=options)
#driver = uc.Chrome(options=options)
driver = uc.Chrome()
with driver:
    driver.get('https://unblockit.bz/')
    url = "https://ettv.unblockit.bz/"
    ettv = driver.find_element_by_partial_link_text('ETTV')
    #ettv.click()
    #time.sleep(8)
    #movies = driver.find_element_by_partial_link_text('TV Shows')
    #movies.click()
    all_matches = []
    for torrent_url in category_urls:
        print("FETCHING URL :", torrent_url)
        driver.get(torrent_url)
        html = driver.page_source
        matches = re.findall(r'<a[^>]* href="([^"]*)"', html)
        matches = [e for e in matches if "/torrent/" in e]
        for match in matches:
            if match not in all_matches:
                all_matches.append(match)
    print(all_matches)
    print(len(all_matches))
    for i in all_matches:
        print(i)
    exit()
    fileDict = {}
    i = 0
    for match in all_matches[30:]:
        i += 1
        print(i,"/",len(all_matches))
        with open('bulkTorrents/index.json') as json_file:
            fileDict = json.load(json_file)
        print("Going TO : !!!")
        print(match)
        url = match
        time.sleep(2)
        driver.get(url)
        time.sleep(1)
        html = driver.page_source
        torrents = re.findall(r'<a[^>]* href="([^"]*)"', html)
        torrentFileUrl = ""
        for torrent in torrents:
            if "etorrent.click/torrents" in torrent:
                torrentFileUrl = torrent
        torrentFilename = torrentFileUrl.replace("https://etorrent.click/torrents/","")
        print("FILE IS :", torrentFilename)
        print("IS THE FILE IN THE DICT ? :", torrentFilename in fileDict)
        if torrentFilename in fileDict:
            # we already have the file stored
            continue
        try:
            print("GETTING FILE INFO")
            size = driver.find_element_by_xpath("/html/body/div/div[3]/div/div[2]/div[3]/div[1]/div[1]/fieldset/dl[4]/dd")
            cat = driver.find_element_by_xpath("/html/body/div/div[3]/div/div[2]/div[3]/div[1]/div[1]/fieldset/dl[2]/dd")
            lang = driver.find_element_by_xpath("/html/body/div/div[3]/div/div[2]/div[3]/div[1]/div[1]/fieldset/dl[3]/dd")
            filesize = size.text
            category = cat.text
            language = lang.text
            filesize = getfilesize(filesize)
        except:
            # skip this invalid page
            continue
        #print("Your file is : {} MB.".format(filesize))
        print("DOWNLOADING THE FILE")
        torrentFileUrl = ""
        fileDict[torrentFilename] = {"size": filesize, "cat": category, "lang": language}
        res = requests.get(torrentFileUrl)
        with open("bulkTorrents/" + torrentFilename, 'wb') as file:
            file.write(res.content)
        filename = 'bulkTorrents/index.json'
        with open(filename, 'w') as outfile:
            jsonString = json.dumps(fileDict)
            outfile.write(jsonString)


