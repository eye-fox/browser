#!/bin/bash
# Trigger browser task dari HP/termux
# Usage: ./trigger.sh "task description disini"

TOKEN="TOKEN_GITHUB_ANDA"
REPO="eye-fox/browser"

if [ -z "$1" ]; then
  echo "Usage: $0 \"task description\""
  echo "Example: $0 \"Login ke shopify, screenshot dashboard\""
  exit 1
fi

curl -s -X POST "https://api.github.com/repos/$REPO/dispatches" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "$(printf '{"event_type":"run-task","client_payload":{"task":"%s"}}' "$1")"

echo "Task dikirim! Cek progress di:"
echo "https://github.com/$REPO/actions"
