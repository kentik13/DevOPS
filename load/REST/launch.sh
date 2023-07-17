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

CONF="config.py"
#SERVER_IP=`egrep -i '^SERVER_IP' $CONF | awk -F'[" ]+' '{ print $3 }'`
#FLASK_PORT=`egrep -i '^FLASK_PORT' $CONF | awk -F'[" ]+' '{ print $3 }'`
#MASTER_IP=`egrep -i '^MASTER_IP' $CONF | awk -F'[" ]+' '{ print $3 }'`
#MASTER_PORT=`egrep -i '^MASTER_PORT' $CONF | awk -F'[" ]+' '{ print $3 }'`
#MASTER_WEB_PORT=`egrep -i '^MASTER_WEB_PORT' $CONF | awk -F'[" ]+' '{ print $3 }'`
CLIENT_NUMBER=`egrep -i '^client_number' $CONF | awk -F'[" ]+' '{ print $3 }'`
SPAWN_RATE=`egrep -i '^spawn_rate' $CONF | awk -F'[" ]+' '{ print $3 }'`
SERVER_HOST=`egrep -i '^SERVER_HOST' $CONF | awk -F'[" ]+' '{ print $3 }'`
SERVER_PORT=`egrep -i '^SERVER_PORT' $CONF | awk -F'[" ]+' '{ print $3 }'`

_PID=`echo $$`
_date=`date +%m-%d-%Y-%H-%M-%S`
#cores=$((`nproc --all` - 1))

NOW=$(date +"%F_%H-%M")
PATH_TO_LOG="./debug_log"
LOG="$PATH_TO_LOG/locust_run_$NOW.log"
LOG_LEVEL=`egrep -i '^LOG_LEVEL' $CONF | awk -F'[" ]+' '{ print $3 }'`

mkdir -p "$PATH_TO_LOG"

function ctrl_c() {
    echo "** Trapped by signal **"
    echo "** Stopping locust **"
    echo "Kill LOCUST PID = $PID_LOCUST"
    kill -s KILL $PID_LOCUST
    echo "Kill TAIL PID = $PID_TAIL"
    kill -s KILL $PID_TAIL

    deactivate
    exit 0
}

start_locust() {
    # START LOCUST
    echo -e "\nStart LOCUST\n"
    locust -f locust_scenario.py --headless -L $LOG_LEVEL --logfile=$LOG -u $CLIENT_NUMBER --print-stats -r $SPAWN_RATE \
    --host "https://$SERVER_HOST:$SERVER_PORT"&
    PID_LOCUST=$!
    echo "LOCUST PID = $PID_LOCUST"

    sleep 3
    tail -f $LOG &
    PID_TAIL=$!
    echo "TAIL PID = $PID_TAIL"
}

loop() {
    while (true) do
        date
        echo -e "\nTo terminate LOAD script press keys \"CTRL-C\"\n"
        sleep 3600
    done
}

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT SIGTERM

start_locust

loop
