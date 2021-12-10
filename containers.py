import docker
from io import StringIO
client = docker.from_env()
f = open('./runs.tar', 'wb')
container = client.containers.create("torrent", ["python","main.py"],network_mode="host")
print("searching IPs")
container.start()
container.exec_run(["python","main.py"])
print("finished scrapping IPs")
strm,status = container.get_archive("/root/runs/")
for d in strm:
    f.write(d)
f.close()
print("finished writing tar file")
