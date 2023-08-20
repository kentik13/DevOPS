FROM python:3.8.12

# docker build -t docker.visonic.com/system/perfomance:0.0.1

MAINTAINER Anton Dmytrenko <anton.dmytrenko-ext@jci.com>
USER root

ENV DEBIAN_FRONTEND noninteractive

RUN : apt-get autoremove -y \
    && apt-get update -y \
    && apt-get install -y \
       unzip \
       build-essential libssl-dev libffi-dev \
       tzdata \
       sudo \
       iputils-ping \
       locales \
       lsof \
       bc

RUN pip3 install -U --trusted-host uapypi.visonic \
    --force-reinstall -i http://uapypi.visonic:8085/simple/ pip

RUN pip3 install -U --trusted-host uapypi.visonic \
    --force-reinstall -i http://uapypi.visonic:8085/simple/ \
       setuptools \
       paramiko \
       requests \
       pyOpenSSL \
       scp \
       pyserial \
       python-dateutil \
       lxml \
       simplejson \
       bunch \
       websocket-client \
       PyCRC \
       xlrd \
       Pillow \
       python-magic

RUN pip3 install -U --trusted-host uapypi.visonic \
    --force-reinstall -i http://uapypi.visonic:8085/simple/ \
    ipmp==1.6.92 \
    testcase==1.0.46 \
    autolib==1.0.99 \
    atl==1.1.21 \
    locust==1.4.3 \
    \
    && mkdir -p /usr/local/performance

ENV TZ "Europe/Kiev"
RUN echo "Europe/Kiev" | tee /etc/timezone \
  && dpkg-reconfigure --frontend noninteractive tzdata

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

WORKDIR /usr/local/performance

#-- make it possible to build unprivileged
RUN adduser --uid 1000 qaload ; \
    chmod 777 /home/qaload ; \
    { echo; echo '#1000 ALL=(ALL) NOPASSWD:ALL'; } >> /etc/sudoers ; \
    chown -R 1000:1000 /usr/local ;

#-- drop root, everything below done with user perms
USER 1000


CMD  ["/usr/local/performance/launch.sh"]
