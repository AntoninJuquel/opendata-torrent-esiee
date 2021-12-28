# Open data torrent

## Install

Prerequisites :
- docker
- snap (to install the latest version of chromium)
- chromium
- gcc
- pip 
- virtualenv (to install in a virtualenv)

``` shell
sudo apt-get install docker.io
sudo apt install snapd
sudo snap install chromium # version above 95
sudo apt-get install build-essential
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
```

Now install the python dependencies

``` shell
virtualenv env
source env/bin/activate # recommended to use a virtual environment
pip install -r requirements.txt
```

## Usage

Once you installed the project you just have to do :

``` shell
python live.py
```

## Configuration

For configuration please edit the config.txt file a sample is provided for you

https://dan.folkes.me/2012/04/converting-a-magnet-link-into-a-torrent/
https://matix.io/finding-peers-from-a-torrent-file-in-python/
https://pytutorial.com/python-get-country-from-ip-python
https://realpython.com/beautiful-soup-web-scraper-python/
https://stackoverflow.com/questions/51213717/beautiful-soup-not-loading-the-entire-page
https://stackoverflow.com/questions/64165726/selenium-stuck-on-checking-your-browser-before-accessing-url


https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/258
