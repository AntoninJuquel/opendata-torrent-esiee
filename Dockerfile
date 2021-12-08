from archlinux
RUN pacman -Syyu --noconfirm
RUN pacman -S --noconfirm python python-pip gcc base base-devel
COPY requirements.txt /root/requirements.txt
COPY . /root/
RUN python /root/main.py
