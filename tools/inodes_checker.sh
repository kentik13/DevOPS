#!/bin/bash

THRESHOLD=85  # Threshold percentage

# Get hostname
HOSTNAME=$(hostname)

# Get all partitions except tmpfs and devtmpfs (optional, adjust as needed)
PARTITIONS=$(df -x tmpfs -x devtmpfs -P | awk 'NR>1 {print $6}' | egrep -v "core|efi|certbot")

for PARTITION in $PARTITIONS; do
    # Get inode usage percentage for each partition
    INODE_USAGE=$(df -i $PARTITION | awk 'NR==2 {print $5}' | sed 's/%//')
    
    # Check if INODE_USAGE is a number (integer)
    if [[ "$INODE_USAGE" =~ ^[0-9]+$ ]]; then
        # Compare inode usage with the threshold
        if [ $INODE_USAGE -ge $THRESHOLD ]; then
            MESSAGE="Hostname: $HOSTNAME - Inode usage on partition $PARTITION is ${INODE_USAGE}%, exceeding threshold of $THRESHOLD%."
            
            # Telegram bot configuration (replace with your bot's token and chat ID)
        BOT_TOKEN="BOT_TOKEN"
        CHAT_ID="CHAT_ID"
            
            # Telegram API URL
            TELEGRAM_API="https://api.telegram.org/bot${BOT_TOKEN}/sendMessage"
            
            # Send message to Telegram
            curl -s -X POST $TELEGRAM_API -d chat_id=$CHAT_ID -d text="$MESSAGE"
            
            echo "Notification sent to Telegram."
        else
            echo "Hostname: $HOSTNAME - Inode usage on partition $PARTITION is below threshold. No action needed."
        fi
    else
        echo "Error: Unable to retrieve inode usage for partition $PARTITION. Check the df -i output."
    fi
done
