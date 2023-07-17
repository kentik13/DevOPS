#!/usr/bin/env bash

activate_env() {
  # activate Python env
  if source $HOME/visonic_env/bin/activate; then
    echo "Start python env: $HOME/visonic_env/bin/activate"
  elif source $HOME/visonicpy_env38/bin/activate; then
    echo "Start python env: $HOME/visonicpy_env38/bin/activate"
  elif source $HOME/visonic-venv3.6/bin/activate; then
    echo "Start python env: $HOME/visonic-venv3.6/bin/activate"
  else
    echo "Fail to launch python env. Abort scenario. Please check Python environment!"
    exit 1
  fi
}

if [ -f /.dockerenv ]; then
    echo "Start Docker container";
else
    activate_env;
fi

ulimit -n 65000 && ulimit -c unlimited


#Set emulator ports:

SG_PORT="1111"           #SG - mlr2
FEP_PORT="2222"          #FEP - fep
VIS_PORT="3333"          #VIS - visnap

function ctrl_c() {
    echo "** Trapped by signal **"
    echo "** Stopping locust **"
    echo "Kill SG Receiver PID = $PID_RECEIVER_SG"
    kill -s KILL $PID_RECEIVER_SG
    echo "Kill FEP RECEIVER PID = $PID_RECEIVER_FEP"
    kill -s KILL $PID_RECEIVER_FEP
    echo "VIS RECEIVER PID = $PID_RECEIVER_VIS"
    kill -s KILL $PID_RECEIVER_VIS
    deactivate
    exit 0
}

start_receiver() {
    cs $SG_PORT SG -logname=sg.log -logsize 100 --per_account_log -events_db_size=10000 &
    PID_RECEIVER_SG=$!
    echo "SG Receiver PID = $!"
    sleep 1
    cs $FEP_PORT FEP -logname=fep.log -logsize 100 --per_account_log -events_db_size=10000  &
    PID_RECEIVER_FEP=$!
    echo "FEP RECEIVER PID = $!"
    sleep 1
    cs $VIS_PORT VIS -logname=vis.log -logsize 100 --per_account_log -events_db_size=10000  &
    PID_RECEIVER_VIS=$!
    echo "VIS RECEIVER PID = $!"

}

loop() {
    while (true) do
        date
        echo -e "\nTo terminate Receiver script press keys \"CTRL-C\"\n"
        sleep 3600
    done
}

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT SIGTERM

start_receiver

loop
