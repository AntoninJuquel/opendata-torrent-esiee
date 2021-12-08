from archlinux
RUN pacman -Syyu --noconfirm
RUN pacman -S --noconfirm python python-pip gcc base base-devel
COPY . /root/
WORKDIR /root/
RUN pip install -r requirements.txt
