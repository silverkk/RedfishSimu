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

# install openresty http://openresty.org/en/linux-packages.html
RUN apt-get -y install wget gnupg ca-certificates
RUN wget -O - https://openresty.org/package/pubkey.gpg | apt-key add -
RUN echo "deb http://openresty.org/package/ubuntu bionic main" |  tee /etc/apt/sources.list.d/openresty.list
RUN apt-get update
RUN apt-get -y install openresty

RUN cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
RUN cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak

CMD mkdir /grilledfish
#copy the config files for nginx
COPY ./tools/ /grilledfish/tools/
COPY ./grilledfish/ /grilledfish/grilledfish/
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/default /etc/nginx/sites-available/default
COPY ./docker/nginx/nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key
COPY ./docker/nginx/nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt
COPY ./docker/nginx/self-signed.conf /etc/nginx/snippets/self-signed.conf
COPY ./start_script.sh /grilledfish/start_script.sh

# copy the config files for openresty
CMD mkdir /usr/local/openresty/nginx/conf/snippets
RUN cp /usr/local/openresty/nginx/conf/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf.bak
COPY $grilledfish_path/docker/openresty/nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY $grilledfish_path/docker/nginx/self-signed.conf /usr/local/openresty/nginx/conf/snippets/self-signed.conf

EXPOSE 80
EXPOSE 443

RUN chmod u+x /grilledfish/start_script.sh

ENTRYPOINT ["/grilledfish/start_script.sh"]


