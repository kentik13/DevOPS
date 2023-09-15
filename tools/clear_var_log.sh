#!/bin/bash
cd /var/log
for i in *.log; do echo -n "$i " ; > $i ; done
