import requests
from bs4 import BeautifulSoup

url = "https://ettv.unblockit.ws/torrents.php?order=asc&sort=id"
#url = "https://ettv.unblockit.ws/torrent/5/it-stains-the-sands-red-2016-1080p-bluray-x264-rovers-ethd"
page = requests.get(url).content

soup = BeautifulSoup(page, "lxml")
print(soup.prettify())
