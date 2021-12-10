from archlinux
COPY filesForDocker/pacman.conf /etc/pacman.conf
RUN pacman -Syyu --noconfirm
RUN pacman -S --noconfirm python python-pip gcc 
RUN pacman -S --noconfirm base base-devel 
RUN pacman -Syu --noconfirm 
RUN pacman -S --noconfirm xorg-server-xvfb
RUN pacman -S --noconfirm chromium
COPY . /root/
WORKDIR /root/
RUN pip install -r requirements.txt
