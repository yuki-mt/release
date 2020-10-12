import json
import urllib.request

headers = {
    'Content-Type': 'application/json',
}
# how to create URL: https://api.slack.com/messaging/webhooks
webhook_url = ('https://hooks.slack.com/services/xxx/xxx/xxx')
payload = {
    'text': "<https://example.com|Overlook Hotel>\n:x: :ok: "
}
req = urllib.request.Request(webhook_url,
                             json.dumps(payload).encode(),
                             headers)
with urllib.request.urlopen(req) as res:
    body = res.read()
