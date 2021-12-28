#!/usr/bin/env python3
import os
from os import listdir
from os.path import isfile, join
from math import ceil


class ProgressManager():
    def __init__(self):
        self.progress_types = ["runs","selenium"]
        self.progress_labels = {"runs":"Fetching new data, please wait",
                                "selenium":"Selenium is starting, please wait"}

    def _write(self,text):
        with open("tmp/progress.txt","w") as file:
            file.write(text)

    def _get_num_of_torrent(self):
        mypath = "bulkTorrents"
        files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print(files)
        return len(files) - 1

    def _add_num_step(self,num_step):
        num_step = num_step.split("/")
        num_step[0] = str(int(num_step[0]) + 1)
        return "/".join(num_step)

    def write_line(self,line):
        self._write(line)

    def create_progress(self,progress_type,scrapeNum=None):
        if scrapeNum:
            steps = (scrapeNum + 1) * 8
        else:
            steps = ceil(self._get_num_of_torrent() / 10)
        line = "{}\n0/{}".format(self.progress_labels[progress_type],steps)
        self.write_line(line)

    def add_progress(self,line):
        with open("tmp/progress.txt","r") as file:
            text = file.read()
            text = text.split("\n")
            new_step = self._add_num_step(text[1])
            new_text = "{}\n{}".format(line,new_step)
        self.write_line(new_text)

    def clean_file(self):
        self.write_line("")

    def show(self):
        with open("tmp/progress.txt","r") as file:
            text = file.read()
        return text
