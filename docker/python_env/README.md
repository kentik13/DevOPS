# Docker
Docker makes it easy to run emulators, but we had problems with the number 
of file descriptors on a large number of VISONIC BBA panels.
Therefore, we are not using docker in our tests yet,
but nevertheless QA may well use docker to start the load.


##  Install docker

- [docker documentation](https://docs.docker.com/engine/install/)
- [compose documentation](https://docs.docker.com/compose/install/)


## Start load scripts via docker

-  set up load script (in this default case  ../load/DSC/PSP/config.py)
 
### Start docker image via docker-compose

- set changes into docker-compose.yml

- ``docker-compose build``

- ``docker-compose up``

###  Start docker image load via docker

```
docker run --name psp_emus --rm \
  -u 1000 --ulimit nofile=65000:65000 \
  --volume ../load/DSC/PSP:/usr/local/performance:rw \
  docker.visonic.com/system/performance:0.0.1
```
- Stop runing
```
docker stop psp_emus
docker rm -f psp_emus
```
