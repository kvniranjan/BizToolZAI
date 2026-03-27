#!/bin/bash
npx cloudflared tunnel --url http://localhost:3030 > cloudflare.log 2>&1 &
sleep 5
grep "trycloudflare.com" cloudflare.log | grep -o 'https://[-a-zA-Z0-9.]*\.trycloudflare\.com' | head -1
