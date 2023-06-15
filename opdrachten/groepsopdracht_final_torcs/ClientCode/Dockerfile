FROM ubuntu:20.04

# Set Timezone
RUN echo "Europe/Amsterdam" > /etc/timezone

# Install packages
RUN apt-get update --yes \
        && apt-get upgrade --yes \
        && apt install --yes

RUN apt-get install pip -y
RUN apt-get install git -y

WORKDIR /opt/app

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone -b DockerReady https://github.com/Inzui/TINLABML_22-23-Group4.git
EXPOSE 3001 3002 3003 3004 3005 3006 3007 3008 3009 3010


ENTRYPOINT ["python3", "TINLABML_22-23-Group4/opdrachten/groepsopdracht_final_torcs/ClientCode/main.py"]