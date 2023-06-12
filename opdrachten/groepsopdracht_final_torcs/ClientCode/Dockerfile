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

RUN git clone https://github.com/Inzui/TINLABML_22-23-Group4.git
EXPOSE 3001

ENTRYPOINT ["bash", "TINLABML_22-23-Group4/opdrachten/groepsopdracht_final_torcs/start_client.sh"]