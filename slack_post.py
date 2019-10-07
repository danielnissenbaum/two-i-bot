import requests,json
import app

def post(response):
    payload = {
    "channel": app.CHANNEL_ID,
    "token": str(app.BOT_USER_TOKEN),
    "text": response["text"],
    "attachments": response["attachments"]
    }

    headers = {"Content-type":"application/json;charset=utf-8", "Authorization":"Bearer "+ str(app.BOT_USER_TOKEN)}
    r = requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=json.dumps(payload))

    return "you can close this now"