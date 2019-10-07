#this builds the response to send to Slack
import slack_settings
import re,datetime,random

# work out what time of day it is
currentTime = datetime.datetime.now()
currentTime.hour
0
if currentTime.hour < 12:
  time = ("Good morning")
elif 12 <= currentTime.hour < 18:
  time = ("Good afternoon")
else:
  time = ("Good evening")


def ziggy(payload):
    response = {"text":"","attachments":""}
    if payload["event"]["type"] == "app_mention":
    #playlist creator
        if bool(re.search('(?:make|create|haz).*playlist', payload["event"]["text"])):
            response["text"] = slack_settings.playlist_text
            response["attachments"] = slack_settings.playlist_attachement
            return response
            
    #we get a mention
        else:
            response["text"] = random.choice(slack_settings.mention_text_list)
            return response

    #a user is added to the channel
    elif payload["event"]["type"] == "member_joined_channel":
        response["text"] = time + "! Welcome to the #music channel :wave: :guitar:"
        return response

    #something weird that we are not expecting
    else:
        text = str(payload)
        response["text"] = "What the heck was that?"
        return response
