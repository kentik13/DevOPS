#!/bin/bash
echo "Checking expired users in 2023:"
cd /root/easy-rsa_operators_2022/pki/issued
echo "Users list:"
for i in *.crt; do echo -n "$i " ; openssl x509 -enddate -noout -in $i | cut -c10-29; done | grep 2023
