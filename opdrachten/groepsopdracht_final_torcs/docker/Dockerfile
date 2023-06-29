FROM continuumio/miniconda3:23.3.1-0

LABEL maintainer="J.A.Boogaard@hr.nl"

# Set Timezone
RUN echo "Europe/Amsterdam" > /etc/timezone

RUN apt-get --yes update \
    && apt-get --yes upgrade

WORKDIR /opt/app

# Add requirements
RUN conda update --all \
    && conda install -y pandas scikit-learn \
    && pip install --upgrade pip keyboard 

# Add runtime code
ADD ClientCode/*.py /opt/app/
ADD ClientCode/Drivers /opt/app/Drivers
ADD ClientCode/Dto /opt/app/Dto
ADD ClientCode/Models /opt/app/Models
ADD ClientCode/Services /opt/app/Services

EXPOSE 3004

ENTRYPOINT ["python", "/opt/app/main.py"]