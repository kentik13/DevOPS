#!/bin/bash

websites=("bloomex.com.au" "bloomex.ca" "blossomshop.ca")

for site in "${websites[@]}"; do
    echo "Checking SSL certificate for $site:"
    openssl s_client -connect "$site:443" 2>/dev/null | openssl x509 -noout -dates | awk -F= '/notAfter/ {print $2}'
    echo
done

