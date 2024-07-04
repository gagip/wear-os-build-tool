#!/bin/bash
ngrok authtoken $NGROK_AUTH_TOKEN

ngrok http 5000 > /dev/null &

sleep 5
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')

echo "ngrok URL: $NGROK_URL"