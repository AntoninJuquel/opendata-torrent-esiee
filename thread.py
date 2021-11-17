from crawl import TorrentCrawler
from threading import Thread

def threaded1():
    crawler = TorrentCrawler("cached_torrent_files/ecf4-Captain Marvel (2019) [WEBRip] [1080p] [YTS.AM].torrent")
    print("Number of peers :",len(crawler.get_peers_raw()))
    print(crawler.get_countries())

def threaded2():
    crawler = TorrentCrawler("cached_torrent_files/arch.torrent")
    print("Number of peers :",len(crawler.get_peers_raw()))
    print(crawler.get_countries())

thread1 = Thread(target=threaded1)
thread1.start()
thread2 = Thread(target=threaded2)
thread2.start()

# use thread like that to pass arg
#Thread(target=processLine, args=(dRecieved,)) 
