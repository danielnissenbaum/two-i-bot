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

#get the message we received from slack, and see what the HECK Is in there!!

def logic(payload):
    response = {"text":"","attachments":""}
    #someone sent a message @ing the bot
    if payload["event"]["type"] == "app_mention":
    #search their message for some specific thing, if we find it, send something back
        if bool(re.search('(?:some specific thing', payload["event"]["text"])):
            response["text"] = slack_settings.call_to_action_text
            response["attachments"] = slack_settings.call_to_action_attachement
            return response

    #otherwise it's just a standard @ mention
        else:
            response["text"] = random.choice(slack_settings.mention_text_list)
            return response

    #a user is added to the channel
    elif payload["event"]["type"] == "member_joined_channel":
        response["text"] = time + "! Welcome to the CHANNEL"
        return response

    #something weird that we are not expecting
    else:
        text = str(payload)
        response["text"] = "What the heck was that?"
        return response
