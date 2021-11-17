files = [
"dataTorrent/Books/038d-Marvel Week+ (10-23-2019).torrent",
"dataTorrent/Books/1104-50 Assorted Magazines - January 16 2019.torrent",
"dataTorrent/Books/5350-Marvel Week+ (08-19-2020).torrent",
"dataTorrent/Books/d716-50 Assorted Magazines - October 6 2020 Part 1.torrent",
"dataTorrent/Books/d9fc-Marvel Week+ (09-25-2019).torrent",
"dataTorrent/Films/0ba9-rambo-last-blood-2019[1080p][BluRay].torrent",
"dataTorrent/Films/46fe-john-wick-chapter-3-parabellum-2019[1080p][WebRip].torrent",
"dataTorrent/Films/a79b-dark-phoenix-2019[1080p][BluRay].torrent",
"dataTorrent/Films/c821-spider-man-far-from-home-2019[1080p][WebRip].torrent",
"dataTorrent/Films/ecf4-Captain Marvel (2019) [WEBRip] [1080p] [YTS.AM].torrent",
"dataTorrent/Music/864e-Drake - Certified Lover Boy (Explicit) (2021) Mp3 320kbps [PMEDIA].torrent",
"dataTorrent/Music/946c-VA - Greatest Hits Ever (2019) Mp3 320kbps [PMEDIA].torrent",
"dataTorrent/Music/954a-Taylor Swift - folklore (2020) Mp3 (320kbps) [Hunter].torrent",
"dataTorrent/Music/d3a5-VA - NOW 100 Hits Party (2019) Mp3 320kbps [PMEDIA].torrent",
"dataTorrent/Music/f739-Nas - King's Disease (2020) Mp3 (320kbps) [Hunter].torrent",
"dataTorrent/Porn/1804-392d8bee8236eeb74546c9a7e145379b.torrent",
"dataTorrent/Porn/2c23-81d21cb3917d38eee71e8a3d3a1799dc.torrent",
"dataTorrent/Porn/abae-FamilyStrokes.19.01.17.Rose.Monroe.Staycation.Sex.Blues.XXX.1080p.MP4-KTR.torrent",
"dataTorrent/Porn/af20-65eca9bcd097052db446b9be567e9453.torrent",
"dataTorrent/Porn/c320-6906492fae9c6554af58475db7a03187.torrent",
"dataTorrent/Series/08d3-The.Mandalorian.S01E06.2019.1080p.WEBRip.X264.AC3-EVO[TGx]-3827.torrent",
"dataTorrent/Series/3e41-Chernobyl.S01E04.720p.WEBRip.x264-TBS[TGx]-16239.torrent",
"dataTorrent/Series/54e0-Game.of.Thrones.S08E05.WEB.H264-MEMENTO[eztv].mkv.torrent",
"dataTorrent/Series/81ab-game.of.thrones.s08e06.web.h264-memento[eztv].mkv.torrent",
"dataTorrent/Series/b459-Rick.and.Morty.S04E04.Claw.and.Hoarder.Special.Ricktims.Morty.HDTV.x264-CRiMSON[TGx]-27342.torrent",
]
from crawl import TorrentCrawler
from threading import Thread
from datetime import date
import os
import json

def threaded_crawl(file):
    crawler = TorrentCrawler(file,time=5)
    file_size = os.path.getsize(file)
    ip = crawler.get_peers_raw()
    countries = crawler.get_countries()
    today = date.today()
    print(countries)
    res = { 'date' : str(today),
            'total people': len(ip),
            'size' : file_size,
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
    thread = Thread(target=threaded_crawl, args=(file,)) 
    thread.start()


# use thread like that to pass arg
