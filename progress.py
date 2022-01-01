#!/usr/bin/env python3
import os
from os import listdir
from os.path import isfile, join
from math import ceil


class ProgressManager():
    def __init__(self):
        """
        C'est la fonction constructeur, il ne prends pas de paramètre mais
        on y déclare les variables utilisé au sein de la classe
        """
        self.progress_types = ["runs","selenium"]
        self.progress_labels = {"runs":"Fetching new data, please wait",
                                "selenium":"Selenium is starting, please wait"}

    def _write(self,text):
        """
        Ecris le texte passé en paramètre dans le fichier progress.txt
        """
        with open("tmp/progress.txt","w") as file:
            file.write(text)

    def _get_num_of_torrent(self):
        """
        Retourne le nombre de fichiers torrent
        """
        mypath = "bulkTorrents"
        files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print(files)
        return len(files) - 1

    def _add_num_step(self,num_step):
        """
        Ajoute 1 au nombre d'étape dans la progression
        """
        num_step = num_step.split("/")
        num_step[0] = str(int(num_step[0]) + 1)
        return "/".join(num_step)

    def write_line(self,line):
        """
        Ecris le texte passé en paramètre dans le fichier progress.txt
        """
        self._write(line)

    def create_progress(self,progress_type,scrapeNum=None):
        """
        Crée une progression, le type de ce dernier est passé en
        paramètre, s'il s'agit d'un scrapping, il faut fournir en paramètre
        le nombre de fichiers scrappé
        """
        if scrapeNum:
            steps = (scrapeNum + 1) * 8
        else:
            steps = ceil(self._get_num_of_torrent() / 10)
        line = "{}\n0/{}".format(self.progress_labels[progress_type],steps)
        self.write_line(line)

    def add_progress(self,line):
        """
        Cette fonction écris la suite de la progression avec le titre de l'étape
        """
        with open("tmp/progress.txt","r") as file:
            text = file.read()
            text = text.split("\n")
            new_step = self._add_num_step(text[1])
            new_text = "{}\n{}".format(line,new_step)
        self.write_line(new_text)

    def clean_file(self):
        """
        Supprime toute les lignes du fichier de progression
        """
        self.write_line("")

    def show(self):
        """
        Affiche le contenu du fichier progress.txt
        """
        with open("tmp/progress.txt","r") as file:
            text = file.read()
        return text
