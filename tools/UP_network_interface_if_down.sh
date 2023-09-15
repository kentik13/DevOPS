#!/bin/bash
output="$(ip link show enp1s0f1 | grep UP)"
if [[ -n $output ]]  
then
    printf -- "%s\n" "Interface is UP"
else
    printf -- "Interface is DOWN, trying UP\n"
    ip link set enp1s0f1 up
fi
