import undetected_chromedriver.v2 as uc
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
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

def execute_scrapping(n):
    options = uc.ChromeOptions()
    options.headless=True
#p = {"download.default_directory": "/home/porus/Coding/opendata-torrent/bulkTorrents/"}
#options.add_argument("user-agent=Mozilla/5.0 (Linux; {Android Version}; {Build Tag etc.})  AppleWebKit/{WebKit Rev} (KHTML, like Gecko) Chrome/{Chrome Rev} Mobile Safari/{WebKit Rev}")
#options.add_experimental_option("prefs", p)
#driver = webdriver.Chrome(options=options)
#driver = uc.Chrome(options=options)
def execute_scrapping(n):
    driver = uc.Chrome()
    with driver:
        driver.get('https://unblockit.bz/')
        url = "https://ettv.unblockit.bz/"
        ettv = driver.find_element_by_partial_link_text('ETTV')
        #ettv.click()
        #time.sleep(8)
        #movies = driver.find_element_by_partial_link_text('TV Shows')
        #movies.click()
        print("waiting for cloudfare")
        all_matches = []
        wait = 5
        for torrent_url in category_urls:
            print("FETCHING URL :", torrent_url)
            driver.get(torrent_url)
            time.sleep(wait)
            wait = 2
            html = driver.page_source
            matches_raw = re.findall(r'<a[^>]* href="([^"]*)"', html)
            matches = []
            for i in matches_raw:
                print(i)
            for match in matches_raw:
                if match.startswith("/torrent/"):
                    matches.append(match)
            incrementor = 0
            for match in matches:
                if match not in all_matches:
                    all_matches.append(match)
                    incrementor += 1
                    if incrementor == n:
                        break
        print(all_matches)
        print(len(all_matches))
        for i in all_matches:
            print(i)
        fileDict = {}
        i = 0
        #all_matches = all_matches[500:]
        for match in all_matches:
            i += 1
            print(i,"/",len(all_matches))
            try:
                with open('bulkTorrents/index.json') as json_file:
                    fileDict = json.load(json_file)
            except:
                fileDict = {}
            print("Going TO : !!!")
            print(match)
            url = match
            time.sleep(2)
            if match.startswith("/torrent"):
                url = "https://ettv.unblockit.bz" + match
            driver.get(url)
            time.sleep(1)
            html = driver.page_source
            torrents = re.findall(r'<a[^>]* href="([^"]*)"', html)
            # if len(torrents) == 0:
            #     continue
            # print(torrents)
            torrentFileUrl = ""
            torrent_xpath = "/html/body/div/div[3]/div/div[2]/div[3]/div[1]/div[4]/fieldset/ul[1]/li[2]/a"
            try:
                #torrentFileUrl = torrent_href.get_attribute("href")
                a_tag = driver.find_element_by_xpath("//a[contains(@href, 'etorrent.click/torrents/')]")
                torrentFileUrl = a_tag.get_attribute("href")
                print("torrent url is :",torrentFileUrl)
            except:
                print("We didn't get the url")
                continue
            # for torrent in torrents:
            #     print("SEARCHING TORRENT FILE")
            #     if "etorrent.click/torrents" in torrent:
            #         torrentFileUrl = torrent
            torrentFilename = torrentFileUrl.replace("https://etorrent.click/torrents/","")
            print("torrent file is :",torrentFilename)
            print(torrentFilename)
            print("FILE IS :", torrentFilename)
            print("IS THE FILE IN THE DICT ? :", torrentFilename in fileDict)
            if torrentFilename in fileDict:
                # we already have the file stored
                print("hmm")
                #continue
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
            fileDict[torrentFilename] = {"size": filesize, "cat": category, "lang": language}
            res = requests.get(torrentFileUrl)
            with open("bulkTorrents/" + torrentFilename, 'wb') as file:
                file.write(res.content)

            filename = 'bulkTorrents/index.json'
            with open(filename, 'w') as outfile:
                jsonString = json.dumps(fileDict)
                outfile.write(jsonString)

if __name__ == '__main__':
    execute_scrapping(1)
