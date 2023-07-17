#!/usr/bin/env bash
echo "Fibro port : $1"
PORT=$1
echo "CS count : $2"
COUNT=$2

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


function ctrl_c() {
    echo "** Trapped by signal **"
    echo "** Stopping locust **"
    echo "Kill SG Receiver PID = $PID_RECEIVER_FIBRO"
    kill -s KILL $PID_RECEIVER_FIBRO
    deactivate
    exit 0
}

start_receiver() {
    python fibrocs.py $PORT $COUNT &
    PID_RECEIVER_FIBRO=$!
    echo "Fibro Receiver PID = $!"
    sleep 1

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
