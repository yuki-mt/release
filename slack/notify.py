import json
import urllib.request

# how to create URL: https://api.slack.com/messaging/webhooks
webhook_url = 'https://hooks.slack.com/services/xxx/xxx/xxx'
payload = {
    "channel": "#general",
    "username": "webhookbot",
    "icon_emoji": ":ghost:",
    'text': "<https://example.com|Overlook Hotel>\n:x: :ok: "
}
req = urllib.request.Request(webhook_url,
                             json.dumps(payload).encode())
with urllib.request.urlopen(req) as res:
    body = res.read()
