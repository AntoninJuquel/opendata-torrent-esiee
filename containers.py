import docker
from io import StringIO
client = docker.from_env()
f = open('./bulkTorrents.tar', 'wb')
container = client.containers.create("torrent", ["python","scrap.py"],network_mode="host")
print("scrapping torrents")
container.start()
container.exec_run(["python","scrap.py"])
print("finished scrapping torrents")
strm,status = container.get_archive("/root/bulkTorrents/")
for d in strm:
    f.write(d)
f.close()
print("finished writing tar file")
