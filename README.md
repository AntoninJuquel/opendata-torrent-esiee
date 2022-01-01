# Open data torrent

Le projet open data torrent a pour but d'analyser un certain nombre de fichiers torrents de toute les catégories, et d'analyser, la taille de fichier les plus téléchargés, les pays qui télécharge le plus, et de voir sur la carte où se situe les personne ayant téléchargé.

## Raport d'Analyse

- reflète bien les résultats obtenus ces résultats sont commentés sa forme est de qualité (structuration, rédaction, etc...)

## Guide d'utilisateur
### Installation

Dépendances :
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

Installation des dépendances python

``` shell
virtualenv env
source env/bin/activate # recommended to use a virtual environment
pip install -r requirements.txt
```

### Utilisation

Une fois les dépendances installées, vous pouvez lancer le fichier main.py

``` shell
python main.py
```

- Une fois arrivé sur le dashboard, supprmier les données existante cliquez sur "purge data"
- Si vous voulez plus de fichiers torrents que ceux fourni dans le projet par défaut, saisissez le nombre de fichiers souhaité et cliquez sur scrape new torrents
- une fois que vous avez vos fichiers torrents, cliquez sur fetch new data, pour analyser vos fichers
- le dashboard se met à jour régulièrement, vous pouvez avoir du mal à zoomer sur les données, avant de zoomer, veuillez mettre sur pause le dashboard avec le boutton pause en haut à gauche de l'écran

### Configuration

L'exemple du fichier de configuration :

``` shell
selenium_in_docker=0
btdht_in_docker=0
root_url=https://ettv.unblockit.tv
wait=3
wait-safe-cloudfare=10
```

- selenium_in_docker prends pour valeur soit 1 ou 0 (0, selenium sera lancé dans un docker, 1 il sera lancé de manière classique)
- btdht_in_docker prends pour valeur soit 1 ou 0 (0, btdht sera lancé dans un docker, 1 il sera lancé de manière classique)
- root_url prends en paramètre l'url du site
- wait prend un entier, il correspond aux pauses que va faire selenium en secondes (recommendé de le mettre à au moins 3 secondes)
- wait-safe-cloudfare prend aussi un entier, et il correspond au nombre de secondes attendu dans l'écran de chargement de cloudflare (recommendé de laisser au mois 6 secondes)

Si votre connection internet est lente ou bien vous le faites tourner dans un machine virtuelle, n'hésiter pas à augementer le nombre de secondes.

Comme le site ETTV est un site de torrent, il arrive souvent qu'il ai changé d'URL, dans ce cas là veuillez mettre à jour l'URL.
Vous pourrez retrouver l'URL d'ETTV sur ce site : https://unblockit.tv/

## Guide de développeur
Voici quelques informations utiles pour pouvoir développer sur notre projet

### Diagramme

``` mermaid
graph TD
    A[main.py] -->|click sur fetch new data button| B(multithreadcrawler.py)
    A[main.py] -->|click sur scrap new torrents| C(scrap.py)
    A[main.py] -->|après avoir saisi le nombre de fichiers, montre le nombre de fichier total| D(progress.py)
    A[main.py] -->|appelle en continu les figures| E(figures.py)
    A[main.py] -->|appelle en continu pour savoir la progression| D(progress.py)
    B[multithreadcrawler.py] -->|appelle les fonctions pour analyser les fichiers torrents| G(crawl.py)
    D[progress.py] -->|écris et lis| H(progress.txt)
    E[figures.py] -->|parse les fichiers en appelant| I(parse.py)
    C[scrap.py] -->|écrire la progression| D(progress.py)
    B[multithreadcrawler.py] -->|écrire la progression| D(progress.py)
    C[scrap.py] -->|Lis les configurations| J(config.py)
    J[config.py] -->|Lis le fichier| K(config.txt)
    L[containers.py] -->|Crée une conteneur à partir de| M(Dockerfile)
```


### config.py
Ce fichier va lire le fichier config.txt et va retourner un dictionnaire dans lequel on pourra réccupérer les informations entré par l'utilisateur

### containers.py
Ce fichier va se charger de créer un conteneur docker dans le cas où l'utilisateur aurait un soucis avec les librairies utlisé par ce projet. Cependant, cette fonction n'est pas abouti.

### crawl.py
Ce fichier ce charge d'analyser les fichiers torrents stocké dans le répertoire "bulkTorrents/"

### figures.py
Ce fichier génère les deux figures utilisé dans ce projet : l'histogramme, et la carte

### main.py
Ce fichier va lancer le dashboard, c'est dans ce fichier qu'on doit faire les modification pour l'interface 

### multithreadcrawler.py
Ce fichier va lancer les analyse des fichiers torrent en parralèle pour cela il va appeler le fichier crawl.py

### parse.py 
Ce fichier lis les fichiers json du dossier runs/ et va parser en fichier json/bar.json et json/geo.json, respectivement pour l'histogramme et la carte

### progress.py
Ce fichier contient toute la logique de la progression

### progress.py
Ce fichier va lancer le scrapping des fichiers torrent à partir du site internet ETTV

## Problèmes rencontrés

L'un des plus grand challenge de notre projet, était de coder le crawler, on avait pas trouver beaucoup de documentation pour utiliser BTDHT.

Autre problème qu'on a recontré par la suite est que l'on ne pouvait pas utiliser des liens magnet dans notre projet (facile à avoir), mais il nous fallait des fichier .torrent (un peu plus compliqué).

Les essais pour convertir des liens magnets en fichier torrent n'ont pas marché.

Une fois que nous avions trouvé une site de torrent qui propose aussi des fichiers torrents : ETTV; mais le problème est que ce site comme beaucoup d'autre sites similaires est protégé avec une protection cloudflare qui empêche les attaques type DDOS et les bots.

Mais avec de la chance on a trouvé une librairie Selenium qui a su passer outre cette protection.

Avec le scrappeur et le crawler (qui analyse) les fichiers torrents marchait, mais le problème était que le crawler était beaucoup trop lent. Il lui fallait 30 secondes par fichiers pour pouvoir retourner assez d'informations, pour pallier à ça nous avons introduit l'execution des analyse en parralèle.

Lorsque l'on faisait plusieurs tests par jour pour débugger, on a excédé rapidement le quota offert par l'API ipinfo.io, nous avons donc fait un compte qui nous donne une quota suffisant gratuitement, et nous avons intégré le token en dure dans le code.

Tout marchait parfaitment, mais on s'est rendu compte que les librairies ne s'installé pas correctement sous Windows, nous avions envisagé la solution docker, mais elle n'a pas abouti.

Nous avons adapté notre guide de manière à aider les utilisateur sous Linux, malheuresement nous n'avons pas de solution pour l'heure sur les autres OS. 
Le Dockerfile cependant est fonctionnel et va créer un conteneur sous Arch avec toute les dépendances du code.


## Sources
- https://matix.io/finding-peers-from-a-torrent-file-in-python/
- https://pytutorial.com/python-get-country-from-ip-python
- https://stackoverflow.com/questions/64165726/selenium-stuck-on-checking-your-browser-before-accessing-url
- https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/258
