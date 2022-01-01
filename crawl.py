import bencode
import hashlib
import btdht
import binascii
from time import sleep
import requests

class TorrentCrawler:
    """
    Cette classe a pour but de parcourir les fichier torrent 
    et c'est lui qui va nous retourner les infomations que l'on vas traiter
    par la suite
    """
    def __init__(self, torrentfile, time = 30):
        """
        Dans ce constructeur nous allons lire les informations qui se trouvent
        sur le fichier torrent et lancer le DHT (Distributed hash table) et 
        commencer à remplir la liste des peers, ensuite la liste des pays
        """
        self.time = time
        with open(torrentfile,'rb') as f: 
            raw_data = f.read()
        self.data = bencode.decode(raw_data)
        self.info_hash = hashlib.sha1(bencode.bencode(self.data["info"])).hexdigest()
        self.dht = btdht.DHT()
        self.dht.start() #should wait about 1 sec for it to start
        self.peers = self.get_peers_raw()
        self.countries_dict = {}

    def get_peers_raw(self, rerun = True):
        """Cette fonction retourne les personnes qui téléchargent ou bien 
        transfert le fichier, par défaut la fonction relance le scan sur 
        le torrent, et attends par défaut 20 secondes, ces valeurs sont
        modifiables.
        """
        time = self.time
        if rerun==True:
            self.peers = []
            while time>=0:
                new_list = self.dht.get_peers(binascii.a2b_hex(self.info_hash))
                if new_list is not None:
                    for peer in new_list:
                        if peer not in self.peers:
                            self.peers.append(peer)
                time -= 1
                sleep(1)
        return self.peers

    def get_countries_info(self):
        """
        Méthode pour obtenir un dictionnaire de pays
        avec le code du pays en clé et pour valeur le nombre de peers
        de ce pays
        """
        countries_dict = {}
        locs = []
        for ipinfo in self.peers:
            info = self._get_info_country(ipinfo[0])
            country = info[0]
            loc = info[1]
            locs.append(loc)
            if country in countries_dict:
                countries_dict[country] += 1
            else:
                countries_dict[country] = 1
        return [countries_dict, locs]


    def _get_info_country(self, ip):
        """
        Méthode pour obtenir le pays associé à l'addresse ip
        """
        url = "https://ipinfo.io/{}/json?token=8cf4887baf8f77".format(ip)
        res = requests.get(url)
        if res.status_code != 200:
            return "Error " + str(res.status_code)
        return [res.json()["country"], res.json()["loc"]]

