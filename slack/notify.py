import json
import urllib.request

# how to create URL: https://api.slack.com/messaging/webhooks
webhook_url = 'https://hooks.slack.com/services/xxx/xxx/xxx'
payload = {
    "channel": "#general",
    "username": "webhookbot",
    "icon_emoji": ":ghost:",
    "text": "Optional text that appears above the attachment block",
    'text': "<https://example.com|Overlook Hotel>\n:x: :ok: "
}
# attachments, blocks:
# https://api.slack.com/messaging/webhook://api.slack.com/reference/messaging/attachments#fields
rich_payload = {
    "channel": "#general",
    "username": "webhookbot",
    "icon_emoji": ":ghost:",
    "attachments": [
        {
            "mrkdwn_in": ["text"],
            "color": "good",  # can be warning or danger
            "pretext": "Optional text that appears above the attachment block",
            "title": "title",
            "title_link": "https://api.slack.com/",
            "text": "Optional `text` that appears within the attachment",
            "fields": [
                {
                    "title": "A field's title",
                    "value": "This field's value",
                    "short": False
                },
            ],
        }
    ]
}
req = urllib.request.Request(webhook_url,
                             json.dumps(payload).encode())
with urllib.request.urlopen(req) as res:
    body = res.read()
