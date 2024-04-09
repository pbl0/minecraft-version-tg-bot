#!/bin/sh

CHAT_ID=$(cat /srv/bot/chat_id.txt | tr -d '\n')
TELEGRAM_TOKEN=$(cat /srv/bot/token.txt | tr -d '\n')


echo "Patching config..."
sed -i 's/{CHAT_ID}/'"$CHAT_ID"'/g' /minecraft-version-change-telegram.py
sed -i 's/{TELEGRAM_TOKEN}/'"$TELEGRAM_TOKEN"'/g' /minecraft-version-change-telegram.py


python3 /minecraft-version-change-telegram.py
