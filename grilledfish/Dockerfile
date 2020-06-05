#This is a sample Image 
FROM ubuntu:18.04 as base

ENV http_proxy "http://child-prc.intel.com:913"
ENV https_proxy "http://child-prc.intel.com:913"

SHELL ["/bin/bash", "-c"]

RUN apt-get update
#RUN apt-get upgrade -y

RUN apt-get install -y apt-transport-https

RUN apt-get install -y unzip

RUN apt install -y build-essential 
RUN apt install -y libssl-dev 
RUN apt install -y libffi-dev 

RUN mkdir environments 
RUN cd environments

RUN apt-get install -y python3
RUN apt install -y python3-dev
RUN apt install -y python3-venv
RUN apt install -y python3-pip
RUN python3 -m venv redfish_env
RUN source redfish_env/bin/activate

RUN pip3 install django
RUN pip3 install wheel
RUN pip3 install uwsgi

RUN apt-get install -y apt-utils
RUN apt-get install -y nginx 
RUN apt install -y vim
RUN apt-get install iputils-ping -y

RUN cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak

CMD mkdir /grilledfish
COPY ./grilledfish/ /grilledfish/grilledfish/
COPY ./docker/nginx/default /etc/nginx/sites-available/default
COPY ./docker/nginx/nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key
COPY ./docker/nginx/nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt
COPY ./docker/nginx/self-signed.conf /etc/nginx/snippets/self-signed.conf
COPY ./start_script.sh /grilledfish/start_script.sh


EXPOSE 80
EXPOSE 443

RUN chmod u+x /grilledfish/start_script.sh

ENTRYPOINT ["/grilledfish/start_script.sh"]


