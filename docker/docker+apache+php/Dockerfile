FROM ubuntu 
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update 
RUN apt-get -y install apache2
RUN apt-get -y install apache2-utils
RUN apt-get -y install php
RUN apt clean 
COPY ./index.php /var/www/html/index.php
EXPOSE 80
CMD apachectl -D FOREGROUND
